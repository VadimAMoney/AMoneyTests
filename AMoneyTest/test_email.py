from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import logging
import uiautomator2 as u2
from selenium.common.exceptions import WebDriverException
import keyboard
import pyperclip
from datetime import datetime
from time import sleep
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
import requests
import psycopg2
import re
logging.basicConfig(level=logging.DEBUG)

apk_path = "C:/adengi/adengi-dev-1.0.28.5-webview-off.apk"
appium_server_url = "http://localhost:4723"
app_name = 'А деньги'
TEXT_FIELD_PXOME = "ru.adengi:id/editTextPhone"
element = "ru.adengi:id/editTextCity"
xpath_cc = '//android.widget.EditText[@resource-id="cc"]'
xpath_number = '//android.view.View[@resource-id="paymentType1"]/android.view.View[1]/android.view.View[1]/android.widget.EditText'
text_field = "4444555566661111"
xpath_cvv = '//android.widget.EditText[@resource-id="cvc"]'
text_cvv = "123"







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


@pytest.fixture(scope="session")
def appium_driver():
    """Фикстура для инициализации и закрытия драйвера Appium."""
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        language='en',
        locale='US',
        noReset=True
    )

    options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    driver.implicitly_wait(20)

    try:
        install_app(driver)
        yield driver
    finally:
        driver.quit()




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

# Свайп снизу вверх
def swipe_bottom_to_top(driver, duration=500):
    """Свайп снизу вверх."""
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] // 2
    end_y = screen_size['height'] // 4
    start_y = 1600

    driver.swipe(start_x, start_y, start_x, end_y, duration)
    logging.info(f"Выполнен свайп снизу вверх с координатами ({start_x}, {start_y}) -> ({start_x}, {end_y})")


def swipe_down(driver, start_y=1250, start_x_percent=0.5, end_y_percent=0.8, duration=500):
    """Свайп сверху вниз, с фиксированным start_y."""
    window_size = driver.get_window_size()
    screen_width = window_size['width']
    screen_height = window_size['height']

    start_x = int(screen_width * start_x_percent)  # Центрируем по горизонтали
    # start_y = int(screen_height * start_y_percent) # Начинаем с заданной Y координатой
    end_y = int(screen_height * end_y_percent)  # Заканчиваем ближе к низу экрана

    try:
        driver.swipe(start_x, start_y, start_x, end_y, duration)
        logging.info(f"Выполнен свайп сверху вниз с координатами ({start_x}, {start_y}) -> ({start_x}, {end_y})")

    except WebDriverException as e:
        logging.error(f"Ошибка при выполнении свайпа: {e}")
        raise  # Перебрасываем исключение, чтобы тест упал, если свайп не удался


def go_to_home(driver, duration=500):
    """Свайп снизу вверх."""
    screen_size = driver.get_window_size()
    start_x = 537
    end_y = screen_size['height'] // 4
    start_y = 1887

    driver.swipe(start_x, start_y, start_x, end_y, duration)
    logging.info(f"Выполнен свайп снизу вверх с координатами ({start_x}, {start_y}) -> ({start_x}, {end_y})")


def type_text_by_xpath(driver, xpath, text_to_type):
    """
    Находит элемент по XPath и вводит в него текст.
    """
    try:
        print(f"Попытка ввести текст '{text_to_type}' в элемент с XPath: {xpath}")
        element = driver.find_element(by=AppiumBy.XPATH, value=xpath)
        element.clear()  # Очищаем поле (рекомендуется, даже если поле пустое)
        element.send_keys(text_to_type)
        print(f"Текст '{text_to_type}' успешно введен.")
    except Exception as e:
        print(f"Ошибка при вводе текста: {e}")


# Ввод номера телефона

def enter_phone_number_press_keycode(driver, phone_number):
    """
    Вводит номер телефона, используя press_keycode для каждой цифры.
    Внимание: Этот метод менее надежен и рекомендуется только для
    специфических случаев.  Обычно лучше использовать send_keys().
    """
    key_codes = {
        '0': appium_driver.KeyCode.KEYCODE_0,
        '1': appium_driver.KEYCODE_1,
        '2': appium_driver.KEYCODE_2,
        '3': appium_driver.KEYCODE_3,
        '4': appium_driver.KEYCODE_4,
        '5': appium_driver.KEYCODE_5,
        '6': appium_driver.KEYCODE_6,
        '7': appium_driver.KEYCODE_7,
        '8': appium_driver.KEYCODE_8,
        '9': appium_driver.KEYCODE_9
    }
    try:
        for digit in phone_number:
            if digit in key_codes:
                driver.press_keycode(key_codes[digit])
            else:
                print(f"Предупреждение: Неизвестная цифра: {digit}")
        print(f"Номер телефона '{phone_number}' введен с помощью press_keycode.")
    except Exception as e:
        print(f"Произошла ошибка при вводе номера телефона: {e}")


# Запуск приложение
def launch_app(appium_driver, app_name):
    wait = WebDriverWait(appium_driver, 10)
    app_icon = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[@text='{app_name}']")))
    app_icon.click()


# Клик по id кнопки
def click_button_by_id(driver, button_id):
    """Функция для клика на кнопку по ее id."""
    try:
        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.presence_of_element_located((AppiumBy.ID, button_id)))
        button.click()
        logging.info(f"Нажата кнопка с id: {button_id}")
    except Exception as e:
        logging.exception(f"Ошибка при клике на кнопку с id: {button_id}: {e}")
        raise


# Установка приложения
def install_app(appium_driver):
    wait = WebDriverWait(appium_driver, 10)
    appium_driver.install_app(apk_path)
    print("Приложение установлено успешно.")
    swipe_bottom_to_top(appium_driver)
    sleep(0.5)
    launch_app(appium_driver, app_name)


# Удаление приложения

def delete_app(appium_driver):
    package_to_remove = "ru.adengi"
    try:
        appium_driver.execute_script('mobile: shell', {'command': 'pm uninstall', 'args': [package_to_remove]})
        print(f"Приложение '{package_to_remove}' успешно удалено.")
    except WebDriverException as e:
        print(f"Не удалось удалить приложение '{package_to_remove}'. Ошибка: {e}")


# Тест 1. Регистрация
def test_field_value_edit(appium_driver):
    wait = WebDriverWait(appium_driver, 10)

    # 1. Клики
    click_button_by_id(appium_driver, "ru.adengi:id/buttonSkip")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonNext")
    click_button_by_id(appium_driver, "ru.adengi:id/acceptButton")
    click_button_by_id(appium_driver, "com.android.permissioncontroller:id/permission_allow_button")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonGetMoney")
    # Ждем появления поля и получаем номер
    phone_element = WebDriverWait(appium_driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextPhone"))
    )
    phone_number = phone_element.text.strip()

    # Убираем `+` и пробелы
    phone_number = re.sub(r"\D", "", phone_number)

    print(f" Сохраненный номер телефона: {phone_number}")

    click_button_by_id(appium_driver, "ru.adengi:id/editTextPhone")

    number_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, TEXT_FIELD_PXOME)))

    # 2. Сохраняем текст из поля
    number_text = number_field.text

    # 3. Стираем текст из поля
    number_field.clear()

    # 4. Вводим сохраненный текст обратно в поле
    index_to_remove = 0
    new_string = number_text[:index_to_remove] + number_text[index_to_remove + 2:]
    number_field.send_keys(new_string)

    # Нажимаю на поле email

    email_field_id = "ru.adengi:id/editTextEmail"
    email_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, email_field_id)))
    email_field.click()

    # Стер и ввел поле email

    email_text = email_field.text
    email_field.clear()
    email_field.send_keys(email_text)

    # Нажал на поле Фамилии, стер и ввел поле фамилии

    lastName_field_id = 'ru.adengi:id/editTextLastName'
    lastName_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, lastName_field_id)))
    lastName_field.click()

    lastName_text = lastName_field.text
    lastName_field.clear()
    lastName_field.send_keys(lastName_text)

    # Нажал на поле имени, стер и ввел поле имя

    FirstName_field_id = 'ru.adengi:id/editTextFirstName'
    FirstName_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, FirstName_field_id)))
    FirstName_field.click()

    FirstName_text = FirstName_field.text
    FirstName_field.clear
    FirstName_field.send_keys(FirstName_text)

    # Нажал на поле отчество, стер и ввел поле отчество

    MidlleName_field_id = 'ru.adengi:id/editTextMiddleName'
    MidlleName_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, MidlleName_field_id)))
    MidlleName_field.click()

    MidlleName_text = MidlleName_field.text
    MidlleName_field.clear
    MidlleName_field.send_keys(MidlleName_text)

    # Скролл вниз

    swipe_bottom_to_top(appium_driver)

    # Клик на зарегистрироваться
    continue_id = 'ru.adengi:id/buttonContinue'
    continue_button = wait.until(EC.presence_of_element_located((AppiumBy.ID, continue_id)))
    continue_button.click()

    # Клик и ввод  смс кода

    sms_field_id = 'ru.adengi:id/editTextCode'
    sms_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, sms_field_id)))
    sms_field.click()

    sms_field_text = sms_field.text
    sms_field.clear
    sms_field.send_keys(sms_field_text)

    # Клик на смс поле

    next_button_id = 'ru.adengi:id/buttonContinue'
    next_button = wait.until(EC.presence_of_element_located((AppiumBy.ID, next_button_id)))
    next_button.click()

    text = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Паспорт"]')))
    print(text.text)

    if text.text == 'Паспорт':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')

    go_to_home(appium_driver)


    return phone_number

#  Фикстура для хранения номера телефона
@pytest.fixture(scope="module")
def registered_phone_number(driver):
    """Проходит регистрацию и возвращает номер телефона"""
    #здесь вставить методы
    test_field_value_edit(appium_driver)
    phone_number = test_field_value_edit(appium_driver)

    assert phone_number, "Ошибка! Номер телефона не получен."
    return phone_number
# Тест 2. Паспорт

def test_passport(appium_driver):
    wait = WebDriverWait(appium_driver, 10)

    # 1. Клики
    click_button_by_id(appium_driver, "ru.adengi:id/buttonSkip")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonNext")
    click_button_by_id(appium_driver, "ru.adengi:id/acceptButton")
    click_button_by_id(appium_driver, "com.android.permissioncontroller:id/permission_allow_button")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonGetMoney")

    wait.until(EC.presence_of_element_located((AppiumBy.ID, TEXT_FIELD_PXOME)))

    swipe_bottom_to_top(appium_driver)

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")

    # Нажал на поле серия, стер и ввел поле

    passport_number_id = 'ru.adengi:id/editTextPassportNumber'
    passport_number = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_number_id)))
    passport_number.click()

    passport_number_text = passport_number.text
    passport_number.clear()
    passport_number.send_keys(passport_number_text)

    # Нажал на поле дата, стер и ввел поле

    passport_data_id = 'ru.adengi:id/editTextPassportDate'
    passport_data = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_data_id)))
    passport_data.click()

    passport_data_text = passport_data.text
    passport_data.clear()
    passport_data.send_keys(passport_data_text)

    # Нажал на поле код, стер и ввел поле

    passport_subdivision_id = 'ru.adengi:id/editTextPassportSubdivision'
    passport_subdivision = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_subdivision_id)))
    passport_subdivision.click()

    passport_subdivision_text = passport_subdivision.text
    passport_subdivision.clear()
    passport_subdivision.send_keys(passport_subdivision_text)

    # Нажал на поле кем выдан, стер и ввел поле

    passport_issuer_id = 'ru.adengi:id/editTextPassportIssuer'
    passport_issuer = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_issuer_id)))
    passport_issuer.click()

    passport_issuer_text = passport_issuer.text
    passport_issuer.clear()
    passport_issuer.send_keys(passport_issuer_text)

    # Нажал на поле Дата рождения, стер и ввел поле

    passport_birth_date_id = 'ru.adengi:id/editTextPassportBirthDate'
    passport_birth_date = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_birth_date_id)))
    passport_birth_date.click

    passport_birth_date_text = passport_birth_date.text
    passport_birth_date.clear()
    passport_birth_date.send_keys(passport_birth_date_text)

    # Свайпнул вниз

    swipe_bottom_to_top(appium_driver)

    # Нажал на поле Место рождения, стер и ввел поле

    passport_birth_place_id = 'ru.adengi:id/editTextPassportBirthPlace'
    passport_birth_place = wait.until(EC.presence_of_element_located((AppiumBy.ID, passport_birth_place_id)))
    passport_birth_place.click()

    passport_birth_place_text = passport_birth_place.text
    passport_birth_place.clear()
    passport_birth_place.send_keys(passport_birth_place_text)

    click_button_by_id(appium_driver, "ru.adengi:id/continueButton")

    text = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@text="Адрес"])')))

    print(text.text)
    if text.text == 'Адрес':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')

    go_to_home(appium_driver)

    # Удалить приложение
    delete_app(appium_driver)


# Тест 3. Адрес

def test_address(appium_driver):
    wait = WebDriverWait(appium_driver, 20)

    # 1. Клики
    click_button_by_id(appium_driver, "ru.adengi:id/buttonSkip")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonNext")
    click_button_by_id(appium_driver, "ru.adengi:id/acceptButton")
    click_button_by_id(appium_driver, "com.android.permissioncontroller:id/permission_allow_button")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonGetMoney")

    wait.until(EC.presence_of_element_located((AppiumBy.ID, TEXT_FIELD_PXOME)))
    swipe_bottom_to_top(appium_driver)

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/buttonContinue")))
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextPassportNumber")))
    swipe_bottom_to_top(appium_driver)

    # 2. Кликабельность полей
    xpath_button = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/continueButton"]')))
    sleep(0.5)
    xpath_button.click()
    address_street = wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextStreet")))
    address_house = wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextHouse")))
    address_corps = wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextCorps")))
    swipe_bottom_to_top(appium_driver)
    address_flat = wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextFlat")))
    swipe_down(appium_driver, start_y=1040)

    click_button_by_id(appium_driver, "ru.adengi:id/editTextRegion")
    click_button_by_id(appium_driver, "ru.adengi:id/editTextCity")
    address_street.click()
    address_house.click()
    address_corps.click()
    swipe_bottom_to_top(appium_driver)
    address_flat.click()

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")

    # 3. Проверка на переход следущего этапа
    text = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@text="Занятость"])')))

    print(text.text)
    if text.text == 'Занятость':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')
        # Вернуться на главный экран
    go_to_home(appium_driver)

    # Удалить приложение
    delete_app(appium_driver)


# Тест 4. Занятость

def test_busyness(appium_driver):
    wait = WebDriverWait(appium_driver, 20)

    # 1. Клики
    click_button_by_id(appium_driver, "ru.adengi:id/buttonSkip")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonNext")
    click_button_by_id(appium_driver, "ru.adengi:id/acceptButton")
    click_button_by_id(appium_driver, "com.android.permissioncontroller:id/permission_allow_button")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonGetMoney")

    wait.until(EC.presence_of_element_located((AppiumBy.ID, TEXT_FIELD_PXOME)))
    swipe_bottom_to_top(appium_driver)

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/buttonContinue")))
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    wait.until(EC.presence_of_element_located((AppiumBy.ID, "ru.adengi:id/editTextPassportNumber")))
    swipe_bottom_to_top(appium_driver)
    xpath_button = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.Button[@resource-id="ru.adengi:id/continueButton"]')))
    sleep(0.5)
    xpath_button.click()
    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ru.adengi:id/editTextRegion')))
    swipe_bottom_to_top(appium_driver)
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")

    click_button_by_id(appium_driver, "ru.adengi:id/spinnerStatus")
    click_button_by_id(appium_driver, "ru.adengi:id/spinnerStatus")
    click_button_by_id(appium_driver, "ru.adengi:id/spinnerWorkExperience")

    # 2. Проверка поля сумма
    monthly_id = "ru.adengi:id/editMonthlyIncome"
    button_monthly = wait.until(EC.presence_of_element_located((AppiumBy.ID, monthly_id)))
    button_monthly.click()

    button_monthly_text = button_monthly.text
    button_monthly.clear()
    button_monthly.send_keys(button_monthly_text)

    click_button_by_id(appium_driver, "ru.adengi:id/buttonAction")

    # 3. Проверка на переход следущего этапа
    text = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@text="Идентификация"])')))

    print(text.text)
    if text.text == 'Идентификация':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')
        # Вернуться на главный экран
    go_to_home(appium_driver)

    # Удалить приложение
    delete_app(appium_driver)

def check_text_not_present(appium_driver):
    # Ожидаем появления кнопки уведомлений и кликаем по ней
    button_notification = WebDriverWait(appium_driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/nav_notification')))
    button_notification.click()

    try:
        # Ожидаем, что элемент с данным локатором НЕ будет видим в течение 10 секунд
        WebDriverWait(appium_driver, 10).until(EC.invisibility_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textTitle"]')))
        print("Надпись отсутствует на экране.")
    except TimeoutException:
        # Если элемент видим, то выбрасывается исключение, значит он всё же был найден
        print("Надпись всё ещё видна на экране.")

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

    check_text_not_present(appium_driver)