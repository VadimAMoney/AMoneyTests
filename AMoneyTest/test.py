from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import pytest

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

def test_AMoney(driver):
    aps = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value= 'А деньги')
    aps.click()

def test_onbording(driver):
    el_onbording1 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]')
    txt = el_onbording1.text
    expected_text = "Пользуйтесь деньгами\nбез процентов"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/buttonNext')
    button.click()



def test_onbording2(driver):
    el_onbording2 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]')
    txt = el_onbording2.text
    expected_text= "Заполните короткую анкету\nи получите деньги на карту любого банка"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext')
    button.click()

def test_onbording3(driver):
    txt_onbording3 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]')
    txt = txt_onbording3.text
    expected_text = "Можно получить заём\nдаже с плохой кредитной историей"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext')
    button.click()

def test_agreement(driver):
    txt_agreement = driver.find_element(by=AppiumBy.ID, value="ru.adengi:id/text_policy")
    txt = txt_agreement.text
    expected_text = "В целях нормального функционирования мобильного приложения Вам необходимо предоставить согласие на сбор, обработку и хранение следующих данных:\nИмя пользователя, Адрес электронной почты, Номер телефона, Местоположение и Фотографии - собираются и хранятся с целью выполнения функций приложения, предотвращения мошенничества, повышения уровня безопасности и соответствие требованиям Федерального закона от 27.07.2006 № 152-ФЗ «О персональных данных». Идентификаторы устройства, Идентификаторы пользователей> - собираются и хранятся с целью выполнения функций приложения, предотвращения мошенничества, повышения уровня безопасности и повышения качества обслуживания.\n\nОбращаем внимание, что Вы можете отказаться предоставлять указанные данные далее в процессе использования приложения.\n\nИнформируем также, что обработка персональных данных осуществляется только в тех случаях, когда получено согласие субъекта на обработку его персональных данных. При обработке персональных данных принимаются необходимые правовые, организационные и технические меры для защиты персональных данных от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения персональных данных, а также от иных неправомерных действий в отношении персональных данных, в соответствии с требованиями ст.19 Федерального закона от 27 июля 2006 г. № 152-ФЗ «О персональных данных». Хранение персональных данных осуществляется с учетом обеспечения режима их конфиденциальности."
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/buttonNext')
    button.click()

def test_push_and_off(driver):
    push_desk_txt = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/description')
    txt_push = push_desk_txt.text
    expected_text = "Предлагаем подписаться на push-уведомления для получения своевременных уведомлений о наступлении важных дат в жизни вашего займа, а также о доступности интересных для вас предложений "
    assert txt_push == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt_push}'"
    button_decline = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/declineButton')
    button_decline.click()

def test_get_money(driver):
    button_get_money = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/buttonGetMoney')
    button_get_money.click()