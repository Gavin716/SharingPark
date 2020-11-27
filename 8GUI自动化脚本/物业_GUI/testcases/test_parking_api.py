from woniutest.tools.util import FileUtil
from woniutest.tools.ui_util import ApiUtil

class TestParking:

    def test_staff_alter(self):#修改
        test_info = FileUtil().get_excel('../testdata/test_parking_info.ini','property','staff_alter_api')
        ApiUtil.assert_api(test_info)

    def test_staff_add(self):#增加
        test_info = FileUtil().get_excel('../testdata/test_parking_info.ini','property','staff_add_api')
        ApiUtil.assert_api(test_info)

    def test_staff_search(self):#查询
        test_info = FileUtil().get_excel('../testdata/test_parking_info.ini','property','staff_search_api')
        ApiUtil.assert_api(test_info)

if __name__ == '__main__':
    test = TestParking()
    test.test_staff_search()
