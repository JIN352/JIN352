import ohou_test

#@pytest.mark.flaky(reruns=3, reruns_delay=2) # 실패 후 3번 재 실행
# 랜덤 상품 장바구니 담기 확인
try:
    ohou_test.test_1()
    print('OHO-1 Pass')
except: print('OHO-1 Fail')

try:
    ohou_test.test_2()
    print('OHO-2 Pass')
except: print('OHO-2 Fail')