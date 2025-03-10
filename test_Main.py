
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import pytest
from time import sleep

capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554",
    "appPackage": "com.android.settings",
    "appActivity": ".Settings",
    "language": "en",
    "locale": "US"
}
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = "http://localhost:4723"


@pytest.fixture()
def driver():
    app_driver = webdriver.Remote(appium_server_url, options=capabilities_options)
    yield app_driver
    if app_driver:
        app_driver.quit()



def test_find_battery(driver) -> None:
    print("Тест начался!")
    el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
    el.click()
    sleep(5)