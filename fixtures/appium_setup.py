import os
import time

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

from configs.constants import APK_FILENAME, APPIUM_ADDRESS, APPIUM_PORT, PACKAGE_NAME
from configs.constants import APPIUM_URL
from configs.constants import PLATFORM_NAME, PLATFORM_VERSION, DEVICE_NAME
from utils.file_utils import PROJECT_PATH


@pytest.fixture(scope='session', autouse=True)
def appium_server():
    """
    Fixture to start and stop the Appium server for the entire test session.

    Yields:
        None: This fixture does not return a value but manages the Appium service lifecycle.
    """
    appium_service = AppiumService()
    appium_service.start(args=['--address', APPIUM_ADDRESS, '--port', APPIUM_PORT])
    yield
    try:
        appium_service.stop()
        start_time = time.time()
        while time.time() - start_time < 10:
            if appium_service.is_running:
                time.sleep(0.5)
            else:
                break
    except Exception as e:
        print(f"Error stopping Appium service: {e}")


@pytest.fixture()
def appium_driver(appium_server):
    """
    Fixture to create and tear down an Appium driver instance.

    Args:
        appium_server (None): Implicitly requires the Appium server to be running.

    Yields:
        webdriver.Remote: An instance of the Appium driver.
    """
    driver = get_driver()
    yield driver
    driver.remove_app(PACKAGE_NAME)
    driver.quit()


def get_driver():
    """
    Creates an Appium driver with the specified desired capabilities.

    Returns:
        webdriver.Remote: A remote WebDriver instance for interacting with the mobile application.
    """
    desired_caps = dict()
    desired_caps["platformName"] = PLATFORM_NAME
    desired_caps["platformVersion"] = PLATFORM_VERSION
    desired_caps["deviceName"] = DEVICE_NAME
    desired_caps["automationName"] = 'UiAutomator2'
    desired_caps["newCommandTimeout"] = 300
    desired_caps["app"] = os.path.join(PROJECT_PATH, APK_FILENAME)
    desired_caps["fullReset"] = True

    options = UiAutomator2Options().load_capabilities(desired_caps)
    driver = webdriver.Remote(
        command_executor=APPIUM_URL,
        options=options,
        keep_alive=True)

    return driver
