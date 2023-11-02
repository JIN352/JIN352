import random
import re
import time
import io

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
f = open("C:/test/ohou_test_result.txt", 'w')
f.close()
result = []
folder = 'C:/test/'

def full_screenshot(screenshot_filename):
    element = driver.find_element(By.CLASS_NAME, 'css-xh0ic1').click()      #장바구니 위치 이동
    element = driver.find_element(By.CLASS_NAME, 'css-1rqmgt4.enny2c40').click()        #쿠폰 띠배너 제거
    screenshots = []        # 전체 페이지 스크린샷을 저장할 리스트 초기화
    driver.maximize_window()
    total_height = int(driver.execute_script("return document.body.scrollHeight"))      # 전체 페이지 높이 계산
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_y = 0         # 현재 위치 초기화
    while scroll_y < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_y});")        # 스크롤 다운 작업 수행
        screenshot = driver.get_screenshot_as_png()                     # 스크린샷 찍고 저장
        screenshots.append(Image.open(io.BytesIO(screenshot)))
        scroll_y += viewport_height         # 스크롤 위치 업데이트

    # 모든 스크린샷을 하나로 합치기
    full_page_screenshot = Image.new("RGB", (driver.execute_script("return window.innerWidth"), total_height))
    y_offset = 0
    for screenshot in screenshots:
        full_page_screenshot.paste(screenshot, (0, y_offset))
        y_offset += screenshot.size[1]

    # 전체 페이지 스크린샷 저장
    full_page_screenshot.save(folder+screenshot_filename)

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
    for number in range(1, 8):

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

        # 4.장바구니 버튼 클릭
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('1')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        element = driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')
                        element = driver.find_element(By.XPATH, xpath).click()

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            f.write('옵션 선택 실패 상품 번호:' + str(item) + '\n')

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
    screenshot_filename = "OHO-1.png"
    full_screenshot(screenshot_filename)

    print('test1 pass')


def test_2():
    global a
    driver.delete_all_cookies()  # 쿠키 삭제
    f = open("C:/test/ohou_test_result.txt", 'a')
    f.write('\n\nOHO-2:랜덤 상품 장바구니 담기 확인\n')
    # 랜덤 상품 장바구니 담기 확인
    # 1.브라우저 열기
    print('브라우저 연결')
    url = 'https://ohou.se/'
    driver.get(url)

    # 2.쇼핑탭 이동
    print('쇼핑탭 이동')
    xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    # 3.임의의 상품 장바구니에 담기
    print('상품 장바구니에 담기')
    count = random.randrange(2, 7)
    for number in range(1, count + 1):
        xpath = '//*[@id="store-index"]/section[3]/div[2]/div[' + str(number) + ']/article/a'
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute(
            'href')
        item = re.findall(r'\d+', element)
        driver.get(element)
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('1')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        element = driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')
                        element = driver.find_element(By.XPATH, xpath).click()

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            f.write('옵션 선택 실패 상품 번호:' + str(item) + '\n')

        element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    # 4.장바구니로 이동
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
        f.write('장바구니에 담은 상품 수: ' + count_s + '\n')
    else:
        f.write('Faill - 장바구니에 담긴 상품 수 확인\n')
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니 표시 수: ' + element_s + '\n')

    if count_s != element_s:
        return False

    # 6.상품 삭제
    if count < 4:
        number_del = 1
    else:
        number_del = random.randrange(1, count - 1)
    print(str(number_del) + '개 상품 삭제')
    element = driver.find_elements(By.CLASS_NAME, '_3UImz')
    for a in range(number_del + 1):
        print(str(a) + '회')
        item_index = element[a]
        item_index.click()
    number_del = a
    element = driver.find_element(By.XPATH, '//button[contains(text(),"삭제")]')
    element = driver.execute_script("arguments[0].click();", element)
    xpath = '/html/body/div[2]/div/div/div[2]/div/button[2]'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()

    # 7.장바구니에 담긴 상품 수 확인
    print('장바구니에 담긴 상품 수 확인')
    driver.refresh()
    element_s = driver.find_element(By.XPATH, xpath_s).text
    count_s = str(count - number_del)
    if count_s == element_s:
        f.write('Pass\n')
        f.write('삭제한 상품 수: ' + str(number_del) + ' / 장바구니에 담김 상품 수: ' + element_s)
    else:
        f.write('Faill\n')
        f.write('실제 담긴 상품 수: ' + count_s + ' / 장바구니 표시 수: ' + element_s + ' 삭제한 상품 수: ' + str(number_del))

    f.close()
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
    xpath_s = '/html/body/div[1]/div/div/header/div[1]/div/div/div[3]/a[2]'
    element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

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
        element_s = driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
        item_cost = element_s.text
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        element = driver.find_element(By.XPATH, xpath).click()

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('1')
            element = driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                element = driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
                    element = driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        element = driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')
                        element = driver.find_element(By.XPATH, xpath).click()

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            f.write('옵션 선택 실패 상품 번호:' + str(item) + '\n')

        item_costs += int(re.sub(r'[^0-9]', '', item_cost))
        element_s = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_s))).click()

    # 4.장바구니로 이동
    print('장바구니 이동')
    xpath = '/html/body/div[1]/div/div/header/div[1]/div/div/div[4]/div/a'
    element = driver.find_element(By.XPATH, xpath).click()

    # 5.총 결제 금액 확인
    time.sleep(3)
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
    if (item_costs + ship_cost) != total_cost:
        return False

    print('test3 pass')



