import random
import re
import time

from test_func import kur_test_func
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
test_func = kur_test_func(driver)
test_func.create_folder('C:/test')
f = open("C:/test/kurly_test_result.txt", 'w')
f.close()
folder = 'C:/test/'

def test_1():
    #랜덤 상품 장바구니 담기 확인
    try:
        f = open("C:/test/kurly_test_result.txt", 'a')
        f.write('KUR-1:랜덤 상품 장바구니 담기 확인\n')

        # 1.마켓컬리 홈페이지 이동
        url = 'https://www.kurly.com/'
        driver.get(url)

        # 2.GNB의 신상품 클릭
        clk_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='신상품']")))
        clk_button.click()
        b = driver.find_elements(By.XPATH,'//*[@id="__next"]/div[2]/div[1]/ul/li[2]')
        b.click()
        print('성공')
        time.sleep(10)

        # 3.임의의 상품 장바구니에 담기
        try:
            count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
            for number in range(1, count + 1):
                item_info = test_func.get_item(number)# 장바구니에 상품 담기
                item_name = item_info
                print('3번성공')

        # 4.장바구니 아이콘 클릭
                driver.find_element(By.CLASS_NAME,'css-ff2aah.e14oy6dx2').click()
        # 5.상품명 확인
                elements = driver.find_elements(By.CLASS_NAME,'css-efcx1u.esoayg86')
                for element in elements:            #실제 상품 명칭과 장바구니내 노출되는 상품 명칭 비교
                    if element.text == item_name:
                        result = (str(number)+'번 상품 PASS - '+item_info+'/')
                        f.write(result)
                    else:
                        result = (str(number) + '번 상품 Fail - ' + item_info + '/')
                        f.write(result)
                        return False

                clk_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='신상품']")))
                clk_button.click()          #신상품 페이지로 이동
            f.close()
            print('\ntest1 pass')
            return True
        finally: test_func.cart_screenshot(folder+'KUR-1')          #장바구니 내부 이미지 저장
    except: return False