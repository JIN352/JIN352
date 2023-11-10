import io
import os
import time

from PIL import Image

def cart_screenshot(driver, By, path,item):

    create_folder(path)                                                       #이미지 저장 폴더 생성
    driver.find_element(By.CLASS_NAME, 'css-xh0ic1').click()                  #장바구니 위치 이동
    driver.find_element(By.CLASS_NAME, 'css-1rqmgt4.enny2c40').click()        #쿠폰 띠배너 제거
    driver.maximize_window()
    elements = driver.find_elements(By.CLASS_NAME, 'commerce-cart__content__group-item')        #상품 위치

    # 동일 요소 스크린샷 후 리스트 추가
    screenshots = []
    for i, element in enumerate(elements):
        screenshot = element.screenshot_as_png
        screenshots.append(Image.open(io.BytesIO(screenshot)))

    # 이미지 사이즈 조정
    combined_image = Image.new('RGB', (max(img.width for img in screenshots), sum(img.height for img in screenshots)))

    # 이미지를 합치기
    y_offset = 0
    for img in screenshots:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    # 각 스크린샷 저장
    combined_image.save(path + '\item_list.png')
    driver.find_element(By.CLASS_NAME, 'sticky-child.commerce-cart__side-bar').screenshot(path + '\cart_total.png')
    driver.find_element(By.CLASS_NAME, 'css-i7a8i3.e6rqo2c5').screenshot(path + '\cart_bannser.png')

    # 상품별 스크린샷 저장
    item_number = item.reverse()
    for i, element in enumerate(elements):
        screenshot = element.screenshot_as_png
        name = str(item_number[i])
        with open(path+'\s'+ name, "wb") as file:
            file.write(screenshot)
        i += 1

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
