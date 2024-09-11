import os

os.makedirs('C:/test', exist_ok=True)       # 폴더 생성 (존재하지 않으면 생성)

f_m = open("C:/test/test_result.txt", 'w')
f_m.close()

#@pytest.mark.flaky(reruns=2, reruns_delay=2) # 실패 후 3번 재 실행
def test_oho():
    import ohou_test
    f_m = open("C:/test/test_result.txt", 'a')

    try: oho = ohou_test.test_1()
    except: pass
    try:
        if oho is True:
            result = 'OHO-1 Pass\n'
        else:
            result = 'OHO-1 Fail\n'
    except Exception as e:
        result = 'test_1 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_2()
    except: pass
    try:
        if oho is True:
            result = 'OHO-2 Pass\n'
        else:
            result = 'OHO-2 Fail\n'
    except Exception as e:
        result = 'test_2 스크립트 오류 ' + str(e) +'\n'
    finally:
        f_m.write(result)

    try:oho = ohou_test.test_3()
    except: pass
    try:
        if oho is True:
            result = 'OHO-3 Pass\n'
        else:
            result = 'OHO-3 Fail\n'
    except Exception as e:
        result = 'test_3 스크립트 오류 ' + str(e) + '\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_4()
    except: pass
    try:
        if oho is True:
            result = 'OHO-4 Pass\n'
        else:
            result = 'OHO-4 Fail\n'
    except Exception as e:
        result = 'test_4 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: oho = ohou_test.test_5()
    except: pass
    try:
        if oho is True:
            result = 'OHO-5 Pass\n'
        else:
            result = 'OHO-5 Fail\n'
    except Exception as e:
        result = 'test_5 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

def test_kur():
    import kurly_test
    f_m = open("C:/test/test_result.txt", 'a')

    try: kur = kurly_test.test_1()
    except: pass
    try:
        if kur is True:
            result = 'KUR-1 Pass\n'
        else:
            result = 'KUR-1 Fail\n'
    except Exception as e:
        result = 'test_1 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: kur = kurly_test.test_2()
    except: pass
    try:
        if kur is True:
            result = 'KUR-2 Pass\n'
        else:
            result = 'KUR-2 Fail\n'
    except Exception as e:
        result = 'test_2 스크립트 오류 ' + str(e) +'\n'
    finally:
        f_m.write(result)

    try:kur = kurly_test.test_3()
    except: pass
    try:
        if kur is True:
            result = 'KUR-3 Pass\n'
        else:
            result = 'KUR-3 Fail\n'
    except Exception as e:
        result = 'test_3 스크립트 오류 ' + str(e) + '\n'
    finally:
        f_m.write(result)

    try: kur = kurly_test.test_4()
    except: pass
    try:
        if kur is True:
            result = 'KUR-4 Pass\n'
        else:
            result = 'KUR-4 Fail\n'
    except Exception as e:
        result = 'test_4 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

    try: kur = kurly_test.test_5()
    except: pass
    try:
        if kur is True:
            result = 'KUR-5 Pass\n'
        else:
            result = 'KUR-5 Fail\n'
    except Exception as e:
        result = 'test_5 스크립트 오류 '+ str(e) +'\n'
    finally:
        f_m.write(result)

f_m.close()