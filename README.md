# Streamlit as Desktop Application

Packaging a Streamlit application into an executable file using PyInstaller presents certain challenges and is not officially endorsed by Streamlit. Streamlit is primarily designed for developing web applications that operate on a server and are accessed through a web browser.

However, if you wish to proceed with this approach, you will need to create a script that initializes the Streamlit server and subsequently launches a web browser directed to the local address.

This script can then potentially be packaged into an executable using PyInstaller.
Please be aware that this method may not be suitable for all scenarios and could have inherent limitations. It is also crucial to manually verify the final list of requirements to mitigate potential dependency issues, as highlighted in discussions within the community.

# Quick start
This is an example of how to convert a streamlit app to an executable for Windows (.exe). To do this, we use the `pynsist` package.

1. Clone this repo
2. Create a new virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the new virtual environment:
    ```bash
    venv\Scripts\activate
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Get the tools. NSIS is a tool for creating Windows installers. It is used by pynsist to create the installer for the application. You can install NSIS by downloading the installer from the [NSIS website](http://nsis.sourceforge.net/Download).

6. Write a config file ``installer.cfg``, like this:
    ```ini
    [Application]
    name=MyStreamlitApp
    version=1.0
    entry_point=main:main

    [Python]
    version=3.12.3
    bitness=64

    [Include]
    pypi_wheels = altair==5.4.1
                attrs==24.2.0
                blinker==1.8.2
                ...
    files=.streamlit/
        app/ 
        src/ 
    ```

7. Run ``pynsist installer.cfg`` to generate your installer.
You have to add the dependencies to the installer.cfg file in order to be included in the executable. You can do this by adding the dependencies to the pypi_wheels section. You can use the output of pip freeze and then run:
    ```bash
    pynsist installer.cfg
    ```