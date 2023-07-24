from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(r"C:\Users\Thomas Stefen M\Dropbox\My PC (LAPTOP-VVOKBOQQ)\Documents\All about me\Kalbe Internship\Data\Selenium\extension_5_8_0_0.crx")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://id.wikipedia.org/wiki/Daftar_rumah_sakit_di_Indonesia")

time.sleep(10)

titles = driver.find_elements(By.CLASS_NAME, "mw-headline")
for title in titles:
    print(title.text)

driver.quit()