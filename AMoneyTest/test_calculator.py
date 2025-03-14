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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.DEBUG)

apk_path = "C:\\Users\\hets4\\adengi\\adengi-dev-1.0.28.5-webview-off.apk"
appium_server_url = "http://localhost:4723"
app_name = 'А деньги'
TEXT_FIELD_PXOME = "ru.adengi:id/editTextPhone"
element = "ru.adengi:id/editTextCity"
xpath_cc = '//android.widget.EditText[@resource-id="cc"]'
xpath_number = '//android.view.View[@resource-id="paymentType1"]/android.view.View[1]/android.view.View[1]/android.widget.EditText'
text_field = "4444555566661111"
xpath_cvv = '//android.widget.EditText[@resource-id="cvc"]'
text_cvv = "123"


@pytest.fixture(scope="session")
def appium_driver():
    """Фикстура для инициализации и закрытия драйвера Appium."""
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='emulator-5554',
        language='ru',
        locale='RU',
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

import pytest
from appium import webdriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "appPackage": "your.app.package",
        "appActivity": "your.app.activity",
        "automationName": "UiAutomator2"
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()


def slider_and_text_match(appium_driver):
    wait = WebDriverWait(appium_driver, 10)

    # Выбираем именно SeekBar (ползунок), исключая ProgressBar
    slider = wait.until(EC.presence_of_element_located((
        By.XPATH, '//android.widget.SeekBar[@content-desc and contains(@content-desc, "Value")]'
    )))

    text_element = wait.until(EC.presence_of_element_located((
        By.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textReturnSumDiscounted"]'
    )))

    min_value = 2000
    max_value = 30000
    step = 500
    num_steps = (max_value - min_value) // step

    start_x = slider.location['x']
    start_y = slider.location['y']
    width = slider.size['width']

    # Округляем шаг, чтобы избежать дробных значений
    step_size = round(width / num_steps)  # Длина одного шага (округлено)

    # Выводим отладочную информацию
    print(f"DEBUG: slider width = {width}, num_steps = {num_steps}")
    print(f"DEBUG: step_size = {step_size}")

    # Получаем текущее значение ползунка
    content_desc = slider.get_attribute("content-desc")
    print(f"DEBUG: content-desc = {content_desc}")

    if not content_desc or content_desc.lower() == "null":
        raise ValueError("Ошибка: content-desc отсутствует или пустой!")

    try:
        current_value = int(content_desc.split(", ")[1])
    except (IndexError, ValueError):
        raise ValueError(f"Ошибка: не удалось извлечь число из content-desc. Получено: {content_desc}")

    print(f"DEBUG: Current value = {current_value}")

    # Двигаем ползунок к минимальному значению, если он не на 2000
    if current_value != min_value:
        actions = ActionChains(appium_driver)
        actions.drag_and_drop_by_offset(slider, -450, 0).perform()
        appium_driver.implicitly_wait(1)

        content_desc = slider.get_attribute("content-desc")
        try:
            current_value = int(content_desc.split(", ")[1])
        except (IndexError, ValueError):
            current_value = int(content_desc)

        assert current_value == min_value, f"Expected 2000, but got {current_value}"

    # Двигаем ползунок вперед по пикселям с проверкой
    move_by_pixels = 8  # Уменьшаем смещение на 10 пикселей за шаг для точности

    for i in range(num_steps):
        # Получаем текущие координаты ползунка
        current_x = slider.location['x']
        print(f"DEBUG: Текущее положение ползунка по X = {current_x}")

        # Передвигаем ползунок на move_by_pixels пикселей вправо
        actions = ActionChains(appium_driver)
        actions.click_and_hold(slider).move_by_offset(move_by_pixels, 0).release().perform()
        time.sleep(0.5)  # Даем UI обновиться

        # Получаем новое значение
        content_desc = slider.get_attribute("content-desc")
        try:
            current_value = int(content_desc.split(", ")[1])
        except (IndexError, ValueError):
            current_value = int(content_desc)

        print(f"DEBUG: Текущее значение ползунка = {current_value}")

        # Проверяем, что значение правильное
        expected_value = min_value + step * (i + 1)
        print(f"DEBUG: Ожидаемое значение = {expected_value}")

        # Проверка с допустимым отклонением
        assert abs(current_value - expected_value) <= step, f"Expected {expected_value}, but got {current_value}"

# Тест 1. Регистрация
def test_field_value_edit(appium_driver):
    wait = WebDriverWait(appium_driver, 10)

    # 1. Клики
    click_button_by_id(appium_driver, "ru.adengi:id/buttonSkip")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonNext")
    click_button_by_id(appium_driver, "ru.adengi:id/acceptButton")
    click_button_by_id(appium_driver, "com.android.permissioncontroller:id/permission_allow_button")
    slider_and_text_match(appium_driver)
    click_button_by_id(appium_driver, "ru.adengi:id/buttonGetMoney")
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

    # Удалить приложение
    delete_app(appium_driver)


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

    # Тест 5. Идентификация по СНИЛС


def test_snils(appium_driver):
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
    click_button_by_id(appium_driver, "ru.adengi:id/buttonAction")

    # Выбираем метот Индификации по СНИЛСу
    click_button_by_id(appium_driver, "ru.adengi:id/buttonIdentificationMethod")

    # 2. Проверяем поля ввода для СНИЛС

    snils_birth_id = 'ru.adengi:id/editSnilsNumber'
    snils_birth = wait.until(EC.presence_of_element_located((AppiumBy.ID, snils_birth_id)))
    snils_birth.click()

    snils_birth_text = snils_birth.text
    snils_birth.clear()
    snils_birth.send_keys(snils_birth_text)

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")

    text = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@text="Получение денег"])')))

    # 3. Проверяем переход на следующий этап

    print(text.text)
    if text.text == 'Получение денег':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')
        # Вернуться на главный экран
    go_to_home(appium_driver)

    # Удалить приложение
    delete_app(appium_driver)

    # Тест 6. Получение денег


def test_take(appium_driver):
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
    click_button_by_id(appium_driver, "ru.adengi:id/buttonAction")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonIdentificationMethod")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")
    click_button_by_id(appium_driver, "ru.adengi:id/buttonAdd")

    wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@text="Номер карты"]')))
    swipe_bottom_to_top(appium_driver)

    # 2. Ввод номера карты

    wait = WebDriverWait(appium_driver, 10)

    # 1. Номер карты

    field_сс = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="cc"]')))
    field_сс.click()

    xpath_cc = '//android.widget.EditText[@resource-id="cc"]'
    text_field = "4444555566661111"
    type_text_by_xpath(appium_driver, xpath_cc, text_field)

    # 2. Месяц

    field_month = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="month"]')))
    field_month.click()
    appium_driver.press_keycode(8)
    appium_driver.press_keycode(8)

    # 3. Год

    field_year = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="year"]')))
    field_year.click()
    appium_driver.press_keycode(9)
    appium_driver.press_keycode(12)

    # 4. CVV

    field_cvv = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="cvc"]')))
    field_cvv.click()

    xpath_cvv = '//android.widget.EditText[@resource-id="cvc"]'
    text_cvv = "123"
    type_text_by_xpath(appium_driver, xpath_cvv, text_cvv)

    # 5. Кнопка "Продолжить"

    button_next = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="Продолжить"]')))
    button_next.click()

    # 6. Проверяем прикрепление карты

    text = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ru.adengi:id/textTitle"]')))

    print(text.text)
    if text.text == 'Карта успешно прикреплена':
        print('Тест пройдет успешно')
    else:
        print('Тест упал')

    click_button_by_id(appium_driver, "ru.adengi:id/buttonContinue")

    go_to_home(appium_driver)

    # Удалить приложение
    delete_app(appium_driver)
