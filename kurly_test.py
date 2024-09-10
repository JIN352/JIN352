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
                result = ('PASS\n장바구니에 담긴 상품들:\n' + str(check_item) + '\n실제 담은 상품들:\n' + str(item_info)+'\n\n')
                f.write(result)
            else:
                result = ('FAIL\n장바구니에 담긴 상품들:\n'+ str(check_item) +'\n실제 담은 상품들:\n'+ str(item_info)+'\n\n')
                f.write(result)
                return False
            f.close()
            print('\ntest1 pass')
            return True
        finally: test_func.cart_screenshot(folder+'KUR-1')          #장바구니 내부 이미지 저장
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def test_2():
    #찜하기 버튼을 통한 로그인 페이지 이동 확인
    try:
        test_func.create_folder('C:/test/KUR-2')
        f = open("C:/test/kurly_test_result.txt", 'a')
        f.write('KUR-2:찜하기 버튼을 통한 로그인 페이지 이동 확인\n')

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

        # 3.임의의 상품 페이지로 이동
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'css-1ao2hqp.e9lsuol7'))).click()

    # 4.찜하기 버튼 클릭
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-18dergt.ei3x04a1'))).click()

    # 5.로그인 필요 팝업 확인
            time.sleep(2)
            driver.save_screenshot(folder+'KUR-2/POPUP.png')                #로그인 필요 팝업 이미지 저장
            driver.find_element(By.XPATH,"//*[text()='확인']").click()

    # 6.로그인 페이지로 이동 확인
            time.sleep(2)
            id_element = driver.find_element(By.NAME,'id').get_attribute('placeholder')
            pw_element = driver.find_element(By.NAME,'password').get_attribute('placeholder')
            if id_element == '아이디 입력':
                if pw_element == '비밀번호 입력':
                    result = ('PASS - 로그인 페이지 노출\n\n')
                    f.write(result)
            else:
                result = ('FAIL - 로그인 페이지 미노출, 마지막 페이지 확인 필요\n\n')
                f.write(result)
                return False
            f.close()
            print('\ntest2 pass')
            return True
        finally: driver.save_screenshot(folder+'KUR-2/KUR-2.png')          #로그인 페이지 이미지 저장
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def test_3():
    #배송지 설정 확인
    try:
        test_func.create_folder('C:/test/KUR-3')
        f = open("C:/test/kurly_test_result.txt", 'a')
        f.write('KUR-3:배송지 설정 확인\n')

        # 1.마켓컬리 홈페이지 이동
        url = 'https://www.kurly.com/'
        driver.get(url)
        driver.maximize_window()
        while True:
            try:
                driver.find_element(By.XPATH, "//*[text()='닫기']").click()
            except NoSuchElementException:                               # "닫기" 문구를 포함한 요소가 더 이상 없을 때 루프 종료
                break

        # 2.배송지 등록 버튼 클릭
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-x4ul3l.eue6tj11'))).click()

        # 3.주소지 입력
            test_func.such_post('성남시청')          #프레임 이동 및 주소검색(검색할 주소 입력)

        # 4.주소지 선택
            driver.find_elements(By.CLASS_NAME, 'link_post')[2].send_keys(Keys.ENTER)

        # 5.저장 버튼 클릭
            time.sleep(2)
            driver.switch_to.default_content()  # 메인프레임으로 이동
            location = driver.find_element(By.ID,'addressDetail')
            location.send_keys(Keys.ENTER+'test')                   #나머지 주소 입력
            location = location.find_element(By.XPATH,'./../../label').text
            driver.find_element(By.XPATH,"//*[text()='저장']").click()
            location = location+(' test')       #설정한 주소 값

        # 6.배송지 등록 버튼 클릭
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-x4ul3l.eue6tj11'))).click()

        # 7.등록된 배송지 확인
            time.sleep(2)
            location_popup = driver.find_element(By.XPATH,"//*[contains(text(), '성남시청')]").text
            if location_popup == location:
                result = ('PASS - 입력한 배송지로 설정 성공: '+location+'\n\n')
                f.write(result)
            else:
                result = ('FAIL - 배송지 설정 확인 필요\n\n')
                f.write(result)
                return False
            f.close()
            print('\ntest3 pass')
            return True
        finally: driver.save_screenshot(folder+'KUR-3/KUR-3.png')          #로그인 페이지 이미지 저장
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def test_4():
    #주소지에 따른 샛별, 하루 배송 노출 확인
    try:
        test_func.create_folder('C:/test/KUR-4')
        f = open("C:/test/kurly_test_result.txt", 'a')
        f.write('KUR-4: 주소지에 따른 샛별, 하루 배송 노출 확인\n')
        such_location = {'성남시청':'샛별배송','광주광역시청':'하루배송'}

        # 1.마켓컬리 홈페이지 이동
        driver.delete_all_cookies()
        url = 'https://www.kurly.com/'
        driver.get(url)
        driver.maximize_window()
        while True:
            try:
                driver.find_element(By.XPATH, "//*[text()='닫기']").click()
            except NoSuchElementException:  # "닫기" 문구를 포함한 요소가 더 이상 없을 때 루프 종료
                break
        # 2.배송지 등록 버튼 클릭
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-x4ul3l.eue6tj11'))).click()

        for i in such_location:             #샛별배송, 하루배송 각각 확인을 위한 반복
            try:
                # 3.주소지 입력
                test_func.such_post(i)  # 프레임 이동 및 주소검색(검색할 주소 입력)

                # 4.주소지 선택
                driver.find_elements(By.CLASS_NAME, 'link_post')[2].send_keys(Keys.ENTER)

                # 5.노출되는 배송 타입 확인
                time.sleep(2)
                driver.switch_to.default_content()  # 메인프레임으로 이동
                driver.find_element(By.ID, 'addressDetail').send_keys(Keys.ENTER + 'test')  # 나머지 주소 입력
                driver.save_screenshot(folder + 'KUR-4/' + such_location[i] + '_' + i + '.png')  # 배송지 이미지 저장

                # 6.저장 버튼 클릭
                driver.find_element(By.XPATH, "//*[text()='저장']").click()

                # 7.배송지 등록 버튼 클릭
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-x4ul3l.eue6tj11'))).click()

                # 8.노출되는 배송 타입 확인
                time.sleep(2)
                location_popup = driver.find_element(By.CLASS_NAME, 'css-1wim3xg.e1kt0drt1')
                location_popup = location_popup.find_element(By.XPATH,'./../strong').text       #설정된 배송지에서 배송 타입 확인
                if such_location[i] == location_popup:
                    result = ('[PASS '+such_location[i]+'_'+i+']\n\n')
                    f.write(result)
                else:
                    result = ('[FAIL '+such_location[i]+'_'+i+']\n\n')
                    f.write(result)
                    return False
            finally:
                driver.save_screenshot(folder + 'KUR-4/KUR-4' + such_location[i] + '_' + i + '.png')  # 이미지 저장
                driver.find_element(By.XPATH,"//*[text()='배송지 변경']").click()
        f.close()
        print('\ntest4 pass')
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
