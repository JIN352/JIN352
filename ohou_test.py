import random
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
result =[]
f = open("C:/test/ohou_test_result.txt", 'w')
f.close()


def test_1():
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('OHO-1\n')

    # 랜덤 상품 장바구니 담기 확인
    #1.브라우저 열기
    print('브라우저 연결')
    url = 'https://ohou.se/'
    driver.get(url)

    #2.쇼핑탭 이동
    print('쇼핑탭 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element = driver.find_element(By.XPATH, xpath).click()

    #3.임의의 상품 선택
    for number in range(1, 8):

        print(str(number)+'번 상품페이지 이동')
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        item = re.findall(r'\d+', element)
        driver.get(element)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/div/span'
        itemname = driver.find_element(By.XPATH, xpath).text
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/p/a'
        element = driver.find_element(By.XPATH, xpath).text
        baner = '[' + element + '] '
        itemname = baner+itemname


        #4.장바구니 버튼 클릭
        print('장바구니버튼 클릭')
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('0')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('0')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('0')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert.accept()
                        select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/ul/li[1]/article/label/div'
                        element = driver.find_element(By.XPATH, select_xpath).send_keys('test')

                    except:
                        pass

                except:
                    pass

            except: pass

        except: pass

        #5.장바구니 이동
        print('장바구니 이동')
        xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
        element = driver.find_element(By.XPATH, xpath).click()

        #6.상품 확인
        print('상품 확인')
        driver.implicitly_wait(3)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li[1]/article/ul/li/article/ul/li/article/a/div[2]/h1'
        element = driver.find_element(By.XPATH, xpath).text
        if element == itemname:
            result = '[상품번호'+str(item)+' Pass]'
        else:
            result = '[상품번호'+str(item)+' Fail]'

        xpath = '/html/body/div[1]/div/div/header/div/div/div/div[3]/a[2]'
        element = driver.find_element(By.XPATH, xpath).click()
        f.write(result)

    f.close()

def test_2():
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\nOHO-2\n')
    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    print('브라우저 연결')
    url = 'https://ohou.se/'
    driver.get(url)

    #2.쇼핑탭 이동
    print('쇼핑탭 이동')
    xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    #3.임의의 상품 장바구니에 담기
    print('상품 장바구니에 담기')
    count = random.randrange(2, 7)
    for number in range(1, count+1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        item = re.findall(r'\d+', element)
        driver.get(element)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('0')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('0')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('0')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert.accept()
                        select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/ul/li[1]/article/label/div'
                        element = driver.find_element(By.XPATH, select_xpath).send_keys('test')

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            pass

        element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    #4.장바구니로 이동
    print('장바구니 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    element = driver.find_element(By.XPATH, xpath).click()

    # 5.장바구니에 담긴 상품 수 확인
    print('장바구니에 담긴 상품 수 확인')
    driver.refresh()
    xpath_s = '/html/body/div[1]/div/div/header/div/div/div/div[4]/div/a/span[2]'
    element_s = driver.find_element(By.XPATH, xpath_s).text
    count_s = str(count)
    if count_s == element_s:
        f.write('최초 상품 갯수' + count_s + '\n')
    else:
        f.write('Faill - 장바구니에 담긴 상품 수 확인\n')
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니에 표시된 숫자: ' + element_s+'\n')

    #6.상품 삭제
    if count < 4:
        number_del = 1 or 2
    else:
        number_del = random.randrange(2, count-1)
    print(str(number_del)+'개 상품 삭제')
    element = driver.find_elements(By.CLASS_NAME,'_3UImz')
    for a in range(1,number_del+1):
        item_index = element[a]
        item_index.click()
    element = driver.find_element(By.XPATH,'//button[contains(text(),"삭제")]').click()
    xpath = '/html/body/div[2]/div/div/div[2]/div/button[2]'
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,xpath))).click()

    # 7.장바구니에 담긴 상품 수 확인
    print('장바구니에 담긴 상품 수 확인')
    driver.refresh()
    element_s = driver.find_element(By.XPATH, xpath_s).text
    count_s = str(count-number_del)
    if count_s == element_s:
        f.write('Pass - 삭제 후 담긴 상품 갯수' + count_s + '\n')
    else:
        f.write('Faill - 삭제 후 장바구니에 담긴 상품 수 확인\n')
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니에 표시된 숫자: ' + element_s)

    f.close()

def test_3():
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\nOHO-3\n')
    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    print('브라우저 연결')
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.쇼핑탭 이동
    print('쇼핑탭 이동')
    xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    #3.임의의 상품 장바구니에 담기
    print('상품 장바구니에 담기')
    count = random.randrange(2, 7)
    for number in range(1, count+1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
        item = re.findall(r'\d+', element)
        driver.get(element)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('0')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('0')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('0')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert.accept()
                        select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/ul/li[1]/article/label/div'
                        element = driver.find_element(By.XPATH, select_xpath).send_keys('test')

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            pass

        element = driver.find_element(By.XPATH,'//span[contains(text(),"주문금액")]')
        item_cost = element.find_element(By.XPATH,'"following-sibling::').text
        element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    #4.장바구니로 이동
    print('장바구니 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    element = driver.find_element(By.XPATH, xpath).click()


    f.close()










