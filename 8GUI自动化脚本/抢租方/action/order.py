from tingna.action.login import Login
from tingna.tools.lib_util import UiUtil
import time

class Order:
    def __init__(self, driver):
        self.driver = driver

    def order_login(self):
        Login(self.driver).do_login({'username': '抢租客周友2', 'password': '123', 'verifycode': '0000'})

    def click_parking(self):
        self.driver.switch_to.frame('testIframe')
        parking_button_element = UiUtil.find_elment('order','parking')
        UiUtil.click(parking_button_element)

    def click_by(self):
        by_button_element = UiUtil.find_elment('order', 'by')
        UiUtil.click(by_button_element)

    def click_order(self):
        self.driver.driver.find_element_by_xpath('//*[@id="orderModel"]/div/div/div[2]/div/div[2]'
                                                 '/div[2]/div[1]/table/tbody/tr/td[5]/input').sendkey("2020/12/22")
        # order_button_element = UiUtil.find_elment('order', 'bybutton')
        # UiUtil.click(order_button_element)

    def do_order(self):
        self.order_login()
        self.click_parking()
        self.click_by()
        self.click_order()


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    Order(driver).do_order()