from pages.login_page import LoginPage

def test_tc03_login_fields_presence(driver):
    login = LoginPage(driver)
    login.load()
    assert login.is_visible(LoginPage.USERNAME)
    assert login.is_visible(LoginPage.PASSWORD)
