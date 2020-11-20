from tingna.tools.util import FileUtil
from tingna.tools.lib_util import APIUtil
import unittest

class Tenant(unittest.TestCase):

    def test_homepage_api(self):#主页
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_homepage_api')
        APIUtil.assert_api(test_info)

    def test_snap_api(self):#抢购
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_homepage_api')
        APIUtil.assert_api(test_info)

    def test_history_api(self):#历史订单
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_history_api')
        APIUtil.assert_api(test_info)

    def test_cemment_api(self):#评论
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_cemment_api')
        APIUtil.assert_api(test_info)

    def test_me_api(self):#我的
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_me_api')
        APIUtil.assert_api(test_info)

    def test_bundled_api(self):#绑定
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','tenant','tenant_bundled_api')
        APIUtil.assert_api(test_info)

if __name__ == '__main__':
    test = Tenant()
    test.test_homepage_api()