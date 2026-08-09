from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os

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
            raise ValueError(f"Unsupported browser: {browser}")
        driver.implicitly_wait(2)
        return driver
