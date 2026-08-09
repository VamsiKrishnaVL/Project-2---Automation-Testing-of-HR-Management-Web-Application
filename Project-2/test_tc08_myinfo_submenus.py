from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.myinfo_page import MyInfoPage

def test_tc08_myinfo_submenus(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    myinfo = MyInfoPage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    dashboard.click(DashboardPage.MENU_MYINFO)
    assert myinfo.is_visible(MyInfoPage.PERSONAL)
    myinfo.open_personal()
    myinfo.open_contact()
    myinfo.open_emergency()
    myinfo.open_dependents()
    dashboard.logout()
