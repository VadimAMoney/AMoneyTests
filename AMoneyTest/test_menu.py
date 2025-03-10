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
#"appPackage": "com.android.documentsui",  # Пакет приложения "Files" на Android
    #"appActivity": ".DownloadsActivity",


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

def test_nav_menu_documents(driver):
    menu_button = driver.find_element(by=AppiumBy.ID, value= 'ru.adengi:id/nav_menu')
    menu_button.click()

def test_menu_documets_link(driver):
    documents_link = driver.find_element(by=AppiumBy.XPATH, value= '//android.widget.TextView[@resource-id="ru.adengi:id/text" and @text="Документы"]')
    documents_link.click()




def test_download_documents(driver):

    certificate_inn = driver.find_element(
        by=AppiumBy.ANDROID_UIAUTOMATOR,
        value='new UiSelector().text("ИНН организации")'
    )
    certificate_inn.click()


    financial_services_procedure_info = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Информация для клиентов"]'
    )
    financial_services_procedure_info.click()


    consumer_memo_sfu = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Памятка для потребителей СФУ"]'
    )
    consumer_memo_sfu.click()

    certificate_mfo = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Свидетельство МФО ООО МКК «А ДЕНЬГИ»"]'
    )
    certificate_mfo.click()

    certificate_ogrn = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Свидетельство ОГРН"]'
    )
    certificate_ogrn.click()

    certificate_mir = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Свидетельство СРО ООО МКК «А ДЕНЬГИ»"]'
    )
    certificate_mir.click()

    dopo_structure_and_composition = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Структура и персональный состав органов управления ООО МКК «А ДЕНЬГИ»"]'
    )
    dopo_structure_and_composition.click()

    loans_general_conditions = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Общие условия договора потребительского займа"]'
    )
    loans_general_conditions.click()

    loan_rules = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Правила предоставления займов"]'
    )
    loan_rules.click()


    mfo_base_standart = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Базовый стандарт совершения МФО операций на финансовом рынке"]'
    )
    mfo_base_standart.click()


    risk_management_base_standard = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Базовый стандарт по управлению рисками"]'
    )
    risk_management_base_standard.click()


def test_scroll_down(driver):
    driver.swipe(500, 1500, 500, -400, 1000)  # (start_x, start_y, end_x, end_y, duration)

def test_download_documents_second(driver):

    security_base_standard = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Базовый стандарт защиты"]'
    )
    security_base_standard.click()

    standing_order = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Устав"]'
    )
    standing_order.click()

    changes_to_charter = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Изменения в Устав"]'
    )
    changes_to_charter.click()

    personal_data_policy = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Политика в отношении обработки персональных данных"]'
    )
    personal_data_policy.click()

    personal_data_usage_policy = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Политика в отношении использования пользовательских данных ООО МКК «А ДЕНЬГИ»"]'
    )
    personal_data_usage_policy.click()

    personal_data_list_whom_transferred = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Перечень лиц, которым могут передаваться персональные данные"]'
    )
    personal_data_list_whom_transferred.click()

    measures_to_support_military_personnel = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Меры поддержки военнослужащих"]'
    )
    measures_to_support_military_personnel.click()

    information_insurer = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Информация о страховщике"]'
    )
    information_insurer.click()

    rules_voluntary_insurance = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Правила добровольного страхования жизни и здоровья"]'
    )
    rules_voluntary_insurance.click()

    insurance_table_one_a = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Таблица №1 А_Правила"]'
    )
    insurance_table_one_a.click()

def test_scroll(driver):
    driver.swipe(500, 1500, 500, -600, 100)  # (start_x, start_y, end_x, end_y, duration)

def test_download_documents_third(driver):
    insurance_table_one_b = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Таблица №1 В_Правила"]'
    )
    insurance_table_one_b.click()

    sed_mkk_selfie0804 = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Соглашение об использовании аналога собственноручной подписи"]'
    )
    sed_mkk_selfie0804.click()

    account_deletion_rules = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Правила удаления аккаунта"]'
    )
    account_deletion_rules.click()

    assessment_working_conditions = driver.find_element(
        by=AppiumBy.XPATH,
        value='//android.widget.TextView[@text="Оценка условий труда"]'
    )
    assessment_working_conditions.click()


def test_check_downloaded_files():
    time.sleep(3)
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


    result = subprocess.run(["adb", "shell", "ls", download_path], capture_output=True, text=True)
    downloaded_files = result.stdout.splitlines()

    found_files = [file for file in expected_files if file in downloaded_files]
    missing_files = [file for file in expected_files if file not in downloaded_files]

    assert found_files, f"Ошибка! Не найдено ни одного файла из ожидаемых: {expected_files}"

    if missing_files:
        print(f" Предупреждение! Не все файлы скачаны. Отсутствуют: {missing_files}")
    else:
        print(f" Все файлы найдены: {found_files}")
