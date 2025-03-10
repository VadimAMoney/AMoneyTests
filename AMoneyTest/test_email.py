import subprocess

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import pytest
import time




capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554"
}



capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = "http://localhost:4723"

@pytest.fixture()
def driver():
    app_driver = webdriver.Remote(appium_server_url, options=capabilities_options)
    yield app_driver
    if app_driver:
        app_driver.quit()


def