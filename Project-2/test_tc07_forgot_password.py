from pages.login_page import LoginPage

def test_tc07_forgot_password(driver):
    login = LoginPage(driver)
    login.load()
    login.click_forgot()
    # The demo site opens a reset page; validate presence of reset form or message
    assert "forgotPassword" in driver.current_url or "reset" in driver.current_url or login.is_visible(LoginPage.FORGOT_LINK) == False
