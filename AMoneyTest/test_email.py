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
import re

# Конфигурация Appium
capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554"
}
capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = "http://localhost:4723"


#  Фикстура для драйвера
@pytest.fixture(scope="module")
def driver():
    app_driver = webdriver.Remote(appium_server_url, options=capabilities_options)
    yield app_driver
    app_driver.quit()


#  Фикстура для БД
@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        dbname="adengi",
        user="adengi_team",
        password="xpt2od18FxmZPeyw",
        host="stage01.adengi.tech",
        port="5432"
    )
    yield conn
    conn.rollback()  # Откат изменений после теста
    conn.close()


def open_AMoney(driver):
    aps = driver.find_element(by=AppiumBy.XPATH, value="//*[contains(@text, 'А деньги')]")
    aps.click()


def onbording(driver):
    # Проход по онбордингу
    for expected_text in [
        "Пользуйтесь деньгами\nбез процентов",
        "Заполните короткую анкету\nи получите деньги на карту любого банка",
        "Можно получить заём\nдаже с плохой кредитной историей"
    ]:
        el = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]'))
        )
        assert el.text == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{el.text}'"
        driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext').click()

    # Согласие на обработку данных
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/text_policy'))
    )
    driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext').click()

    # Отклонение push-уведомления
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/description'))
    )
    driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/declineButton').click()


#  Регистрация с очисткой номера телефона
def fast_registration_skip(driver):
    button_get_money = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonGetMoney'))
    )
    button_get_money.click()

    # Ждем появления поля и получаем номер
    phone_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextPhone"))
    )
    phone_number = phone_element.text.strip()

    # Убираем `+` и пробелы
    phone_number = re.sub(r"\D", "", phone_number)

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


#  Фикстура для хранения номера телефона
@pytest.fixture(scope="module")
def registered_phone_number(driver):
    """Проходит регистрацию и возвращает номер телефона"""
    open_AMoney(driver)
    onbording(driver)
    phone_number = fast_registration_skip(driver)

    assert phone_number, "Ошибка! Номер телефона не получен."
    return phone_number

def check_text_not_present(driver):
    # Ожидаем появления кнопки уведомлений и кликаем по ней
    button_notification = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/nav_notification')))
    button_notification.click()

    try:
        # Ожидаем, что элемент с данным локатором НЕ будет видим в течение 10 секунд
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textTitle"]')))
        print("Надпись отсутствует на экране.")
    except TimeoutException:
        # Если элемент видим, то выбрасывается исключение, значит он всё же был найден
        print("Надпись всё ещё видна на экране.")


#  Фикстура для получения токена
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

    return ACCESS_TOKEN


#  Тест API-запроса
def test_get_client_info(access_token):
    URL = "https://stage01.adengi.tech/api/v1/client/me"
    HEADERS = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(URL, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка запроса: {response.status_code}, {response.text}"

    data = response.json()
    client_id = data.get("client", {}).get("client", {}).get("id")
    assert client_id, "Ошибка! client_id не получен."

    print(f"✅ Получен client_id: {client_id}")


#  Тест работы с БД
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
    cursor.execute("SELECT * FROM email_confirmations WHERE client_id = %s", (client_id,))
    user = cursor.fetchone()
    assert user, "Ошибка! Пользователь не найден в email_confirmation."

    email_confirmation_id = user[0]
    print(f"✅ Найден пользователь: ID: {user[0]}, Client ID: {user[1]}, Email: {user[2]}, Type: {user[3]}")

    # Получаем код подтверждения
    cursor.execute(
        "SELECT * FROM email_confirmation_codes WHERE email_confirmation_id = %s",
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

    check_text_not_present(driver)