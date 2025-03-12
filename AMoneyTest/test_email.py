import pytest
import requests
import psycopg2
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# 🔹 Конфигурация Appium
capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554"
}
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = "http://localhost:4723"


# 🔹 Фикстура для драйвера
@pytest.fixture(scope="module")
def driver():
    app_driver = webdriver.Remote(appium_server_url, options=capabilities_options)
    yield app_driver
    app_driver.quit()


# 🔹 Фикстура для БД
@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        dbname="test_email",
        user="postgres",
        password="qwerty123",
        host="localhost",
        port="5432"
    )
    yield conn
    conn.rollback()  # Откат изменений после теста
    conn.close()


def open_AMoney(driver):
    aps = driver.find_element(by=AppiumBy.XPATH, value="//*[contains(@text, 'А деньги')]")
    aps.click()

def onbording(driver):
    # Ожидание появления первого элемента
    el_onbording1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]'))
    )
    txt = el_onbording1.text
    expected_text = "Пользуйтесь деньгами\nбез процентов"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/buttonNext')
    button.click()

    # Ожидание появления второго элемента
    el_onbording2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]'))
    )
    txt = el_onbording2.text
    expected_text = "Заполните короткую анкету\nи получите деньги на карту любого банка"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext')
    button.click()

    # Ожидание появления третьего элемента
    txt_onbording3 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]'))
    )
    txt = txt_onbording3.text
    expected_text = "Можно получить заём\nдаже с плохой кредитной историей"
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext')
    button.click()

    # Ожидание появления текста согласия
    txt_agreement = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/text_policy'))
    )
    txt = txt_agreement.text
    expected_text = "В целях нормального функционирования мобильного приложения Вам необходимо предоставить согласие на сбор, обработку и хранение следующих данных:\nИмя пользователя, Адрес электронной почты, Номер телефона, Местоположение и Фотографии - собираются и хранятся с целью выполнения функций приложения, предотвращения мошенничества, повышения уровня безопасности и соответствие требованиям Федерального закона от 27.07.2006 № 152-ФЗ «О персональных данных». Идентификаторы устройства, Идентификаторы пользователей> - собираются и хранятся с целью выполнения функций приложения, предотвращения мошенничества, повышения уровня безопасности и повышения качества обслуживания.\n\nОбращаем внимание, что Вы можете отказаться предоставлять указанные данные далее в процессе использования приложения.\n\nИнформируем также, что обработка персональных данных осуществляется только в тех случаях, когда получено согласие субъекта на обработку его персональных данных. При обработке персональных данных принимаются необходимые правовые, организационные и технические меры для защиты персональных данных от неправомерного или случайного доступа к ним, уничтожения, изменения, блокирования, копирования, предоставления, распространения персональных данных, а также от иных неправомерных действий в отношении персональных данных, в соответствии с требованиями ст.19 Федерального закона от 27 июля 2006 г. № 152-ФЗ «О персональных данных». Хранение персональных данных осуществляется с учетом обеспечения режима их конфиденциальности."
    assert txt == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{txt}'"
    button = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext')
    button.click()

    # Ожидание появления push-уведомления
    push_desk_txt = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/description'))
    )
    button_decline = driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/declineButton')
    button_decline.click()
#Вот это переработать
def fast_registration_skip(driver):
    button_get_money = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonGetMoney'))
    )
    button_get_money.click()

    # Ждем появления поля и считываем номер
    phone_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextPhone"))
    )
    phone_number = phone_element.text.strip()

    print(f"📱 Сохраненный номер телефона: {phone_number}")

    button_continue_1 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/buttonContinue"]')))
    button_continue_1.click()

    button_continue_2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/buttonContinue"]')))
    button_continue_2.click()

    button_continue_3 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/continueButton"]')))
    button_continue_3.click()

    button_continue_4 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/buttonContinue"]')))
    button_continue_4.click()

    button_continue_5 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/buttonAction"]')))
    button_continue_5.click()

    return phone_number


# 🔹 Фикстура для хранения номера телефона (результат test_fast_reg)
@pytest.fixture(scope="module")
def registered_phone_number(driver):
    """Проходит регистрацию и возвращает номер телефона"""
    open_AMoney(driver)
    onbording(driver)
    return fast_registration_skip(driver)
    assert phone_number, "Ошибка! Номер телефона не получен."



# 🔹 Фикстура для получения токена
@pytest.fixture(scope="module")
def access_token(registered_phone_number):
    TOKEN_URL = "https://stage01.adengi.tech/api/v1/oauth/token"
    data = {
        "client_id": 100,
        "client_secret": "secret",
        "grant_type": "password",
        "password": "123456",
        "username": registered_phone_number
    }

    response = requests.post(TOKEN_URL, json=data)
    assert response.status_code == 200, f"Ошибка запроса: {response.status_code}, {response.text}"

    tokens = response.json()
    ACCESS_TOKEN = tokens.get("access_token")
    assert ACCESS_TOKEN, "Ошибка! Access token не получен."

    return ACCESS_TOKEN  # Возвращаем токен для использования в следующих тестах


# 🔹 Тест регистрации (должен быть первым)



# 🔹 Тест API-запроса (начинается только после успешного теста регистрации)
def test_get_client_info(access_token):
    URL = "https://stage01.adengi.tech/api/v1/client/me"
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(URL, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка запроса: {response.status_code}, {response.text}"

    data = response.json()
    client_id = data.get("client", {}).get("client", {}).get("id")
    assert client_id, "Ошибка! client_id не получен."

    print(f"✅ Получен client_id: {client_id}")


# 🔹 Тест работы с БД (использует client_id)
def test_find_user(db_connection, access_token):
    cursor = db_connection.cursor()

    # Получаем client_id через API
    URL = "https://stage01.adengi.tech/api/v1/client/me"
    HEADERS = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(URL, headers=HEADERS)
    data = response.json()
    client_id = data.get("client", {}).get("client", {}).get("id")

    assert client_id, "Ошибка! client_id не получен."

    # Поиск пользователя в БД
    cursor.execute("SELECT id, client_id, email, type FROM email_confirmation WHERE client_id = %s", (client_id,))
    user = cursor.fetchone()
    assert user, "Ошибка! Пользователь не найден в email_confirmation."

    email_confirmation_id = user[0]
    print(f"✅ Найден пользователь: ID: {user[0]}, Client ID: {user[1]}, Email: {user[2]}, Type: {user[3]}")

    # Получаем код подтверждения
    cursor.execute(
        "SELECT id, email_confirmation_id, code FROM email_confirmation_codes WHERE email_confirmation_id = %s",
        (email_confirmation_id,))
    verification = cursor.fetchone()
    assert verification, "Ошибка! Код подтверждения не найден."

    verification_id = verification[0]
    new_code = "333333"

    # Обновляем код в БД
    cursor.execute("UPDATE email_confirmation_codes SET code = %s WHERE id = %s", (new_code, verification_id))
    db_connection.commit()
    print(f"✅ Код подтверждения обновлен: {new_code}")

    # Отправляем код в API
    post_url = "https://stage01.adengi.tech/api/v1/email_confirmation/confirm"
    post_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    post_body = {"code": new_code}

    post_response = requests.post(post_url, headers=post_headers, json=post_body)
    assert post_response.status_code == 200, f"Ошибка при подтверждении: {post_response.status_code}, {post_response.text}"
    print(f"✅ Подтверждение успешно: {post_response.json()}")


