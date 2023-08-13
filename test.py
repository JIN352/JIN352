from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# 비회원 구매 팝업 노출 확인
#1.네이버 이동
print('네이버 페이지 이동')
url = 'http://naver.com'
driver.get(url)

#2.쇼핑탭 이동
print('쇼핑탭 이동')
xpath = '//*[@id="shortcutArea"]/ul/li[4]'
element = driver.find_element(By.XPATH, xpath).click()

#3.임의의 상품 선택
print('상품페이지 이동')
time.sleep(10)
xpath = '//*[@id="gnb-header"]/div[4]/div[1]/div[2]/button[1]'
element = driver.find_element(By.XPATH, xpath).click()
print('test')
xpath = '//*[@id="content"]/div/div/div[4]/div/div[3]/ul/li[4]'
element = driver.find_element(By.XPATH, xpath).click()

#4.장바구니 버튼 클릭
print('장바구니버튼 클릭')
xpath = '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[10]/div[2]/div[3]'
element = driver.find_element(By.XPATH, xpath).click()

check = driver.switchto().alert().gettext()
print(check)





