import requests
import time
import keyboard
import aspose.words as aw
import pyautogui

from bs4 import BeautifulSoup
from selenium import webdriver
from keyboard import press
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

count = 0
driver = webdriver.Chrome()

#take screenshot
def take_screenshot():
    url = "https://www.cars.bg/"
    driver.get(url)
    time.sleep(2)

    # coupe 
    driver.find_element(By.XPATH,'//*[@id="categorySelectSheetChip"]/span[2]')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="categorySelectSheet"]/div/div/form/div/label[3]/div/span')\
        .click()
    time.sleep(2)

    # make
    driver.find_element(By.XPATH,'//*[@id="brandSelectSheetChip"]/span[2]')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="brandsList"]/label[2]/div/span')\
        .click()
    time.sleep(2)

    # model
    driver.find_element(By.XPATH,'//*[@id="modelbutton"]/span[2]')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="modelsContainer"]/div/label[24]/div/span')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="modelSelectSheet"]/div/button')\
        .click()
    time.sleep(2)

    # electrical
    driver.find_element(By.XPATH,'//*[@id="fuelSelectSheetChip"]/span[2]')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="fuelSelectSheet"]/div/div/form/div/label[7]/div/span')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="fuelSelectSheet"]/div/button')\
        .click()
    time.sleep(2)

    # automatic
    driver.find_element(By.XPATH,'//*[@id="gearSelectSheetChip"]/span[2]')\
        .click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="gearSelectSheet"]/div/div/form/div/label[3]/div/span')\
        .click()
    time.sleep(2)

    driver.maximize_window()
    time.sleep(4)

    # take screenshot
    for i in range(1,6):
        driver.save_screenshot(".\\Desktop\\cars{}.jpeg".format(i))
        time.sleep(1)
        driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    
    global secondURL
    secondURL = driver.current_url

#download data from the secondURL
def fetch_data_cars():
    r = requests.get(secondURL)
    soup = BeautifulSoup(r.content, "lxml")
    cars = soup.find_all("div", attrs={"class": "mdc-card__primary-action"})
    count = 0
    document = open(".\\Desktop\\resultCars.txt", "w", encoding="utf-8")

    for car in cars:
        carLink = car.a.get("list-link")
        rCar = requests.get(carLink)       
        soupCar = BeautifulSoup(rCar.content, "lxml")
        properties = soupCar.find_all("div", attrs={"class","mdc-top-app-bar--fixed-adjust"})
        for properti in properties:
            make = properti.find("div", attrs={"style":"float:left; font-size: 1.5em; padding-top: 3px;"}).h2.text.replace(" ", "")
            try:
                extras = properti.find("div", attrs={"class":"description text-copy"}).div.text.replace(" ", "")
                " ".join(extras.split())
            except:
                pass
            price = properti.find("div", attrs={"class":"offer-price"}).strong.text.replace(" ", "")
            contact = properti.find("table", attrs={"cellspacing":"2"}).find("td", attrs={"valign":"top"}).text.replace(" ", "")
            count += 1
            if count > 4: break
            time.sleep(6)

        results = ("#"*148 + "\n" + str(count) + "." +str(make) + "\n" + str(carLink) + "\n" + "-"*74 + "\n" + str(extras) + "\n" + "*"*15 + "\n" + "Цена: " + str(price) + "\n" + "*"*15 + "\n" + str(contact) + "\n")
        document = open(".\\Desktop\\resultCars.txt", "a", encoding="utf-8")
        document.write(results)


#convert txt to docx
def convert_txt_docx():
    doc = aw.Document(".\\Desktop\\resultCars.txt")
    doc.save(".\\Desktop\\resultCars2.docx")

#send screenshot and file to me as a mail
def mail_screenshot_and_data():
    driver.get('https://www.abv.bg/')
    driver.maximize_window()
    driver.find_element(By.XPATH, '//input[@id="username"]').send_keys('tnrprjct@abv.bg')
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys('123456789ten')
    driver.find_element(By.XPATH, '//input[@id="loginBut"]').click()
    time.sleep(8)

    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[4]/div/div[4]/div/div[2]/div/div[2]/div/div[3]/div').click()
    time.sleep(4)
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[4]/div/div[4]/div/div[4]/div/div[2]/div/div[2]/div/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/input')\
        .send_keys('tnrprjct@abv.bg')
    time.sleep(4)
    pyautogui.press('enter', presses=2)
    time.sleep(4)

    driver.find_element(By.XPATH, '//iframe[@class="gwt-RichTextArea"]').send_keys('Screenshot and file - OK')
    time.sleep(4)
    driver.find_element(By.XPATH, '//input[@class="gwt-TextBox"]')\
        .send_keys('Cars')
    time.sleep(4)

    for i in range(1, 5):
        driver.find_element(By.XPATH, '//div[@class="sendFp1 abv-fileUpload"]').click()
        time.sleep(6)
        pyautogui.press('tab', presses=5)
        keyboard.write('cars{}.jpeg'.format(i))           
        time.sleep(5)
        pyautogui.press('tab', presses=4)
        time.sleep(5)
        keyboard.write('cars{}'.format(i))
        time.sleep(5)
        pyautogui.press('tab', presses=2)
        press('enter')
        time.sleep(7)

    time.sleep(10)
    driver.find_element(By.XPATH, '//div[@class="sendFp1 abv-fileUpload"]').click()
    time.sleep(4)
    keyboard.write('resultCars2')
    time.sleep(4)
    press('enter')  
    time.sleep(8)

    driver.find_element(By.XPATH, '//div[@class="abv-button"]').click()
    time.sleep(8)

    driver.find_element(By.XPATH, '//td[@class="fr abv-arrdown abv-headerTriger"]').click()
    time.sleep(2)

    driver.find_element(By.XPATH, '(//div[@class="commonMenuDropdown"]//td[@class="gwt-MenuItem"])[2]').click()
    time.sleep(20)

    driver.close()

def all_functions():
    take_screenshot()
    fetch_data_cars()
    convert_txt_docx()
    mail_screenshot_and_data()

all_functions()