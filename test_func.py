import io

from PIL import Image

def full_screenshot(driver, By, screenshot_filename):
    driver.find_element(By.CLASS_NAME, 'css-xh0ic1').click() #장바구니 위치 이동
    driver.find_element(By.CLASS_NAME, 'css-1rqmgt4.enny2c40').click()        #쿠폰 띠배너 제거
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
    full_page_screenshot.save(screenshot_filename)
