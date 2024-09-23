import os
import time

import cv2
import numpy as np
import logging

from selenium.common import NoSuchElementException

from configs.constants import FAILED_SCREENSHOTS_FOLDER, TEMP_SCREENSHOTS_FOLDER
from utils.image_utils import multi_scale_template_matching, draw_rectangle_on_screenshot, take_screenshot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseScreen:
    def __init__(self, appium_driver):
        self.appium_driver = appium_driver

    logger = logging.getLogger(__name__)

    def find_image_in_screenshot(
            self,
            template_path: str,
            max_val_threshold: float = 0.5
    ):
        """
        Finds the specified image in the current screenshot taken by the Appium driver.

        Args:
            template_path (str): The file path to the template image to find.
            max_val_threshold (float): The threshold for maximum confidence value to consider the image found.

        Returns:
            list[float] | None: The coordinates of the found image's center (x, y) or None if not found.
        """
        screenshot = self.appium_driver.get_screenshot_as_png()
        nparr = np.frombuffer(screenshot, np.uint8)
        template_name = template_path.split('/')[-1]
        screenshot_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        template_img = cv2.imread(template_path)

        if screenshot_img is None or template_img is None:
            logger.error("Error loading images.")
            return None

        max_val, top_left, (template_width, template_height), best_scale = multi_scale_template_matching(
            screenshot_img,
            template_img
        )
        if max_val < max_val_threshold:
            logger.error(f"{template_name} image not found with sufficient confidence. Max_val = {max_val}")
            return None

        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        coordinates = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

        draw_rectangle_on_screenshot(screenshot_img, coordinates, filename=template_name)

        logger.info(f"Max value: {max_val}")
        logger.info(
            f"{template_name} Image found at: Top-Left: {top_left}, Bottom-Right: {bottom_right}, Scale: {best_scale}")

        center_x = (top_left[0] + bottom_right[0]) / 2
        center_y = (top_left[1] + bottom_right[1]) / 2
        return [(center_x, center_y)]

    def get_element_coordinates(
            self,
            template_path: str,
            timeout: int = 30,
            interval: int = 1
    ) -> list[float]:
        """
        Retrieves the coordinates of an element by finding its template in the screenshot.

        Args:
            template_path (str): The file path to the template image.
            timeout (int): Maximum time to wait for the element to appear.
            interval (int): Time to wait between checks.

        Returns:
            list[float]: The coordinates of the element's center (x, y).

        Raises:
            FileNotFoundError: If the template file does not exist.
            NoSuchElementException: If the element is not found within the timeout.
        """
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"File not found at path: {template_path}. Current directory: {os.getcwd()}")

        element_name = template_path.split('/')[-1]
        start_time = time.time()
        while time.time() - start_time < timeout:
            element_coordinates = self.find_image_in_screenshot(template_path)

            if element_coordinates:
                return element_coordinates
            logger.debug(f"Waiting {interval} seconds")
            time.sleep(interval)

        take_screenshot(
            self.appium_driver,
            save_directory=str(os.path.join(TEMP_SCREENSHOTS_FOLDER, FAILED_SCREENSHOTS_FOLDER)),
            filename="failed_screen.png")
        raise NoSuchElementException(f"{element_name} element not found")
