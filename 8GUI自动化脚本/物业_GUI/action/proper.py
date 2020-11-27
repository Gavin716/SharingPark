import time
from woniutest.tools.ui_util import UiUtil, DoElement

class ParkingProper:

    def __init__(self,driver):
        self.driver = driver
        self.driver.implicitly_wait(15)
        #登录功能

    def login(self):
        uname = UiUtil.find_element('login', 'uname')
        DoElement.input(uname, '物业0')
        upass = UiUtil.find_element('login', 'upass')
        DoElement.input(upass, '123')
        verifycode = UiUtil.find_element('login', 'verifycode')
        DoElement.input(verifycode, '0000')
        time.sleep(1)
        login_button = UiUtil.find_element('login', 'login_button')
        login_button.click()

    def switch_iframe(self):#切换iframe
        iframe1 = UiUtil.find_element('iframe', 'iframe1')
        self.driver.switch_to.frame(iframe1)


    def index(self):#选择第几个修改
        select = UiUtil.find_element('modify','modify_index')
        select.click()

    def modify_button(self):#【修改】按键
        modify = UiUtil.find_element('modify', 'modify_button')
        modify.click()

    def modify(self):#修改完后的【确认修改按钮】
        mo = UiUtil.find_element('modify','modify')
        mo.click()

    def add_button(self):  # 【增加】按键
        add = UiUtil.find_element('add', 'add_button')
        add.click()

    def add(self):  # 增加完后的【确认增加】按钮
        ad = UiUtil.find_element('add', 'add')
        ad.click()

    def input_name(self,proper_name):#物业名
        uname = UiUtil.find_element('input_element', 'uname')
        DoElement.input(uname, proper_name)

    def input_passwd(self,proper_passwd):#物业密码
        unpass = UiUtil.find_element('input_element', 'upass')
        DoElement.input(unpass, proper_passwd)

    def input_phone(self,proper_phone):#电话号码
        uphone = UiUtil.find_element('input_element', 'uphone')
        DoElement.input(uphone, proper_phone)

    def input_uintroduce(self,proper_introduce):#物业简介
        uintroduce = UiUtil.find_element('input_element','uintroduce')
        DoElement.input(uintroduce,proper_introduce)

    def input_uificateid(self,proper_uificateid):#物业证书
        uificateid = UiUtil.find_element('input_element','uificateid')
        DoElement.input(uificateid,proper_uificateid)

    def click_do(self):
        userinfo_manage = UiUtil.find_element('select', 'user_manage')
        userinfo_manage.click()
        proper = UiUtil.find_element('select', 'proper')
        proper.click()

    def do_add_staff(self,proper_data):#增加内容测试
        self.switch_iframe()#切换iframe
        self.add_button()
        self.input_name(proper_data['proper_name'])
        self.input_passwd(proper_data['proper_passwd'])
        self.input_phone(proper_data['proper_phone'])
        self.input_uificateid(proper_data['proper_uificateid'])
        self.input_uintroduce(proper_data['proper_introduce'])
        self.add()

    def do_modify_staff(self,proper_data):#修改内容测试
        self.switch_iframe()#切换iframe
        self.index()
        self.modify_button()
        self.input_name(proper_data['proper_name'])
        self.input_passwd(proper_data['proper_passwd'])
        self.input_phone(proper_data['proper_phone'])
        self.input_uificateid(proper_data['proper_uificateid'])
        self.input_uintroduce(proper_data['proper_introduce'])
        time.sleep(3)
        self.modify()
        # self.driver.switch_to.default_content()#切换出iframe区域，以便做其他操作

    def do_select(self,proper_data):  # 选择查询条件并且输入查询内容，按查询按钮.
        self.switch_iframe()  # 切换iframe
        el1 = UiUtil.find_element('search', 'search_button')
        el1.click()
        el2 = UiUtil.find_element('search', 'select_info')
        el2.click()
        el3 = UiUtil.find_element('search','input')
        DoElement.input(el3,proper_data['v2'])
        el4 = UiUtil.find_element('search', 'search')
        el4.click()
        # self.driver.switch_to.default_content()#切换出iframe区域，以便做其他操作
