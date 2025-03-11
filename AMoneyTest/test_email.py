import subprocess

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import psycopg2
import requests
from selenium.common.exceptions import TimeoutException



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
    conn.autocommit = False  # Отключаем автокоммит, чтобы можно было откатывать тестовые данные    # Возможно вот это убьёт БД, Надо быть осторожнее
    yield conn
    conn.rollback()  # Откатываем все изменения после теста
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

def fast_registration_skip(driver):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((AppiumBy.ID, 'ru.adengi:id/buttonContinue')))
        button.click()
    except TimeoutException:
        print("Кнопка не была найдена или не кликабельна")

def test_fast_reg(driver):
    open_AMoney(driver)
    onbording(driver)
    fast_registration_skip(driver)

# ТОКЕН
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxMDAiLCJqdGkiOiI3NDdiYzVhYzkzZThkYWE0MDFiMmM4NzBlM2JhMDA5ZmI3MTIzNGQ1YmU2MWZlMjRhZDU0ZDlkYzk1MWZhYjExM2E0ZmU5ZTE3MjA2ZjU0MSIsImlhdCI6MTc0MTY5NTg5MS41NTE3ODcsIm5iZiI6MTc0MTY5NTg5MS41NTE3ODgsImV4cCI6MTc0MTcxMDI5MS41NDQwMjMsInN1YiI6Ijg1MTU1Iiwic2NvcGVzIjpbXX0.Gbltigl409hKivPZGveZGquuuME3PxsgUU9V0WhViNQzB0jYFNHvTgkYfamjgkrzyCr97FrLtov1VEMN_0UWIRn_AZ3k1dgD0CDAOfIj5npm0t-It3A5X4RYWRoinxPunhSMcKl6FgltlDimTnPf3z-Y1XLE1lJ_MiIOn42wbmnD5py9_SwbhNZhE43iys-Q25FaRCC2QTTcAVou_E8nU20QNcFtZcuC9F5x0gT_cZVwVNGnrxpxFxwFJH0QTv8obu3mV0zgif2K_YCNUgX4SWLpewtClrRxmHq5nWM4qONFEI0RNXOJQjAth-oLfWv4FTzXe-en2rYaL429ndGMh-KKAw9brclRosTvOc-r55CFoOnNMre7MVCAJiymHxCc5wlbisno1izfOvMWxkRE1df2xZ2iffISI4FsJxQFU9L_jCmeJYMkj5sOxk0qkerFX1jQ9ZiJoqyL3MAje0s1CtPjKHbdXYtc5w17DngFNOp-cW3Pl3GZWXgy-Ns5VMszY3UEE1CEt9rv_XQ-ax1tqnwjv_SLQsaq0TGNOU2-92Jv2YYHNb5r5B8QgPZdO0eyj9QUqffM08YKDQ2Kjfcx35iyTDko3AzJlh2Kl5H8kRA0hfbEN8L-Ivh3eNiTqpEaaM_mmZeEXaeCHu8hqtyjcNLQkLSts3HA8d00olDNXF0"
URL = "https://stage01.adengi.tech/api/v1/client/me"
HEADERS = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone64_x86_64 Build/TE1A.240213.009)",  # здесь тоже не понятно
    "Device-Id": "710bfeffa84db427", # здесь потом надо исправить
    "Client-Name": "AndroidApp",
    "Client-Version": "316442",                # здесь потом надо исправить
    "Package-Id": "ru.adengi",
    "Accept": "application/json",
    "Cookie": "_ga=1.2.223760086.1741678617",   # здесь потом надо исправить
    "Authorization": f"Bearer {TOKEN}"
}
response = requests.get(URL, headers=HEADERS)
assert response.status_code == 200, f"Ошибка запроса: {response.status_code}, {response.text}"
data = response.json()
client_id = data.get("client", {}).get("client", {}).get("id")
print(f"✅ Получен client_id: {client_id}")

def test_find_user(db_connection):
    cursor = db_connection.cursor()


    cursor.execute("SELECT id, client_id, email, type FROM email_confirmation WHERE client_id = %s", (client_id,))
    user = cursor.fetchone()  # Получаем одну строку





    email_confirmation_id = user[0]

    print(f" Найден пользователь: ID: {user[0]}, Client ID: {user[1]}, Email: {user[2]}, Type: {user[3]}")


    cursor.execute(
        "SELECT id, email_confirmation_id, code FROM email_confirmation_codes WHERE email_confirmation_id = %s",
        (email_confirmation_id,))
    verification = cursor.fetchone()



    verification_id = verification[0]  # ID записи в email_confirmation_codes
    new_code = "136789"

    print(
        f" Найден код подтверждения: ID: {verification[0]}, Email Confirmation ID: {verification[1]}, Code: {verification[2]}")


    cursor.execute("UPDATE email_confirmation_codes SET code = %s WHERE id = %s", (new_code, verification_id))
    db_connection.commit()  # Фиксируем изменения

    print(f" Код обновлен в email_confirmation_codes: {new_code}")

    post_url = "https://stage01.adengi.tech/api/v1/email_confirmation/confirm"
    post_headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    post_body = {"code": new_code}

    post_response = requests.post(post_url, headers=post_headers, json=post_body)


    assert post_response.status_code == 200, f" Ошибка при подтверждении: {post_response.status_code}, {post_response.text}"

    print(f" Ответ API: {post_response.status_code}, {post_response.json()}")