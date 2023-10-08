import ohou_test
import pytest

f_m = open("C:/test/test_result.txt", 'w')
f_m.close()

#@pytest.mark.flaky(reruns=2, reruns_delay=2) # 실패 후 3번 재 실행
# 랜덤 상품 장바구니 담기 확인
def test():
    f_m = open("C:/test/test_result.txt", 'a')
    oho = ohou_test.test_1()
    try:
        if oho is False:
            result = 'OHO-1 Fail\n'
        else:
            result = 'OHO-1 Pass\n'
    except Exception as e:
        result = '스크립트 오류'+ str(e) +'\n'
    finally:
        f_m.write(result)

    oho = ohou_test.test_2()
    try:
        if oho is False:
            result = 'OHO-2 Fail\n'
        else:
            result = 'OHO-2 Pass\n'
    except Exception as e:
        result = '스크립트 오류' + str(e) +'\n'
    finally:
        f_m.write(result)
f_m.close()