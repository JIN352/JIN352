import io
import os

from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class test_func():

    # Initializer
    def __init__(self, driver):     # 초기화
        self.driver = driver

    def cart_screenshot(self, path):
        """
        장바구니 내부 스크린샷
        :param path: 파일 저장 위치
        :return:
        """

        self.create_folder(path)                                                       #이미지 저장 폴더 생성
        self.driver.find_element(By.CLASS_NAME, 'css-ym6lm7').click()                  #장바구니 위치 이동
        self.driver.find_element(By.CLASS_NAME, 'css-1rqmgt4.enny2c40').click()        #쿠폰 띠배너 제거
        self.driver.maximize_window()
        elements = self.driver.find_elements(By.CLASS_NAME, 'commerce-cart__content__group-item')        #상품 위치

        # 상단 배너, 토탈 금액 스크린샷 저장
        self.driver.find_element(By.CLASS_NAME, 'sticky-child.commerce-cart__side-bar').screenshot(path + '\cart_total.png')
        self.driver.find_element(By.CLASS_NAME, 'css-i7a8i3.e6rqo2c5').screenshot(path + '\cart_bannser.png')

        # 상단 배너 제거
        element_to_remove = self.driver.find_element(By.CLASS_NAME,"sticky-container")
        self.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element_to_remove)

        # 동일 요소 스크린샷 후 리스트 추가
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

        combined_image.save(path + '\item_list.png')        # 스크린샷 저장# 상품별 스크린샷 저장

    def create_folder(self, directory):
        """

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
            Select(element).select_by_value('1')
            self.driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = self.driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                self.driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = self.driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
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
