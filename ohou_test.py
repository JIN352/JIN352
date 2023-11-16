import random
import re
import time
from Test_func import test_func

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
test_func = test_func(driver)
test_func.create_folder('C:/test')
f = open("C:/test/ohou_test_result.txt", 'w')
f.close()
folder = 'C:/test/'
result = []


def test_1():
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('OHO-1:랜덤 상품 장바구니 담기 확인\n')

    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.쇼핑탭 이동
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element = driver.find_element(By.XPATH, xpath).click()

    # 3.임의의 상품 선택
    try:
        count = random.randrange(2, 7)  # 장바구니에 담을 상품 수 선택
        for number in range(1, count + 1):

            xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute(
                'href')
            item = re.findall(r'\d+', element)
            driver.get(element)
            xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/div/span'
            itemname = driver.find_element(By.XPATH, xpath).text
            xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/p/a'
            element = driver.find_element(By.XPATH, xpath).text
            baner = '[' + element + '] '
            itemname = baner + itemname
            test_func.item_option()  # 상품 장바구니에 담기

            # 5.장바구니 이동
            xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
            element = driver.find_element(By.XPATH, xpath_s).click()

            # 6.상품 확인
            driver.implicitly_wait(3)
            xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/ul/li[1]/article/ul/li/article/ul/li/article/a/div[2]/h1'
            element = driver.find_element(By.XPATH, xpath).text

            if element == itemname:
                result = ' / ' + str(number) + '번 상품' + '[상품번호' + str(item) + ' Pass]'

            else:
                result = ' / ' + str(number) + '번 상품' + '[상품번호' + str(item) + ' Fail]'

            f.write(result)
            if element != itemname:
                return False

            xpath = '/html/body/div[1]/div/div/header/div/div/div/div[3]/a[2]'
            element = driver.find_element(By.XPATH, xpath).click()  # 쇼핑탭 이동

        f.close()
    finally: test_func.cart_screenshot(folder+'OHO-1')
    print('test1 pass')


def test_2():
    global a
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-2:랜덤 상품 장바구니 담기 확인\n')
    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.쇼핑탭 이동
    xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    # 3.임의의 상품 장바구니에 담기
    count = random.randrange(2, 7)      #장바구니에 담을 상품 수 선택
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'       #상품번호 추출
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute(
            'href')
        item = re.findall(r'\d+', element)
        driver.get(element)         #상품 페이지 이동
        test_func.item_option()     #상품 장바구니에 담기
        element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    # 4.장바구니로 이동
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    element = driver.find_element(By.XPATH, xpath).click()

    # 5.장바구니에 담긴 상품 수 확인
    driver.refresh()
    xpath_s = '/html/body/div[1]/div/div/header/div/div/div/div[4]/div/a/span[2]'
    element_s = driver.find_element(By.XPATH, xpath_s).text
    count_s = str(count)
    if count_s == element_s:
        f.write('장바구니에 담은 상품 수: ' + count_s + '\n')
    else:
        f.write('Faill - 장바구니에 담긴 상품 수 확인\n')
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니 표시 수: ' + element_s + '\n')

    if count_s != element_s:
        return False
    test_func.cart_screenshot(folder + 'OHO-2_before')

    # 6.상품 삭제
    if count < 4:
        number_del = 1
    else:
        number_del = random.randrange(1, count - 1)
    element = driver.find_elements(By.CLASS_NAME, '_3UImz')

    for a in range(number_del + 1):
        item_index = element[a]
        item_index.click()
    number_del = a
    element = driver.find_element(By.XPATH, '//button[contains(text(),"삭제")]')
    driver.execute_script("arguments[0].click();", element)
    element = driver.find_element(By.CLASS_NAME,'css-97tdd8')
    element.screenshot(folder+'OHO-2_before/del.png')
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-6ums0u')))
    element.click()

    # 7.장바구니에 담긴 상품 수 확인
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-97tdd8')))
        element.click()
        f.write('삭제 버튼 클릭 확인 필요\n')
    except TimeoutException:
        pass
    driver.refresh()
    element_s = driver.find_element(By.XPATH, xpath_s).text
    count_s = str(count - number_del)
    f.write('삭제한 상품 수: ' + str(number_del)+'\n')
    if count_s == element_s:
        f.write('Pass\n')
        f.write('장바구니에 담김 상품 수: ' + element_s)
    else:
        f.write('Faill\n')
        f.write('노출되야 될 상품 수: ' + count_s + ' / 장바구니 표시 수: ' + element_s)

    f.close()
    test_func.cart_screenshot(folder + 'OHO-2_after')

    if count_s != element_s:
        return False
    print('test2 pass')


def test_3():
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-3:랜덤 상품 장바구니 담기 확인\n')
    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    print('브라우저 연결')
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.쇼핑탭 이동
    print('쇼핑탭 이동')
    shoping_clk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 3.임의의 상품 장바구니에 담기
    print('상품 장바구니에 담기')
    count = random.randrange(2, 7)
    item_costs = 0
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute(
            'href')
        item = re.findall(r'\d+', element)
        driver.get(element)
        item_cost = test_func.item_option_price()     #상품 장바구니에 담기 & 상품 금액 확인
        item_costs += int(re.sub(r'[^0-9]', '', item_cost))
        # print('개별 금액')
        # print(item_cost)
        # time.sleep(20)
        # print('합친금액')
        # print(item_costs)
        shoping_clk = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='쇼핑']"))).click()

    # 4.장바구니로 이동
    print('장바구니 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    element = driver.find_element(By.XPATH, xpath).click()

    # 5.총 결제 금액 확인
    time.sleep(2)
    element = driver.find_elements(By.CLASS_NAME, 'commerce-cart__summary__row.commerce-cart__summary__row--total')[0]
    element = element.find_element(By.XPATH, './dd/span').get_attribute('innerText')
    total_cost = int(re.sub(r'[^0-9]', '', element))
    element = driver.find_elements(By.XPATH, '//*[contains(text(),"총 배송비")]/../dd/span')[0].get_attribute('innerText')
    ship_cost = int(re.sub(r'[^0-9]', '', element))
    if (item_costs + ship_cost) == total_cost:
        f.write('Pass\n')
        f.write('노출금액:' + str(total_cost) + '/')
        f.write('실제금액: 상품금액' + str(item_costs) + '총 배송비:')
    else:
        f.write('False\n')
        f.write('노출금액:' + str(total_cost) + '/')
        f.write('실제금액: (상품금액:' + str(item_costs) + '+총 배송비:' + str(ship_cost) + ')')

    f.close()
    test_func.cart_screenshot(folder+'OHO-3')
    if (item_costs + ship_cost) != total_cost:
        return False

    print('test3 pass')



