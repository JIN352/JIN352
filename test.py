import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
number=0

# 랜덤 상품 장바구니 담기 확인
#1.브라우저 연결
print('브라우저 연결')
url = 'https://ohou.se/'
driver.get(url)
#driver.maximize_window()

#2.쇼핑탭 이동
print('쇼핑탭 이동')
xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
element = driver.find_element(By.XPATH, xpath).click()

#3.임의의 상품 선택
for number in range(5):

    print('상품페이지 이동'+str(number))
    itemlist = ['1244849','1297593','1502238','767440','1450530','1918219']
    item = random.choice(itemlist)
    url = 'https://ohou.se/productions/'+ item
    driver.get(url)
    xpath = '/html/body/div[1]/div'
    itemname = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute('production-selling-header__title__name')

    #4.장바구니 버튼 클릭
    print('장바구니버튼 클릭')
    xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
    element = driver.find_element(By.XPATH, xpath).click()
    time.sleep(3)

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div/select'
        element = driver.find_element(By.XPATH, xpath)
        element.select_by_value('1')
        time.sleep(10)

    except: pass

time.sleep(15)


# xpath = '/html/body/div[5]/div/div/div/div/div[1]/h2'
# element = driver.find_element(By.XPATH, xpath).text()
# print(element)





