import io
import os
import time

from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class test_func():

    # Initializer
    def __init__(self, driver):     # 초기화
        self.driver = driver

    def cart_screenshot(self, path):
        """
        장바구니 내 이미지 저장
        :param path: 파일 저장 위치
        :return: 없음
        """

        self.create_folder(path)                                                       #이미지 저장 폴더 생성
        self.driver.find_element(By.CLASS_NAME, 'css-giclcf').click()                  #장바구니 위치 이동
        self.driver.find_element(By.CLASS_NAME, 'css-1rqmgt4.enny2c40').click()        #쿠폰 띠배너 제거
        self.driver.maximize_window()
        elements = self.driver.find_elements(By.CLASS_NAME, 'commerce-cart__content__group-item')        #상품 위치

        # 상단 배너, 토탈 금액 이미지 저장
        self.driver.find_element(By.CLASS_NAME, 'sticky-child.commerce-cart__side-bar').screenshot(path + '\cart_total.png')
        self.driver.find_element(By.CLASS_NAME, 'sticky-container').screenshot(path + '\cart_bannser.png')

        # 상단 배너 제거
        element_to_remove = self.driver.find_element(By.CLASS_NAME,"sticky-container")
        self.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element_to_remove)

        # 동일 요소 이미지 후 리스트 추가
        screenshots = []
        for i, element in enumerate(elements):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            screenshot = element.screenshot_as_png
            screenshots.append(Image.open(io.BytesIO(screenshot)))

        # 이미지 사이즈 조정
        combined_image = Image.new('RGB', (max(img.width for img in screenshots), sum(img.height for img in screenshots)))

        # 이미지를 합치기
        y_offset = 0
        for img in screenshots:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.height

        combined_image.save(path + '\item_list.png')        # 상품별 이미지 저장

    def create_folder(self, directory):
        """
        폴더 생성
        :param directory: 폴더 생성 위치 및 명
        :return: 없음
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

    def item_option(self):
        """
        상품 페이지 내부에서 장바구니 버튼 클릭 및 옵션 선택
        :return: 없음
        """
        #장바구니 버튼 클릭
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        self.driver.find_element(By.XPATH, xpath).click()

        # 옵션 선택
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = self.driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = self.driver.find_element(By.XPATH, select_xpath)
            select = Select(element)            # Select 객체 생성
            options = select.options            # 모든 옵션 가져오기
            for option in options[1:]:
                # 옵션의 텍스트에 "품절"이 포함되어 있다면 다른 옵션 선택
                if "품절" not in option.text:
                    select.select_by_visible_text(option.text)
                    break
            self.driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = self.driver.find_element(By.XPATH, select_xpath)
                select = Select(element)  # Select 객체 생성
                options = select.options  # 모든 옵션 가져오기
                for option in options[1:]:
                    # 옵션의 텍스트에 "품절"이 포함되어 있다면 다른 옵션 선택
                    if "품절" not in option.text:
                        select.select_by_visible_text(option.text)
                        break
                self.driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = self.driver.find_element(By.XPATH, select_xpath)
                    select = Select(element)  # Select 객체 생성
                    options = select.options  # 모든 옵션 가져오기
                    for option in options[1:]:
                        # 옵션의 텍스트에 "품절"이 포함되어 있다면 다른 옵션 선택
                        if "품절" not in option.text:
                            select.select_by_visible_text(option.text)
                            break
                    self.driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        self.driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')
                        self.driver.find_element(By.XPATH, xpath).click()

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            pass

        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "css-0.e131ry20")))
        except TimeoutException:
            self.driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')          # 필수 TEXT 입력
            self.driver.find_element(By.XPATH, xpath).click()

    def item_option_price(self):
        """
        상품 페이지 내부에서 장바구니 버튼 클릭 및 옵션 선택과 상품 금액 추가
        :return: 상품 금액
        """
        #장바구니 버튼 클릭
        element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
        item_cost = element_s.text
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/button[1]'
        self.driver.find_element(By.XPATH, xpath).click()

        # 옵션 선택
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = self.driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = self.driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('1')
            element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
            item_cost = element_s.text
            self.driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = self.driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
                item_cost = element_s.text
                self.driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = self.driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
                    element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
                    item_cost = element_s.text
                    self.driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        self.driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')
                        self.driver.find_element(By.XPATH, xpath).click()

                    except:
                        pass

                except:
                    pass

            except:
                pass

        except:
            pass

        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "css-0.e131ry20")))
        except TimeoutException:
            self.driver.find_element(By.CLASS_NAME, 'css-1kg8g4k').send_keys('test')          # 필수 TEXT 입력
            self.driver.find_element(By.XPATH, xpath).click()

        return item_cost

    def item_name(self):
        """
        상품명 추출
        :return: 상품명
        """

        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/div/span'
        itemname = self.driver.find_element(By.XPATH, xpath).text
        xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[1]/h1/p/a'
        element = self.driver.find_element(By.XPATH, xpath).text
        baner = '[' + element + '] '
        itemname = baner + itemname  # 상품 이름 추출

        return itemname

    def get_link(self, number):
        """
        상품 링크 추출
        :param number: 장바구니에 담을 상품 갯수
        :return: 상품링크
        """
        element = self.driver.find_element(By.CLASS_NAME,'css-1i1zz0y.e1g1wifd2')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(2)
        line_choice = self.driver.find_elements(By.CLASS_NAME,'css-oe54r4.etj6rb20')[number-1]
        element= line_choice.find_element(By.TAG_NAME,'a').get_attribute('href')
        return element

