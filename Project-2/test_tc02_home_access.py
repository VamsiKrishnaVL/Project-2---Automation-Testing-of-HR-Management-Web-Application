from pages.login_page import LoginPage

def test_tc02_home_access(driver):
    login = LoginPage(driver)
    login.load()
    assert "orangehrmlive" in driver.current_url
