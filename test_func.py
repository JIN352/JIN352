import io
import os
import time
import re

from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

class Oho_test_func():
    # ohou_test에 사용
    
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
        xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div/button[1]'
        self.driver.find_element(By.XPATH, xpath).click()

        # 옵션 선택
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = self.driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
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
                select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
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
                    select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
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
                        self.driver.find_element(By.CLASS_NAME, 'css-1nol6lk').send_keys('test')
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
            self.driver.find_element(By.CLASS_NAME, 'css-1nol6lk').send_keys('test')          # 필수 TEXT 입력
            self.driver.find_element(By.XPATH, xpath).click()

    def item_option_price(self):
        """
        상품 페이지 내부에서 장바구니 버튼 클릭 및 옵션 선택과 상품 금액 추가
        :return: 상품 금액
        """
        #장바구니 버튼 클릭
        element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
        item_cost = element_s.text
        xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div/button[1]'
        self.driver.find_element(By.XPATH, xpath).click()

        # 옵션 선택
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 1번 필수 옵션 선택
            alert = self.driver.switch_to.alert
            alert.accept()
            select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[1]/select'
            element = self.driver.find_element(By.XPATH, select_xpath)
            Select(element).select_by_value('1')
            element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
            item_cost = element_s.text
            self.driver.find_element(By.XPATH, xpath).click()

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 2번 필수 옵션 선택
                alert.accept()
                select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[2]/select'
                element = self.driver.find_element(By.XPATH, select_xpath)
                Select(element).select_by_value('1')
                element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
                item_cost = element_s.text
                self.driver.find_element(By.XPATH, xpath).click()

                try:
                    WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 3번 필수 옵션 선택
                    alert.accept()
                    select_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div[2]/div[2]/section/div/div/div[3]/select'
                    element = self.driver.find_element(By.XPATH, select_xpath)
                    Select(element).select_by_value('1')
                    element_s = self.driver.find_element(By.XPATH, '//span[contains(text(),"주문금액")]/../span[2]')
                    item_cost = element_s.text
                    self.driver.find_element(By.XPATH, xpath).click()

                    try:
                        WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # 필수 TEXT 입력
                        alert.accept()
                        self.driver.find_element(By.CLASS_NAME, 'css-1nol6lk').send_keys('test')
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
            self.driver.find_element(By.CLASS_NAME, 'css-1nol6lk').send_keys('test')          # 필수 TEXT 입력
            self.driver.find_element(By.XPATH, xpath).click()

        return item_cost

    def item_name(self):
        """
        상품명 추출
        :return: 상품명
        """

        class_name = 'production-selling-header__title__name'
        item_name = self.driver.find_element(By.CLASS_NAME, class_name).text
        class_name = 'production-selling-header__title__brand'
        baner_name = self.driver.find_element(By.CLASS_NAME, class_name).text
        baner = '[' + baner_name + '] '
        itemname = baner + item_name  # 상품 이름 추출
        return itemname

    def get_link(self, number):
        """
        상품 링크 추출
        :param number: 장바구니에 담을 상품 갯수
        :return: 상품링크
        """

        item_class = 'css-oe54r4.etj6rb20'                  #상품 Class Name
        scroll_amount = 600  # 픽셀 단위로 스크롤 양을 설정
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")         #상품으로 스크롤 이동
        time.sleep(3)

        #상품링크 추출
        line_choice = self.driver.find_elements(By.CLASS_NAME, item_class)[number-1]
        element= line_choice.find_element(By.TAG_NAME,'a').get_attribute('href')
        return element


class Kur_test_func():
    # kurly_test에 사용
    # Initializer
    def __init__(self, driver):     # 초기화
        self.driver = driver

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

    def cart_screenshot(self, path):
        """
        장바구니 내 이미지 저장
        :param path: 파일 저장 위치
        :return: 없음
        """

        self.create_folder(path)                                                       #이미지 저장 폴더 생성
        self.driver.maximize_window()
        elements = self.driver.find_elements(By.CLASS_NAME, 'css-bjn8wh.e17itp850')

        # 동일 요소 이미지 후 리스트 추가
        screenshots = []
        for i, element in enumerate(elements):
            screenshot = element.screenshot_as_png
            screenshots.append(Image.open(io.BytesIO(screenshot)))

            # 이미지 사이즈 조정
            combined_width = max(img.width for img in screenshots)
            combined_height = sum(img.height for img in screenshots)

            combined_image = Image.new('RGB', (combined_width, combined_height))

            # 이미지를 합치기
            y_offset = 0
            for img in screenshots:
                combined_image.paste(img, (0, y_offset))
                y_offset += img.height
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        combined_image.save(path + '\item_list.png')  # 상품별 이미지 저장

        self.driver.find_element(By.CLASS_NAME, 'css-47nnfk.e11sj0mr1').screenshot(path + '\cart_total_0.png')
        self.driver.find_element(By.CLASS_NAME, 'css-1e06u91.e1g2d0840').screenshot(path + '\cart_total_1.png')
        self.driver.find_element(By.CLASS_NAME, 'css-1ih0cp7.e6js8xr0').screenshot(path + '\cart_total_2.png')

    def get_item(self, number):
        """
        상품 장바구니에 담기
        :param number: 장바구니에 담을 상품 갯수
        :return: 상품번호, 상품명
        """
        time.sleep(2)
        scroll_amount = 300  # 픽셀 단위로 스크롤 양을 설정
        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")  # 상품으로 스크롤 이동
        if number > 4:
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        child_element = self.driver.find_elements(By.XPATH, "//*[text()='담기']")[number-1]
        parent_element = child_element.find_element(By.XPATH, './../..')                    #상위 요소로 이동
        item_number = parent_element.get_attribute('href')                                  #상품 url 추출
        item_number = re.sub(r'[^0-9]', '', item_number)                                    #상품번호 추출
        item_name = parent_element.find_element(By.XPATH, './div[3]/div').text              #상품명 추출
        child_element.click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//*[contains(text(), '장바구니 담기')]").click()  #상품 장바구니 담기
        #옵션 포함 상품에 옵션 수량 선택
        try:
            pop_element = self.driver.find_element(By.ID,'swal2-content')       #알림팝업 노출 확인
            if pop_element:
                self.driver.find_element(By.XPATH, "//*[text()='확인']").click()                     #알림 팝업 닫기
                self.driver.find_element(By.XPATH, "//*[@aria-label='수량올리기']").click()           #옵션 수량 1 올리기
                self.driver.find_element(By.XPATH, "//*[contains(text(), '장바구니 담기')]").click()  #상품 장바구니 담기
        except NoSuchElementException: pass

        return item_number, item_name

    def such_post(self,such):
        """
        배송지 검색
        :param such: 검색할 주소지
        :return: 없음
        """
        time.sleep(2)
        #프레임 변경
        frame = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(frame)
        frame = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(frame)
        #검색할 주소지 입력
        location = self.driver.find_element(By.ID, 'region_name')
        self.driver.execute_script(f"arguments[0].value = '{such}';", location)
        location.send_keys(Keys.ENTER)

    def popup_close(self):
        """
        메인 화면에 노출되는 팝업 닫기
        :return: 없음
        """
        while True:
            try:
                self.driver.find_element(By.XPATH, "//*[text()='닫기']").click()
            except NoSuchElementException:  # "닫기" 문구를 포함한 요소가 더 이상 없을 때 루프 종료
                break