from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
#options.add_argument("--headless")

PATH = "C:\WebDriver\bin\chromedriver.exe"
s = Service(PATH)

driver = webdriver.Chrome(service=s, options=options)

driver.get("https://lewatmana.com/lokasi/fasilitas-kesehatan/apotek/")


search = driver.find_element(By.XPATH, '//*[@id="poi-search-by-category-query"]')
search.send_keys("Farma")
search.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)
main = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[3]')))

print(main.text)

#print(driver.title)

#time.sleep(10)
driver.quit()