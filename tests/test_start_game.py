from screens.terms_of_use_privacy_policy_screen import TermsOfUsePrivacyPolicyPopup


def test_start_game(appium_driver):
    terms_of_use_privacy_policy_screen = TermsOfUsePrivacyPolicyPopup(appium_driver)
    home_screen = terms_of_use_privacy_policy_screen.accept_terms_of_use()
    game_screen = home_screen.start_game()
    assert game_screen.is_game_screen_visible(), "Game screen is not visible"
