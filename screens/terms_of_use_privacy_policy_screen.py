from screens.base_screen import BaseScreen
from screens.home_screen import HomeScreen


class TermsOfUsePrivacyPolicyPopup(BaseScreen):
    _terms_of_use_popup_template_path = "../screens/element_templates/terms_of_use_privacy_policy_popup.png"
    _ok_btn_template_path = "../screens/element_templates/ok_btn.png"

    def accept_terms_of_use(self):
        self.get_element_coordinates(self._terms_of_use_popup_template_path)
        ok_btn = self.get_element_coordinates(self._ok_btn_template_path)
        self.appium_driver.tap(ok_btn)
        return HomeScreen(self.appium_driver)
