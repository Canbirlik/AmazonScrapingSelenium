import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sqlite3

webpage = "https://www.amazon.com.tr/"

# Store DB Func
def store_db(product_name, product_price):
    conn = sqlite3.connect('amazon_search.db')
    curr = conn.cursor()

    # create table
    curr.execute(
        '''CREATE TABLE IF NOT EXISTS search_result (name text, price real)''')
    # insert data into a table
    curr.executemany(
        "INSERT INTO search_result (name, price) VALUES (?,?)",
        list(zip(product_name, product_price)))
    conn.commit()
    conn.close()

def amazon_multi_search(keyword, max_pages):
    # Web sürücüsünü başlat
    page_number = 1
    next_page = ""
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Amazon.com.tr adresine gidin
    driver.get(webpage)

    # Arama kutusunu bulun ve bir ürün araması yapın (örneğin, "iPhone")
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)

    while page_number <= max_pages:
        # Sayfa yüklenene kadar birkaç saniye bekleyin
        items = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "sg-col-inner")]')))

        # Ürün fiyatlarını çekin
        product_price = []
        product_name = []

        for item in items:
            whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
            fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
            name = item.find_elements(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')

            if whole_price != [] and fraction_price != []:
                price = '.'.join([whole_price[0].text, fraction_price[0].text])
                product_unit = ''.join(name[0].text)
            else:
                price = 0
                product_unit = ""

            product_price.append(price)
            product_name.append(product_unit)

        page_number += 1
        next_page = webpage + "s?k=" + keyword + "&page=" + str(page_number)
        
        

        print(next_page)
        store_db(product_name, product_price)

        driver.get(next_page)
      

    # Web sürücüsünü kapat
    driver.quit()


keyword = input("Aramak istediğiniz kelime nedir? ")
max_pages = int(input("Max. kaç sayfayı tarayalım? "))

amazon_multi_search(keyword, max_pages)