# Gardenscapes Automation

## Overview
This project is an automation framework for testing the mobile game Gardenscapes using Appium and OpenCV. The goal is to automate user interactions and validate the game's UI elements through image recognition.

## Installing the dependencies

1. **Create a virtual environment:** 
```bash 
python -m venv .venv 
``` 
2. **Activate the virtual environment:** 
- On macOS/Linux:
```bash 
source .venv/bin/activate 
``` 
- On Windows: 
```bash
.venv\Scripts\activate 
``` 
3. **Install the dependencies:** 
```bash
pip install -r requirements.txt 
``` 

4. **Add the application file to the root of the project:** 

   The name of the .apk file should be com.playrix.gardenscapes.apk.
## Running Tests 
**To run the automated tests, navigate to the *tests* directory**:
```bash
cd tests
```
**and start tests using the following command:**
```bash 
pytest
```

- In the `configs/constants.py` file, specify the name of your device or emulator (DEVICE_NAME) and platform (PLATFORM_NAME) and operating system version (PLATFORM_VERSION).
- The name of your device or emulator can be obtained using the command: 
```bash
 adb devices 
``` 
- If you are using a real device, ensure that **Developer Mode** and **USB debugging** is activated.

## Test Environment

Test was successfully run on a real **Huawei Y6 2019** device with **Android version 9**.


## Project Structure

- __GardenscapesAutomation__
   - __configs__ # Configuration files
     - [constants.py](configs/constants.py) # Constants for configuration
   - __fixtures__ # Fixtures for test setup
     - [appium_setup.py](fixtures/appium_setup.py) # Appium setup and driver management
     - [file_fixtures.py](fixtures/file_fixtures.py) # Fixtures for files and folders
   - __screens__ # Screen definitions and element templates
       - __element_templates__ # Directory for image templates used for matching
         - [base_screen.py](screens/base_screen.py) # Base screen class with common methods
         - [game_screen.py](screens/game_screen.py) # Class for handling the game screen
         - [home_screen.py](screens/home_screen.py) # Class for handling the home screen
         - [terms_of_use_privacy_policy_screen.py](screens/terms_of_use_privacy_policy_screen.py) # Class for handling terms of use and privacy policy screen
   - __tests__ # Contains test cases
     - __temp_screenshots__ # Directory for temporary screenshots. The folder is cleared every test
       - __failed_screenshots__ # Directory for storing screenshots of the entire screen when OpenCV is unable to find the template
     - [conftest.py](tests/conftest.py) # List of fixtures
     - [test_start_game.py](tests/test_start_game.py) # Automated test for starting the game
  - __utils__ # Utility functions
    - [file_utils.py](utils/file_utils.py) # File and folder processing utilities
    - [image_utils.py](utils/image_utils.py) # Image processing utilities
  - [requirements.txt](requirements.txt) # List of project dependencies
  - [README.md](README.md) # Project documentation
