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

def nav_menu_documents(driver):
        menu_button =  WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ID, 'ru.adengi:id/nav_menu')))
        menu_button.click()

def menu_documets_link(driver):
        documents_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.XPATH,'//android.widget.TextView[@resource-id="ru.adengi:id/text" and @text="Документы"]')))
        documents_link.click()

def documents_download(driver):
    document_links = [
        "ИНН организации",
        "Информация для клиентов",
        "Памятка для потребителей СФУ",
        "Свидетельство МФО ООО МКК «А ДЕНЬГИ»",
        "Свидетельство ОГРН",
        "Свидетельство СРО ООО МКК «А ДЕНЬГИ»",
        "Структура и персональный состав органов управления ООО МКК «А ДЕНЬГИ»",
        "Общие условия договора потребительского займа",
        "Правила предоставления займов",
        "Базовый стандарт совершения МФО операций на финансовом рынке",
        "Базовый стандарт по управлению рисками",
        "Базовый стандарт защиты",
        "Устав",
        "Изменения в Устав",
        "Политика в отношении обработки персональных данных",
        "Политика в отношении использования пользовательских данных ООО МКК «А ДЕНЬГИ»",
        "Перечень лиц, которым могут передаваться персональные данные",
        "Меры поддержки военнослужащих",
        "Информация о страховщике",
        "Правила добровольного страхования жизни и здоровья",
        "Таблица №1 А_Правила",
        "Таблица №1 В_Правила",
        "Соглашение об использовании аналога собственноручной подписи",
        "Правила удаления аккаунта",
        "Оценка условий труда"
    ]

    for doc_text in document_links:
        while True:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.TextView[@text="{doc_text}"]'))
                )
                element.click()
                break
            except:
                driver.swipe(500, 1500, 500, 500, 800)
                time.sleep(1)


def check_downloaded_files():
    expected_files = [
        "certificate_inn.pdf",
        "financial_services_procedure_info.pdf",
        "consumer_memo_sfu.pdf",
        "certificate_mfo.pdf",
        "certificate_ogrn.pdf",
        "certificate_mir.pdf",
        "dopo_structure_and_composition.pdf",
        "loans_general_conditions.pdf",
        "loan_rules.pdf",
        "mfo_base_standard.pdf",
        "risk_management_base_standard.pdf",
        "security_base_standard.pdf",
        "standing_order.pdf",
        "changes_to_charter.pdf",
        "personal_data_policy.pdf",
        "personal_data_usage_policy.pdf",
        "personal_data_list_whom_transferred.pdf",
        "measures_to_support_military_personnel.pdf",
        "information_insurer.pdf",
        "rules_voluntary_insurance.pdf",
        "insurance_table_one_a.pdf",
        "insurance_table_one_b.pdf",
        "sed_mkk_selfie0804.pdf",
        "account_deletion_rules.pdf",
        "assessment_working_conditions.pdf"
    ]

    download_path = "/sdcard/Android/data/ru.adengi/files/Download/"


    timeout = 15
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = subprocess.run(["adb", "shell", "ls", download_path], capture_output=True, text=True)
        downloaded_files = result.stdout.splitlines()

        found_files = [file for file in expected_files if file in downloaded_files]
        missing_files = [file for file in expected_files if file not in downloaded_files]

        if not missing_files:
            print(f" Все файлы найдены: {found_files}")
            return

        time.sleep(2)


    if missing_files:
        pytest.fail(f" Не все файлы скачаны. Отсутствуют: {missing_files}")


#Тест онбординг
def test_onbording(driver):
    open_AMoney(driver)
    onbording(driver)

def test_menu_download_documents(driver):
    nav_menu_documents(driver)
    menu_documets_link(driver)
    documents_download(driver)
    check_downloaded_files()
