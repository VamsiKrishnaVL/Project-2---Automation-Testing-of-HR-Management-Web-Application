import pytest
import os
from utils.driver_factory import DriverFactory
from utils.logger import setup_logger

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
LOGS_DIR = os.path.join(REPORTS_DIR, "logs")
SCREENSHOT_DIR = os.path.join(REPORTS_DIR, "screenshots")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logger = setup_logger(os.path.join(LOGS_DIR, "execution.log"))

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    driver = DriverFactory().get_driver(browser)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # capture result and take screenshot on failure
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            import os
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                logger.error(f"Saved screenshot: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to save screenshot: {e}")
