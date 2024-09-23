from screens.base_screen import BaseScreen
from screens.game_screen import GameScreen


class HomeScreen(BaseScreen):
    _home_screen_template_path = "../screens/element_templates/home_screen.png"
    _play_button_template_path = "../screens/element_templates/play_btn.png"

    def start_game(self):
        self.get_element_coordinates(self._home_screen_template_path)
        play_btn = self.get_element_coordinates(self._play_button_template_path)
        self.appium_driver.tap(play_btn)
        return GameScreen(self.appium_driver)
