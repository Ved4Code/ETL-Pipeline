from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from database.database_connect import DatabaseConnect

from scrapper.clean_data import cleandata
import pandas as pd
# Variables
url = 'https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails'

property_fields={
    'year_id': 'dbselect',
    'district_id': 'district_id',
    'taluka_id': 'taluka_id',
    'village_id':'village_id',
    'doc_property_id': 'free_text',
    'submit_button_id': 'submit',
    'no_of_records_id': 'tableparty_length'
    }

property_value={
    'year_value' : 30, # '2023'
    'district_value': 25, # Mumbai Suburbs
    'taluka_value': 1, # Andheri
    'village_value': 58, # Bandra
    'doc_property_id': '2023',
    'no_of_records_value': '50'
}

# print(property_fields.ye)


def openBrowser(url):
    '''
    @brief: Opens the browser and adds google translator extension
    @params: url
    '''
    options = webdriver.ChromeOptions()
    options.set_capability('unhandledPromptBehavior', 'accept')
    options.add_extension('utilities\\google_translate.crx') 
    prefs = {
    "translate_whitelists": {"hi":"en"},
    "translate":{"enabled":"true"}
    }
    options.add_experimental_option("prefs", prefs)
    print('Launching Browser...')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get(url)
    driver.implicitly_wait(10)
    return driver

def selectOption(driver, optionId, option):
    while True:
        select=Select(driver.find_element(By.ID, optionId))
        if len(select.options) > 1:
            select.select_by_index(option)
            break
        else:
            sleep(1)
        
def enterCaptcha(driver):
    enter_doc = driver.find_element(By.ID, 'cpatchaTextBox')
    enter_doc.send_keys("")

    while True:
        if len(enter_doc.get_attribute("value")) >=5:
            sleep(2)
            submit = driver.find_element(By.ID, "submit")
            submit.click()
            break
        else:
            sleep(1)

def scrollDown(driver):
    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    for i in range(1, total_height, 10):
        driver.execute_script("window.scrollTo(0, {});".format(i))
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    driver.execute_script("window.scrollTo(0, 0);")

def extractData(driver):
    table = []
    rows = driver.find_elements(By.TAG_NAME, 'tr')

    for i, row in enumerate(rows):
        data=[]
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells)==0:
            continue    
        for j, cell in enumerate(cells):
            print(j)
            if j<=7:
                data.append(cell.text)
            else:
                data.append(cell.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        print(data)
        table.append(data)
    
    return table

def storeDataToCSV(data):
    df = pd.DataFrame(data, columns = ['S_N', 'Document_no', 'Document_type', 'Document Office', 'Year', 'Will_write', 'Will_write_down', 'Other_Information', 'Link'])
    df.to_csv('scrapped_table.csv')

def insertIntoDatabase(data):
    db=DatabaseConnect()
    db.createTable()
    db.insertIntoTable(data)

def scrapeData():
    driver=openBrowser(url)

    selectOption(driver, property_fields['year_id'], property_value['year_value'])
    selectOption(driver, property_fields['district_id'], property_value['district_value'])
    selectOption(driver, property_fields['taluka_id'], property_value['taluka_value'])
    selectOption(driver, property_fields['village_id'], property_value['village_value'])
    
    enter_doc = driver.find_element(By.ID, 'free_text')
    enter_doc.send_keys("2023")

    enterCaptcha(driver)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.NAME, 'tableparty_length')))
    select=Select(driver.find_element(By.NAME, 'tableparty_length'))
    select.select_by_visible_text("50")

    try:
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//thead/tr/th[6]"), 'Will write'))
    except:
        sleep(10)
    
    scrollDown(driver)

    data=extractData(driver)
    storeDataToCSV(data)
    cleandata(data)
    insertIntoDatabase(data)
