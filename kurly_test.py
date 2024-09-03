import random
import re
import time

from test_func import Kur_test_func
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
mobile_emulation = {"deviceName": "iPhone XR"}
options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(options=options)
test_func = Kur_test_func(driver)
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
        check_item = []

        # 1.마켓컬리 홈페이지 이동
        url = 'https://www.kurly.com/'
        driver.get(url)
        driver.maximize_window()
        while True:
            try:
                driver.find_element(By.XPATH, "//*[text()='닫기']").click()
            except NoSuchElementException:                               # "닫기" 문구를 포함한 요소가 더 이상 없을 때 루프 종료
                break

        # 2.GNB의 신상품 클릭
        clk_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='신상품']")))
        clk_button.click()

        # 3.임의의 상품 장바구니에 담기
        try:
            count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
            for number in range(1, count + 1):
                item = test_func.get_item(number) # 장바구니에 상품 담기
                item_info.append(item)
                driver.find_element(By.XPATH, "//*[text()='계속 쇼핑하기']").click()
                driver.refresh()

    # 4.장바구니 페이지로 이동
            driver.find_element(By.CLASS_NAME, 'css-1ukhbex.e10bpect1').click()
            WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.ID, 'kurlyDelivery')))

    # 5.상품명 확인
            for number in range(1, count + 1):
                loc_item = driver.find_elements(By.CLASS_NAME, 'css-1bti31.ersep5u0')[number-1]      #장바구니에 담긴 상품 확인
                check_number = loc_item.get_attribute('href')                                       #상품 url 추출
                check_number = re.sub(r'[^0-9]', '', check_number)
                try: check_name = loc_item.find_element(By.XPATH,'./p[2]').text                     #상품명 추출
                except: check_name = loc_item.find_element(By.XPATH,'./p').text
                check_item.append((check_number,check_name))
            item_info.sort()
            check_item.sort()

            if check_item == item_info :
                result = ('PASS\n장바구니에 담긴 상품들:\n' + str(check_item) + '\n실제 담은 상품들:\n' + str(item_info))
                f.write(result)
            else:
                result = ('FAIL\n장바구니에 담긴 상품들:\n'+ str(check_item) +'\n실제 담은 상품들:\n'+ str(item_info))
                f.write(result)
                return False
            f.close()
            print('\ntest1 pass')
            return True
        finally: test_func.cart_screenshot(folder+'KUR-1')          #장바구니 내부 이미지 저장
    except: return False