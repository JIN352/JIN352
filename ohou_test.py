import random
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
    #driver.maximize_window()

    #2.쇼핑탭 이동
    print('쇼핑탭 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element = driver.find_element(By.XPATH, xpath).click()
    number = 0
    xpath = '//*[@id="store-index"]/section[3]/div[2]/div['+str(number+1)+']/article/a'
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('href')
    print(element)
    itemlist = ['1244849', '1297593', '1502238', '767440', '1450530', '1918219','144229','345755']
    random.shuffle(itemlist)

    #3.임의의 상품 선택
    for number in range(8):

        print(str(number+1)+'번 상품페이지 이동')
        item = itemlist[number]
        url = 'https://ohou.se/productions/' + item
        driver.get(url)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/div/span'
        itemname = driver.find_element(By.XPATH, xpath).text
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/p/a'
        element = driver.find_element(By.XPATH, xpath).text
        baner = '[' + element + '] '
        itemname = baner+itemname
        print(itemname)


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
                alert = driver.switch_to.alert
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('0')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('0')
                    element = driver.find_element(By.XPATH, xpath).click()

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
            result = ['상품번호' + item + ' Pass']
        else:
            result = ['상품번호' + item+' Fail']

        f.write(str(result))
    f.close()

def test_2():
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\nOHO-2')

    f.close()











