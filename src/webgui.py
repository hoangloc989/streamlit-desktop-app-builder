import os
import sys
import shutil
import time
import uuid
import signal
import psutil
import tempfile
import platform
import subprocess
import socketserver
from multiprocessing import Process
from threading import Thread
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union
from shutil import which
import logging

__version__ = "0.3.7"

WEBGUI_USED_PORT = None
WEBGUI_BROWSER_PROCESS = None

OPERATING_SYSTEM = platform.system().lower()
PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"

def is_python2():
    return sys.version_info[0] < 3

def find_executable():
    """
    As distutils.spawn.find_executable, but on Windows, look up
    every extension declared in PATHEXT instead of just `.exe`
    """
    executable = PY
    path = None
    if not is_python2():
        # shutil.which() already uses PATHEXT on Windows, so on
        # Python 3 we can simply use shutil.which() in all cases.
        # (https://github.com/docker/docker-py/commit/42789818bed5d86b487a030e2e60b02bf0cfa284)
        return which(executable, path=path)

    if sys.platform != 'win32':
        return which(executable, path)

    if path is None:
        path = os.environ['PATH']

    paths = path.split(os.pathsep)
    extensions = os.environ.get('PATHEXT', '.exe').split(os.pathsep)
    base, ext = os.path.splitext(executable)

    if not os.path.isfile(executable):
        for p in paths:
            for ext in extensions:
                f = os.path.join(p, base + ext)
                if os.path.isfile(f):
                    return f
        return None
    else:
        return executable

def get_free_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    return free_port

def kill_port(port: int):
    for proc in psutil.process_iter():
        try:
            for conns in proc.connections(kind="inet"):
                if conns.laddr.port == port:
                    proc.send_signal(signal.SIGTERM)
        except psutil.AccessDenied:
            continue

def find_browser():
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

browser_path_dispacher: Dict[str, Callable[[], str]] = {
    "windows": find_browser
}

class BaseDefaultServer:
    server: Callable
    get_server_kwargs: Callable

webserver_dispacher: Dict[str, BaseDefaultServer] = {}

@dataclass
class GUI:
    server: Union[str, Callable[[Any], None]]
    server_kwargs: dict = None
    app: Any = None
    port: int = None
    width: int = None
    height: int = None
    fullscreen: bool = True
    on_startup: Callable = None
    on_shutdown: Callable = None
    extra_flags: List[str] = None
    browser_path: str = None
    browser_command: List[str] = None
    socketio: Any = None
    profile_dir_prefix: str = "webgui"

    def __post_init__(self):
        self.__keyboard_interrupt = False
        global WEBGUI_USED_PORT

        if self.port is None:
            self.port = (self.server_kwargs.get("port") if self.server_kwargs else get_free_port())

        WEBGUI_USED_PORT = self.port

        if isinstance(self.server, str):
            default_server = webserver_dispacher[self.server]
            self.server = default_server.server
            self.server_kwargs = self.server_kwargs or default_server.get_server_kwargs(
                app=self.app, port=self.port, flask_socketio=self.socketio)

        self.profile_dir = os.path.join(tempfile.gettempdir(), self.profile_dir_prefix + uuid.uuid4().hex)
        self.url = f"http://127.0.0.1:{self.port}"

        self.browser_path = (self.browser_path or browser_path_dispacher.get(OPERATING_SYSTEM)())
        self.browser_command = self.browser_command or self.get_browser_command()

        if not self.browser_path:
            print("Path to browser not found.")
            self.browser_command = [PY, "-m", "webbrowser", "-n", self.url]

    def get_browser_command(self):
        flags = [
            self.browser_path,
            f"--user-data-dir={self.profile_dir}",
            "--new-window",
            "--no-first-run",
        ]

        if self.width and self.height:
            flags.extend([f"--window-size={self.width},{self.height}"])
        elif self.fullscreen:
            flags.extend(["--start-maximized"])

        if self.extra_flags:
            for flag in self.extra_flags:
                flags.extend([flag])

        flags.extend([f"--app={self.url}"])

        return flags

    def start_browser(self, server_process: Union[Thread, Process]):
        try:
            print("Command:", " ".join(self.browser_command))
            global WEBGUI_BROWSER_PROCESS

            WEBGUI_BROWSER_PROCESS = subprocess.Popen(self.browser_command)
            WEBGUI_BROWSER_PROCESS.wait()

            if self.browser_path is None:
                while self.__keyboard_interrupt is False:
                    time.sleep(1)

            if isinstance(server_process, Process):
                if self.on_shutdown is not None:
                    self.on_shutdown()
                shutil.rmtree(self.profile_dir, ignore_errors=True)
                server_process.kill()
            else:
                if self.on_shutdown is not None:
                    self.on_shutdown()
                shutil.rmtree(self.profile_dir, ignore_errors=True)
                kill_port(self.port)
        except Exception as e:
            logging.error("Error launching browser: %s", e)

    def run(self):
        logging.info("webgui run start")
        if self.on_startup is not None:
            self.on_startup()

        server_process = Thread(target=self.server, kwargs=self.server_kwargs or {})
        logging.info(f"webgui server_process: {server_process}")
        time.sleep(1)
        browser_thread = Thread(target=self.start_browser, args=(server_process,))
        logging.info(f"webgui browser_thread: {browser_thread}")

        try:
            server_process.start()
            browser_thread.start()

            while server_process.is_alive() and browser_thread.is_alive():
                time.sleep(1)

            # Log statuses when the loop exits
            if not server_process.is_alive():
                logging.warning("Server process has stopped.")
            if not browser_thread.is_alive():
                logging.warning("Browser thread has stopped.")

            server_process.join()
            browser_thread.join()

        except Exception as e:
            logging.error(f"Error in run method: {e}")