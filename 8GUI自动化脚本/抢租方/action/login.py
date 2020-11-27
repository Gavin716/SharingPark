from tingna.tools.util import FileUtil
from tingna.tools.lib_util import UiUtil
import time

class Login:

    def __init__(self, driver):
        self.driver = driver

    def input_account(self, username):
        uname_element = UiUtil.find_elment('login', 'uname')
        UiUtil.input(uname_element, username)

    def input_password(self, password):
        upass_element = UiUtil.find_elment('login', 'upass')
        UiUtil.input(upass_element, password)

    def input_verifycode(self, verifycode):
        vfcode_element = UiUtil.find_elment('login', 'vcode')
        UiUtil.input(vfcode_element, verifycode)

    def click_login_button(self):
        login_button_element = UiUtil.find_elment('login', 'login_button')
        UiUtil.click(login_button_element)

    def do_login(self, login_data):
        self.input_account(login_data['username'])
        self.input_password(login_data['password'])
        self.input_verifycode(login_data['verifycode'])
        self.click_login_button()

    def do_logout(self):
        logout_button_element = UiUtil.find_elment('login', 'logout_button1')
        UiUtil.click(logout_button_element)
        logout_button_element2 = UiUtil.find_elment('login', 'logout_button2')
        UiUtil.click(logout_button_element2)



if __name__ == '__main__':

    driver = UiUtil.get_driver()
    Login(driver).do_login({'username': '抢租客周友2', 'password': '123', 'verifycode': '0000'})
    time.sleep(2)
    Login(driver).do_logout()