import requests
import time
import pyautogui
import re
import keyboard
import aspose.words as aw

from selenium import webdriver
from bs4 import BeautifulSoup
from keyboard import press
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def take_screenshot():
    driver = webdriver.Chrome("C:\\chromedriver.exe")

    url = "https://telegraph.bg/"
    driver.get(url)
    driver.maximize_window()
    time.sleep(8)

    driver.find_element(By.XPATH,'//button[@class="align-right secondary slidedown-button"]')\
        .click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH,'//button[@id="didomi-notice-agree-button"]')\
            .click()
    except:
        pass
    try:
        driver.find_element(By.XPATH,'//button[@id="didomi-notice-agree-button"]')\
            .click()
    except:
        pass
    time.sleep(10)
    try:
        driver.find_element(By.XPATH,'//span[@class="ad-TransitionClose"]')\
            .click()
    except:
        pass
    time.sleep(2)

    driver.find_element(By.XPATH,'//li[@class="nav-item d-block "]//a[contains(@href,"posledni")]')\
        .click()
    time.sleep(8)
    try:
        driver.find_element(By.XPATH,'//span[@class="ad-TransitionClose"]')\
            .click()
    except:
        pass
    time.sleep(2)

    firstfour = 0
    for i in range(1, 17):
        driver.save_screenshot(".\\Desktop\\news{}.jpeg".format(i))
        time.sleep(1)
        driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        firstfour += 1
        if firstfour > 3: break
    time.sleep(1)

    global secondURL
    secondURL = driver.current_url

def fetch_data():
    r = requests.get(secondURL)
    s = BeautifulSoup(r.content, "lxml")
    articles = s.find_all("h2", attrs={"class":"second-title"})
    count = 0
    document = open(".\\Desktop\\news.txt", "w")

    for article in articles:
        news = article.a.get("href")
        rNews = requests.get(news)
        sNews = BeautifulSoup(rNews.content, "lxml")
        linkContent = sNews.find_all("section", attrs={"class":"article-text"})
        headers = sNews.find_all("section", attrs={"class":"article-info"})

        for he in headers:
            t1 = he.h1.text
            title = t1.strip()
            count += 1
        if count > 4: break

        for content in linkContent:
            body = content.text.replace("0", "").replace("Сподели", "").strip()

        results = (str(news) + "\n\n" + str(title) + "\n" + "-"*74 + "\n" + str(body) + "\n\n" +  "#"*74 + "\n\n")
        document = open(".\\Desktop\\news.txt", "a", encoding="utf-8")
        document.write(results)

def convert_txt_docx():
    doc = aw.Document(".\\Desktop\\news.txt")
    doc.save(".\\Desktop\\newss.docx")

def send_mail():
    driver = webdriver.Chrome("C:\\chromedriver.exe")

    url = "https://www.abv.bg/"
    driver.get(url)

    driver.find_element(By.XPATH,'//input[@name="username"]')\
        .send_keys("tnrprjct@abv.bg")

    driver.find_element(By.XPATH,'//input[@name="password"]')\
        .send_keys("123456789ten")

    driver.find_element(By.XPATH,'//input[@id="loginBut"]')\
        .click()
    driver.maximize_window()
    time.sleep(4)

    driver.find_element(By.XPATH,'//div[@class="abv-button"]')\
        .click()
    time.sleep(2)

    driver.find_element(By.XPATH,'//*[@id="main"]/div/div[4]/div/div[4]/div/div[4]/div/div[2]/div/div[2]/div/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/input')\
        .send_keys("tnrprjct@abv.bg")
    press("enter")
    time.sleep(2)

    driver.find_element(By.XPATH,'//*[@id="main"]/div/div[4]/div/div[4]/div/div[4]/div/div[2]/div/div[2]/div/div[2]/div[1]/table/tbody/tr[5]/td[2]/div/input')\
        .send_keys("Telegraph: ss and first 4 news!")
    time.sleep(8)

    firstfour = 0
    for i in range(1,17):
        driver.find_element(By.XPATH,'//div[@class="sendFp1 abv-fileUpload"]').click()
        time.sleep(6)

        pyautogui.press('tab', presses=5)
        time.sleep(4)
        pyautogui.write('news{}'.format(i))
        time.sleep(4)
        pyautogui.press('tab', presses=4)
        time.sleep(4)
        pyautogui.write('news{}'.format(i))
        time.sleep(4)
        pyautogui.press('tab', presses=2)
        time.sleep(4)
        press('enter')
        time.sleep(7)
        firstfour += 1
        if firstfour > 3: break
    
    time.sleep(10)
    driver.find_element(By.XPATH,'//div[@class="sendFp1 abv-fileUpload"]').click()
    time.sleep(6)
    pyautogui.press('tab', presses=5)
    pyautogui.write('newss.docx')
    time.sleep(6)
    pyautogui.press('tab', presses=4)
    pyautogui.write('newss.docx')
    time.sleep(2)
    pyautogui.press('tab', presses=2)
    time.sleep(8)
    press('enter')
    time.sleep(4)

    driver.find_element(By.XPATH,'//*[@id="main"]/div/div[4]/div/div[4]/div/div[4]/div/div[2]/div/div[2]/div/div[2]/div[1]/table/tbody/tr[2]/td[2]/div/input')\
        .send_keys("tnrprjct@abv.bg")
    press("enter")
    time.sleep(2)

    driver.find_element(By.XPATH,'//div[@class="abv-button"]')\
        .click()
    time.sleep(2)

    driver.find_element(By.XPATH,'//td[@class="fr abv-arrdown abv-headerTriger"]')\
        .click()
    time.sleep(2)   

    driver.find_element(By.XPATH,'(//td[@class="gwt-MenuItem"])[3]')\
        .click()
    time.sleep(2)   

def all_functions():
    take_screenshot()
    fetch_data()
    convert_txt_docx()
    send_mail()
        
all_functions()