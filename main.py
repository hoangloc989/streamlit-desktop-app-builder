import os
import sys
import logging
import subprocess
from src.webgui import GUI

# Configure logging
logging.basicConfig(filename=os.path.join(os.getenv('APPDATA'),
                                          'streamlit_server.log'),
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def start_streamlit(**server_kwargs):
    script = server_kwargs.pop("script", None)
    port = server_kwargs.pop("port", 8501)
    headless = server_kwargs.pop("headless", True)

    python_executable = sys.executable  # Use the Python executable provided by Pynsist

    logging.info(f"Python Path: {python_executable}")

    command = [
        python_executable, "-m", "streamlit", "run", script, "--server.port",
        str(port), "--server.headless",
        str(headless).lower(), "--global.developmentMode=false"
    ]

    try:
        logging.info("Starting Streamlit server with command: %s",
                     " ".join(command))
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        logging.info(stdout.decode())
        if stderr:
            logging.error(stderr.decode())
    except subprocess.CalledProcessError as e:
        logging.error("Streamlit server failed with error: %s", e)
    except Exception as e:
        logging.error("Error starting Streamlit: %s", e)
    finally:
        logging.info("Streamlit server has exited.")
        if process:
            process.terminate()


def main():
    # Determine the base path dynamically
    if 'pythonw' in sys.executable:
        # If running as a bundled executable
        pkgs_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(pkgs_path)
    else:
        # If running directly from source
        base_path = os.path.dirname(os.path.abspath(__file__))

    streamlit_app_script = os.path.join(base_path, "app", "main_app.py")

    gui = GUI(
        server=start_streamlit,
        server_kwargs={
            "script": streamlit_app_script,
            "port": 8501
        },
        width=1024,
        height=600,
        fullscreen=False,
        on_startup=lambda: print(
            f"Streamlit app starting...\n"
            f"ScriptPath: {streamlit_app_script}"
        ),
        on_shutdown=lambda: print("Streamlit app shutting down..."))

    gui.run()

if __name__ == "__main__":
    main()
