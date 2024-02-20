import ohou_test
f_m = open("C:/test/test_result.txt", 'w')
f_m.close()

#@pytest.mark.flaky(reruns=2, reruns_delay=2) # 실패 후 3번 재 실행
# 랜덤 상품 장바구니 담기 확인
def test():
    f_m = open("C:/test/test_result.txt", 'a')

    try: oho = ohou_test.test_1()
    except: pass
    try:
        if oho is False:
            result = 'OHO-1 Fail\n'
        else:
            result = 'OHO-1 Pass\n'
    except Exception as e:
        result = 'test_1 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_2()
    except: pass
    try:
        if oho is False:
            result = 'OHO-2 Fail\n'
        else:
            result = 'OHO-2 Pass\n'
    except Exception as e:
        result = 'test_2 스크립트 오류 ' + str(e) +'\n'
    finally:
        f_m.write(result)

    try:oho = ohou_test.test_3()
    except: pass
    try:
        if oho is False:
            result = 'OHO-3 Fail\n'
        else:
            result = 'OHO-3 Pass\n'
    except Exception as e:
        result = 'test_3 스크립트 오류 ' + str(e) + '\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_4()
    except: pass
    try:
        if oho is False:
            result = 'OHO-4 Fail\n'
        else:
            result = 'OHO-4 Pass\n'
    except Exception as e:
        result = 'test_4 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_5()
    except: pass
    try:
        if oho is False:
            result = 'OHO-5 Fail\n'
        else:
            result = 'OHO-5 Pass\n'
    except Exception as e:
        result = 'test_5 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

f_m.close()