from sharingparktest.tools.lib_util import UIutil

class Login:

    def __init__(self, driver):
        self.driver = driver

    def input_uname(self, username):
        username_ele = UIutil.find_element("login", "username")
        UIutil.input(username_ele, username)

    def input_password(self, password):
        password_ele = UIutil.find_element("login", "password")
        UIutil.input(password_ele, password)

    def input_verifycode(self, verifycode):
        verifycode_ele = UIutil.find_element("login", "verifycode")
        UIutil.input(verifycode_ele, verifycode)

    def login_button(self):
        button_ele = UIutil.find_element("login", "login_button")
        UIutil.click(button_ele)

    def do_login(self, login_data):
        self.input_uname(login_data["username"])
        self.input_password(login_data["password"])
        self.input_verifycode(login_data["verifycode"])
        self.login_button()


if __name__ == '__main__':
    driver = UIutil.get_driver()
    login_data = {"username": "出租方1", "password": "123", "verifycode": "0000"}
    test = Login(driver)
    test.do_login(login_data)