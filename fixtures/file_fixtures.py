import pytest
import shutil
import os

from configs.constants import TEMP_SCREENSHOTS_FOLDER


@pytest.fixture(scope='session', autouse=True)
def clean_temp_screenshots():
    """
      Fixture to clean up the temporary screenshots folder before each test function.

      This fixture removes the temporary screenshots directory if it exists
      and creates a new one to ensure a clean state for each test.
    """
    if os.path.exists(TEMP_SCREENSHOTS_FOLDER):
        shutil.rmtree(TEMP_SCREENSHOTS_FOLDER)
    os.makedirs(TEMP_SCREENSHOTS_FOLDER)
