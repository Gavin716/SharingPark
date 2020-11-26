from tingna.tools.util import FileUtil
from tingna.tools.lib_util import UiUtil
from tingna.action.order import Order
from tingna.action.order import Login
import unittest


class TenantUi(unittest.TestCase):
    def setUp(self):
        self.driver = UiUtil.get_driver()

    def tearDown(self):
        pass

    def test_login_ui(self):#登录
        test_info = FileUtil().get_test_info('..\\conf\\test_parking_info.ini','parking','tenant_login_ui')
        for data in test_info:
            a = data['params']
            Login(self.driver).do_login(a)
            Login(self.driver).do_logout()


    def test_order_ui(self):#下单
        Order(self.driver).do_order()


if __name__ == '__main__':
    test = Tenant()
    test.test_login_ui()