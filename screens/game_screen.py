from selenium.common import NoSuchElementException

from screens.base_screen import BaseScreen


class GameScreen(BaseScreen):
    _game_screen = "../screens/element_templates/game_screen.png"

    def is_game_screen_visible(self):
        try:
            self.get_element_coordinates(self._game_screen)
            return True
        except NoSuchElementException:
            self.logger.error("Game screen is not visible")
            return False

