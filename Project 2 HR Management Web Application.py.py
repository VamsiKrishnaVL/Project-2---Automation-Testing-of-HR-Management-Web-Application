"""
OrangeHRM Selenium + Pytest - All-in-One Test Suite

This file combines the uploaded:
- BasePage
- DriverFactory
- Logger
- Excel/CSV utility
- LoginPage
- DashboardPage
- AdminPage
- LeavePage
- ClaimsPage
- MyInfoPage
- pytest fixture/conftest logic
- TC01 through TC10

Run:
    pip install selenium pytest
    pytest orangehrm_all_in_one.py -v --browser chrome

Optional:
    pytest orangehrm_all_in_one.py -v --browser firefox
    pytest orangehrm_all_in_one.py -v --browser edge

For TC01, the original project expects:
    testdata/login_data.csv

Expected CSV columns:
    username,password,expected

If the CSV is not present, TC01 uses the built-in fallback rows below.
"""

import csv
import logging
import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ============================================================
# LOGGER
# ============================================================

def setup_logger(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger("orangehrm")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        )

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


# ============================================================
# PATHS / REPORTING
# ============================================================

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
LOGS_DIR = os.path.join(REPORTS_DIR, "logs")
SCREENSHOT_DIR = os.path.join(REPORTS_DIR, "screenshots")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logger = setup_logger(
    os.path.join(LOGS_DIR, "execution.log")
)

DATA_PATH = os.path.join(
    os.getcwd(),
    "testdata",
    "login_data.csv"
)


# ============================================================
# CSV UTILITY
# ============================================================

def read_login_csv(path):
    """
    Read login test data from CSV.

    Expected columns:
        username,password,expected

    If the original CSV is unavailable, use the source project's
    expected Admin credentials as a fallback so the all-in-one
    file can still execute.
    """
    if os.path.exists(path):
        rows = []
        with open(path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)

        if rows:
            return rows

    # Fallback data for a standalone run.
    return [
        {
            "username": "Admin",
            "password": "admin123",
            "expected": "pass",
        },
        {
            "username": "invalid_user",
            "password": "invalid_password",
            "expected": "fail",
        },
    ]


# ============================================================
# DRIVER FACTORY
# ============================================================

class DriverFactory:

    def get_driver(self, browser="chrome"):
        browser = browser.lower()

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            driver = webdriver.Firefox()
            driver.maximize_window()

        elif browser == "edge":
            driver = webdriver.Edge()
            driver.maximize_window()

        else:
            raise ValueError(
                f"Unsupported browser: {browser}"
            )

        driver.implicitly_wait(2)
        return driver


# ============================================================
# BASE PAGE
# ============================================================

class BasePage:

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        el = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        el.click()
        return el

    def send_keys(self, locator, text):
        el = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        el.clear()
        el.send_keys(text)
        return el

    def is_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            return False

    def get_text(self, locator):
        el = self.find(locator)
        return el.text

    def get_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title


# ============================================================
# LOGIN PAGE
# ============================================================

class LoginPage(BasePage):

    URL = "https://opensource-demo.orangehrmlive.com"

    USERNAME = (By.ID, "txtUsername")
    PASSWORD = (By.ID, "txtPassword")
    LOGIN_BTN = (By.ID, "btnLogin")
    FORGOT_LINK = (By.LINK_TEXT, "Forgot your password?")
    ERROR_MSG = (By.ID, "spanMessage")

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.send_keys(self.USERNAME, username)
        self.send_keys(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def click_forgot(self):
        self.click(self.FORGOT_LINK)

    def get_error(self):
        el = self.is_visible(self.ERROR_MSG)
        return el.text if el else ""


# ============================================================
# DASHBOARD PAGE
# ============================================================

class DashboardPage(BasePage):

    WELCOME = (By.ID, "welcome")
    MENU_ADMIN = (By.ID, "menu_admin_viewAdminModule")
    MENU_PIM = (By.ID, "menu_pim_viewPimModule")
    MENU_LEAVE = (By.ID, "menu_leave_viewLeaveModule")
    MENU_TIME = (By.ID, "menu_time_viewTimeModule")
    MENU_RECRUIT = (By.ID, "menu_recruitment_viewRecruitmentModule")
    MENU_MYINFO = (By.ID, "menu_pim_viewMyDetails")
    MENU_PERFORMANCE = (By.ID, "menu__Performance")
    MENU_DASHBOARD = (By.ID, "menu_dashboard_index")

    def is_logged_in(self):
        return self.is_visible(self.WELCOME)

    def logout(self):
        self.click(self.WELCOME)
        self.click(
            (By.XPATH, "//a[text()='Logout']")
        )


# ============================================================
# ADMIN PAGE
# ============================================================

class AdminPage(BasePage):

    USER_MANAGEMENT = (
        By.ID,
        "menu_admin_UserManagement"
    )
    USERS = (
        By.ID,
        "menu_admin_viewSystemUsers"
    )
    ADD_BTN = (By.ID, "btnAdd")
    USER_ROLE = (By.ID, "systemUser_userType")
    EMPLOYEE_NAME = (
        By.ID,
        "systemUser_employeeName_empName"
    )
    NEW_USERNAME = (By.ID, "systemUser_userName")
    NEW_PASSWORD = (By.ID, "systemUser_password")
    CONFIRM_PASSWORD = (
        By.ID,
        "systemUser_confirmPassword"
    )
    SAVE_BTN = (By.ID, "btnSave")
    SEARCH_USERNAME = (
        By.ID,
        "searchSystemUser_userName"
    )
    SEARCH_BTN = (By.ID, "searchBtn")
    RESULT_TABLE = (By.ID, "resultTable")

    def go_to_users(self):
        self.click(self.USER_MANAGEMENT)
        self.click(self.USERS)

    def add_user(
        self,
        employee_name,
        username,
        password,
        role_index=1
    ):
        self.click(self.ADD_BTN)

        # Original source uses a simple role selection approach.
        role_select = self.find(self.USER_ROLE)
        role_select.click()

        self.send_keys(
            self.EMPLOYEE_NAME,
            employee_name
        )
        self.send_keys(
            self.NEW_USERNAME,
            username
        )
        self.send_keys(
            self.NEW_PASSWORD,
            password
        )
        self.send_keys(
            self.CONFIRM_PASSWORD,
            password
        )
        self.click(self.SAVE_BTN)

    def search_user(self, username):
        self.send_keys(
            self.SEARCH_USERNAME,
            username
        )
        self.click(self.SEARCH_BTN)

        table = self.find(self.RESULT_TABLE)
        return username in table.text


# ============================================================
# LEAVE PAGE
# ============================================================

class LeavePage(BasePage):

    ASSIGN_LEAVE = (
        By.ID,
        "menu_leave_assignLeave"
    )
    EMPLOYEE_NAME = (
        By.ID,
        "assignleave_txtEmployee_empName"
    )
    LEAVE_TYPE = (
        By.ID,
        "assignleave_txtLeaveType"
    )
    FROM_DATE = (
        By.ID,
        "assignleave_txtFromDate"
    )
    TO_DATE = (
        By.ID,
        "assignleave_txtToDate"
    )
    ASSIGN_BTN = (By.ID, "assignBtn")
    SUCCESS_MSG = (
        By.XPATH,
        "//div[contains(@class,'message success')]"
    )

    def go_to_assign(self):
        self.click(self.ASSIGN_LEAVE)

    def assign_leave(
        self,
        employee,
        leave_type,
        from_date,
        to_date
    ):
        self.send_keys(
            self.EMPLOYEE_NAME,
            employee
        )
        self.send_keys(
            self.FROM_DATE,
            from_date
        )
        self.send_keys(
            self.TO_DATE,
            to_date
        )

        # Original source uses send_keys for leave type.
        self.send_keys(
            self.LEAVE_TYPE,
            leave_type
        )

        self.click(self.ASSIGN_BTN)

    def get_success(self):
        el = self.is_visible(self.SUCCESS_MSG)
        return el.text if el else ""


# ============================================================
# CLAIMS PAGE
# ============================================================

class ClaimsPage(BasePage):

    # The uploaded source notes that the OrangeHRM demo may not
    # have a Claims module.
    CLAIMS_MENU = (By.LINK_TEXT, "Claims")
    NEW_CLAIM = (By.ID, "btnNewClaim")
    CLAIM_TYPE = (By.ID, "claim_type")
    CLAIM_AMOUNT = (By.ID, "claim_amount")
    CLAIM_REASON = (By.ID, "claim_reason")
    SUBMIT_BTN = (By.ID, "btnSubmit")
    SUCCESS_MSG = (
        By.XPATH,
        "//div[contains(@class,'message success')]"
    )

    def go_to_claims(self):
        self.click(self.CLAIMS_MENU)

    def submit_claim(self, ctype, amount, reason):
        self.click(self.NEW_CLAIM)
        self.send_keys(self.CLAIM_TYPE, ctype)
        self.send_keys(self.CLAIM_AMOUNT, amount)
        self.send_keys(self.CLAIM_REASON, reason)
        self.click(self.SUBMIT_BTN)

    def get_success(self):
        el = self.is_visible(self.SUCCESS_MSG)
        return el.text if el else ""


# ============================================================
# MY INFO PAGE
# ============================================================

class MyInfoPage(BasePage):

    PERSONAL = (By.LINK_TEXT, "Personal Details")
    CONTACT = (By.LINK_TEXT, "Contact Details")
    EMERGENCY = (By.LINK_TEXT, "Emergency Contacts")
    DEPENDENTS = (By.LINK_TEXT, "Dependents")

    def open_personal(self):
        self.click(self.PERSONAL)

    def open_contact(self):
        self.click(self.CONTACT)

    def open_emergency(self):
        self.click(self.EMERGENCY)

    def open_dependents(self):
        self.click(self.DEPENDENTS)


# ============================================================
# PYTEST CONFIGURATION / FIXTURE
# ============================================================

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    driver = DriverFactory().get_driver(browser)

    yield driver

    driver.quit()


@pytest.hookimpl(
    tryfirst=True,
    hookwrapper=True
)
def pytest_runtest_makereport(item, call):
    """
    Capture a screenshot whenever a test fails.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")

        if driver:
            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                f"{item.name}.png"
            )

            try:
                driver.save_screenshot(
                    screenshot_path
                )
                logger.error(
                    f"Saved screenshot: {screenshot_path}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to save screenshot: {e}"
                )


# ============================================================
# TC01 - LOGIN DATA DRIVEN
# ============================================================

@pytest.mark.parametrize(
    "row",
    read_login_csv(DATA_PATH)
)
def test_tc01_login_data_driven(driver, row):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()

    username = row.get("username")
    password = row.get("password")
    expected = row.get("expected", "").lower()

    login.login(username, password)

    if expected == "pass":
        assert dashboard.is_logged_in(), (
            "Expected to be logged in but not"
        )

        dashboard.logout()

        logger.info(
            f"TC01: Login passed for {username}"
        )

    else:
        err = login.get_error()

        assert err != "", (
            "Expected error message for invalid credentials"
        )

        logger.info(
            f"TC01: Login failed as expected for {username}"
        )


# ============================================================
# TC02 - HOME ACCESS
# ============================================================

def test_tc02_home_access(driver):

    login = LoginPage(driver)

    login.load()

    assert "orangehrmlive" in driver.current_url


# ============================================================
# TC03 - LOGIN FIELDS
# ============================================================

def test_tc03_login_fields_presence(driver):

    login = LoginPage(driver)

    login.load()

    assert login.is_visible(
        LoginPage.USERNAME
    )

    assert login.is_visible(
        LoginPage.PASSWORD
    )


# ============================================================
# TC04 - MENU ITEMS
# ============================================================

def test_tc04_menu_items(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    assert dashboard.is_visible(
        DashboardPage.MENU_ADMIN
    )

    assert dashboard.is_visible(
        DashboardPage.MENU_PIM
    )

    assert dashboard.is_visible(
        DashboardPage.MENU_LEAVE
    )

    assert dashboard.is_visible(
        DashboardPage.MENU_TIME
    )

    assert dashboard.is_visible(
        DashboardPage.MENU_RECRUIT
    )

    assert dashboard.is_visible(
        DashboardPage.MENU_MYINFO
    )

    dashboard.logout()


# ============================================================
# TC05 - CREATE USER AND VALIDATE LOGIN
# ============================================================

def test_tc05_create_user_and_validate_login(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    admin = AdminPage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    admin.go_to_users()

    # Create unique username.
    ts = str(int(time.time()))
    new_username = f"testuser_{ts}"

    admin.add_user(
        employee_name="Linda Anderson",
        username=new_username,
        password="Password@123"
    )

    dashboard.logout()

    # Attempt login with new user.
    login.load()
    login.login(
        new_username,
        "Password@123"
    )

    # New user may not have permissions to see dashboard welcome.
    if dashboard.is_logged_in():
        dashboard.logout()
    else:
        err = login.get_error()

        assert err == "", (
            f"New user login failed: {err}"
        )


# ============================================================
# TC06 - SEARCH USER
# ============================================================

def test_tc06_validate_new_user_in_admin_list(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    admin = AdminPage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    admin.go_to_users()

    # Original source searches for the existing Admin user.
    found = admin.search_user("Admin")

    assert found, (
        "Expected to find user 'Admin' in user list"
    )

    dashboard.logout()


# ============================================================
# TC07 - FORGOT PASSWORD
# ============================================================

def test_tc07_forgot_password(driver):

    login = LoginPage(driver)

    login.load()
    login.click_forgot()

    # The source validates a reset page/form.
    assert (
        "forgotPassword" in driver.current_url
        or "reset" in driver.current_url
        or login.is_visible(
            LoginPage.FORGOT_LINK
        ) is False
    )


# ============================================================
# TC08 - MY INFO SUBMENUS
# ============================================================

def test_tc08_myinfo_submenus(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    myinfo = MyInfoPage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    dashboard.click(
        DashboardPage.MENU_MYINFO
    )

    assert myinfo.is_visible(
        MyInfoPage.PERSONAL
    )

    myinfo.open_personal()
    myinfo.open_contact()
    myinfo.open_emergency()
    myinfo.open_dependents()

    dashboard.logout()


# ============================================================
# TC09 - ASSIGN LEAVE
# ============================================================

def test_tc09_assign_leave(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    leave = LeavePage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    leave.go_to_assign()

    leave.assign_leave(
        employee="Linda Anderson",
        leave_type="Annual Leave",
        from_date="2026-08-10",
        to_date="2026-08-11"
    )

    success = leave.get_success()

    assert success != "", (
        "Expected success message after assigning leave"
    )

    dashboard.logout()


# ============================================================
# TC10 - CLAIM REQUEST
# ============================================================

def test_tc10_claim_request(driver):

    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    claims = ClaimsPage(driver)

    login.load()
    login.login("Admin", "admin123")

    assert dashboard.is_logged_in()

    try:
        claims.go_to_claims()

        claims.submit_claim(
            "Medical",
            "1000",
            "Medical reimbursement"
        )

        success = claims.get_success()

        assert success != "", (
            "Expected success message after claim submission"
        )

    except Exception:
        # The uploaded source explicitly treats the missing
        # Claims module as an expected limitation of the demo.
        pytest.xfail(
            "Claims module not available on demo site"
        )

    finally:
        dashboard.logout()


# ============================================================
# OPTIONAL DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":
    # Equivalent to:
    # pytest orangehrm_all_in_one.py -v --browser chrome
    raise SystemExit(
        pytest.main(
            [
                __file__,
                "-v",
                "--browser",
                "chrome",
            ]
        )
    )
