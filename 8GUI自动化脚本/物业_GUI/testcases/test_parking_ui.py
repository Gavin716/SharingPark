import time
from woniutest.action.proper import ParkingProper
from woniutest.tools.util import FileUtil
from woniutest.tools.ui_util import UiUtil


class TestProper:

    def __init__(self,driver):
        self.driver = driver

    def test_update_proper(self,option):#解析、取出测试要用的数据
        proper_data = FileUtil().get_txt('../testdata/parking_proper_datas')
        params_list = FileUtil().get_excel('../testdata/test_parking_info.ini','property',option)
        for params in params_list:
            proper_data['proper_name'] = params['params']['uname']
            proper_data['proper_passwd'] = params['params']['upass']
            proper_data['proper_phone'] = params['params']['phone']
            proper_data['proper_introduce'] = params['params']['propertyintroduce']
            proper_data['proper_uificateid'] = params['params']['propertycertificateid']
            time.sleep(1)
            ParkingProper(self.driver).click_do()
            time.sleep(2)
            ParkingProper(self.driver).do_modify_staff(proper_data)
            # ParkingProper(self.driver).do_add_staff(proper_data)
            time.sleep(2)
            self.driver.refresh()

if __name__ == '__main__':
    test = TestProper(driver=UiUtil.get_driver())
    test.test_update_proper('staff_modify_ui')
    # test.test_update_proper('staff_add_ui')