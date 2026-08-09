import pytest
import os
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.excel_utils import read_login_csv
from utils.logger import setup_logger

logger = setup_logger(os.path.join("reports", "logs", "execution.log"))
DATA_PATH = os.path.join("testdata", "login_data.csv")

@pytest.mark.parametrize("row", read_login_csv(DATA_PATH))
def test_tc01_login_data_driven(driver, row):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    login.load()
    username = row.get("username")
    password = row.get("password")
    expected = row.get("expected").lower()  # "pass" or "fail"
    login.login(username, password)
    if expected == "pass":
        assert dashboard.is_logged_in(), "Expected to be logged in but not"
        # logout to reset
        dashboard.logout()
        logger.info(f"TC01: Login passed for {username}")
    else:
        err = login.get_error()
        assert err != "", "Expected error message for invalid credentials"
        logger.info(f"TC01: Login failed as expected for {username}")
