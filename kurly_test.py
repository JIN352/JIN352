import random
import re
import time

from test_func import kur_test_func
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
mobile_emulation = {"deviceName": "iPhone XR"}
options.add_experimental_option("mobileEmulation", mobile_emulation)
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
        item_info = []

        # 1.마켓컬리 홈페이지 이동
        url = 'https://www.kurly.com/'
        driver.get(url)
        driver.maximize_window()
        while True:
            try:
                driver.find_element(By.XPATH, f"//*[text()='닫기']").click()
            except NoSuchElementException:                               # "닫기" 문구를 포함한 요소가 더 이상 없을 때 루프 종료
                break

        # 2.GNB의 신상품 클릭
        clk_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='신상품']")))
        clk_button.click()

        # 3.임의의 상품 장바구니에 담기
        try:
            count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
            print(count)
            for number in range(1, count + 1):
                item = test_func.get_item(number) # 장바구니에 상품 담기
                item_info.append(item)
                driver.find_element(By.XPATH, f"//*[text()='계속 쇼핑하기']").click()
                driver.refresh()
                #print(item_info)

    # 4.장바구니 페이지로 이동
            print(item_info)
            driver.find_element(By.XPATH, f"//*[text()='장바구니 확인']").click()
            time.sleep(2)
    # 5.상품명 확인
            parent_element = driver.find_element(By.ID,'kurlyDelivery')
            parent_element = parent_element.find_element(By.XPATH,'./../div[2]')
            child_elements = parent_element.find_elements(By.XPATH,'./*')
            number_of_children = len(child_elements)
            print(number_of_children)
            elements = driver.find_elements(By.CLASS_NAME,'css-efcx1u.esoayg86')
            for element in elements:            #실제 상품 명칭과 장바구니내 노출되는 상품 명칭 비교
                if element.text == item_info:
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