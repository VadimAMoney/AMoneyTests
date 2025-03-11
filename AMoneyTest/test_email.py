import subprocess
import time
import requests
import psycopg2
import pytest
from mitmproxy.tools.main import mitmdump
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Глобальная переменная для токена
TOKEN = None

# Настройки Appium
capabilities = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554"
}

capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = "http://localhost:4723"

@pytest.fixture(scope="module")
def db_connection():
    """Подключение к PostgreSQL"""
    conn = psycopg2.connect(
        dbname="test_email",
        user="postgres",
        password="qwerty123",
        host="localhost",
        port="5432"
    )
    conn.autocommit = False
    yield conn
    conn.rollback()
    conn.close()

def start_mitmproxy():
    """Запускает mitmproxy в фоне для перехвата токена"""
    return subprocess.Popen(["mitmdump", "-w", "network_log"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_token_from_mitm():
    """Извлекает токен из записанных сетевых запросов"""
    global TOKEN
    with open("network_log", "r", encoding="utf-8") as f:
        for line in f:
            if "Authorization: Bearer" in line:
                TOKEN = line.split("Authorization: Bearer ")[1].strip()
                print(f"✅ Получен токен: {TOKEN}")
                break

def register_and_get_token(driver):
    """Проходит регистрацию и получает токен"""
    proxy = start_mitmproxy()

    open_AMoney(driver)
    onbording(driver)
    fast_registration_skip(driver)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/homeScreen"))
    )

    time.sleep(5)

    proxy.terminate()
    get_token_from_mitm()

    assert TOKEN, "Ошибка: не удалось получить токен!"
    return TOKEN

def open_AMoney(driver):
    """Открытие приложения 'А деньги'"""
    aps = driver.find_element(by=AppiumBy.XPATH, value="//*[contains(@text, 'А деньги')]")
    aps.click()

def onbording(driver):
    """Прохождение онбординга"""
    texts = [
        "Пользуйтесь деньгами\nбез процентов",
        "Заполните короткую анкету\nи получите деньги на карту любого банка",
        "Можно получить заём\nдаже с плохой кредитной историей"
    ]

    for expected_text in texts:
        el = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textDescription"]'))
        )
        assert el.text == expected_text, f"Ожидаемый текст '{expected_text}', но найден: '{el.text}'"
        driver.find_element(by=AppiumBy.ID, value='ru.adengi:id/buttonNext').click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/text_policy'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/declineButton'))
    ).click()

def fast_registration_skip(driver):
    """Пропуск быстрого входа"""
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonContinue'))
        )
        button.click()
    except TimeoutException:
        print("Кнопка не была найдена или не кликабельна")



def test_find_user(db_connection):
    """Тест на поиск пользователя в БД и подтверждение кода"""
    global TOKEN

    URL = "https://stage01.adengi.tech/api/v1/client/me"
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(URL, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка запроса: {response.status_code}, {response.text}"

    data = response.json()
    client_id = data.get("client", {}).get("client", {}).get("id")
    print(f"✅ Получен client_id: {client_id}")

    cursor = db_connection.cursor()
    cursor.execute("SELECT id, client_id, email, type FROM email_confirmation WHERE client_id = %s", (client_id,))
    user = cursor.fetchone()

    email_confirmation_id = user[0]
    print(f"Найден пользователь: ID: {user[0]}, Client ID: {user[1]}, Email: {user[2]}, Type: {user[3]}")

    cursor.execute(
        "SELECT id, email_confirmation_id, code FROM email_confirmation_codes WHERE email_confirmation_id = %s",
        (email_confirmation_id,)
    )
    verification = cursor.fetchone()
    verification_id = verification[0]
    new_code = "136789"

    print(f"Найден код подтверждения: ID: {verification[0]}, Email Confirmation ID: {verification[1]}, Code: {verification[2]}")
    cursor.execute("UPDATE email_confirmation_codes SET code = %s WHERE id = %s", (new_code, verification_id))
    db_connection.commit()

    print(f"Код обновлен в email_confirmation_codes: {new_code}")

    post_url = "https://stage01.adengi.tech/api/v1/email_confirmation/confirm"
    post_headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    post_body = {"code": new_code}

    post_response = requests.post(post_url, headers=post_headers, json=post_body)
    assert post_response.status_code == 200, f"Ошибка при подтверждении: {post_response.status_code}, {post_response.text}"

    print(f"Ответ API: {post_response.status_code}, {post_response.json()}")

def fast_registration_skip(driver):
    button_get_money = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonGetMoney')))
    button_get_money.click()
    while True:
        try:
            # Ожидаем появления кнопки "Continue" на экране
            button_continue = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonContinue')))
            button_continue.click()
            print("Кнопка 'Continue' была нажата")
        except TimeoutException:
            # Если кнопка не найдена, то переходим к следующему экрану или завершаем цикл
            print("Кнопка 'Continue' не найдена, переходим к следующему экрану или завершаем.")
            break  # Прерываем цикл, если кнопка не найдена, либо можно продолжить на след. экран

def notification_button_test(driver):
    button_notification = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonGetMoney')))
    button_notification.click()

def check_text_not_present(driver):
        try:
            # Ожидаем, что элемент с данным локатором НЕ будет видим в течение 10 секунд
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textTitle"]')))
            print("Надпись отсутствует на экране.")
        except TimeoutException:
            # Если элемент видим, то выбрасывается исключение, значит он всё же был найден
            print("Надпись всё ещё видна на экране.")


def test_fast_reg(driver):
    open_AMoney(driver)
    onbording(driver)
    fast_registration_skip(driver)

