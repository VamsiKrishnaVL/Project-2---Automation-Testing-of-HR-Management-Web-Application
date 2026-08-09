from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_tc04_menu_items(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    assert dashboard.is_visible(DashboardPage.MENU_ADMIN)
    assert dashboard.is_visible(DashboardPage.MENU_PIM)
    assert dashboard.is_visible(DashboardPage.MENU_LEAVE)
    assert dashboard.is_visible(DashboardPage.MENU_TIME)
    assert dashboard.is_visible(DashboardPage.MENU_RECRUIT)
    assert dashboard.is_visible(DashboardPage.MENU_MYINFO)
    # logout
    dashboard.logout()
