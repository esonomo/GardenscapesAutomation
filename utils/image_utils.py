import os

import cv2
import numpy as np

from configs.constants import TEMP_SCREENSHOTS_FOLDER


def draw_rectangle_on_screenshot(screenshot_img: np.ndarray, coordinates: tuple[int, int, int, int], filename: str) -> None:
    """
    Draws a rectangle on the screenshot image and saves it.

    Args:
        screenshot_img (np.ndarray): The image on which to draw the rectangle.
        coordinates (Tuple[int, int, int, int]): The coordinates of the rectangle in the format (x_min, y_min, x_max, y_max).
        filename (str): The name of the file to save the modified image.
    """
    x_min, y_min, x_max, y_max = coordinates
    img_with_rectangle = screenshot_img.copy()
    cv2.rectangle(img_with_rectangle, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    save_path = os.path.join(TEMP_SCREENSHOTS_FOLDER, filename)
    cv2.imwrite(str(save_path), img_with_rectangle)


def multi_scale_template_matching(
        screenshot_img: np.ndarray,
        template_img: np.ndarray,
        scale_range: tuple[float, float] = (0.5, 1.5),
        step: float = 0.1
):
    """
    Performs multiscale template matching on a screenshot image.

    Args:
        screenshot_img (np.ndarray): The image in which to search for the template.
        template_img (np.ndarray): The template image to search for.
        scale_range (Tuple[float, float]): The range of scales to apply to the template.
        step (float): The step size for scaling the template.

    Returns:
        Tuple[float, Tuple[int, int], Tuple[int, int], float]: A tuple containing:
            - The best matching value (confidence).
            - The location of the best match (top-left corner).
            - The size of the best matching template.
            - The scale at which the best match was found.
    """
    screenshot_gray = cv2.cvtColor(screenshot_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    best_match = None
    best_val = -1
    best_loc = None
    best_scale = 1

    for scale in np.arange(scale_range[0], scale_range[1], step):
        scaled_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if scaled_template.shape[0] > screenshot_gray.shape[0] or scaled_template.shape[1] > screenshot_gray.shape[1]:
            continue
        result = cv2.matchTemplate(screenshot_gray, scaled_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > best_val:
            best_val = max_val
            best_match = scaled_template
            best_loc = max_loc
            best_scale = scale
    return best_val, best_loc, best_match.shape[::-1], best_scale


def take_screenshot(appium_driver, save_directory: str, filename: str):
    """
    Takes a screenshot using the Appium driver and saves it to the specified directory.

    Args:
        appium_driver: The Appium driver instance used to take the screenshot.
        save_directory (str): The directory where the screenshot will be saved.
        filename (str): The name of the file to save the screenshot as.
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    appium_driver.get_screenshot_as_file(os.path.join(save_directory, filename))
