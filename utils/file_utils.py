import os

from configs.constants import APK_FILENAME


def find_project_root() -> str:
    """
    Searches for the .apk file in the root directory

    Returns:
        str: Absolute normal path to the .apk file (including file name).

    Raises:
        NameError: If the file was not found.
    """
    folder = os.getcwd()
    file_name = APK_FILENAME

    while folder != os.path.dirname(folder):
        files = os.listdir(folder)
        if file_name in files:
            return folder
        folder = os.path.normpath(os.path.join(folder, os.pardir))

    raise NameError(f"No {file_name} file found")


PROJECT_PATH = find_project_root()

