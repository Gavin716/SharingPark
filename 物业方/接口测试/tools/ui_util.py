
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from selenium.webdriver.common.by import By
import os
from woniutest.tools.util import FileUtil
from woniutest.tools.util import LogUtil

import requests

class ApiUtil:

    @classmethod
    def get_session_post(cls):
        session = requests.session()#配置文件路径：../conf/base.ini
        login_url = FileUtil.get_ini_value('../conf/base.ini','api','login_url')
        login_data = eval(FileUtil.get_ini_value('../conf/base.ini', 'api', 'login_data'))
        session.post(login_url,login_data)
        return session

    @classmethod
    def get_session_get(cls):
        session = requests.session()  # 配置文件路径：../conf/base.ini
        session.get('http://172.16.13.162:8080/SharedParkingPlace/image')
        login_url = FileUtil.get_ini_value('../conf/base.ini', 'api', 'parking_url')
        res = session.get(login_url)
        return session



    @classmethod
    def request(cls,method,url,data):
        session = cls.get_session_get()
        resp = getattr(session,method)(url,params=data)
        return resp

    @classmethod
    def assert_api(cls,test_info):
        for info in test_info:
            resp = ApiUtil.request(info['request_method'],info['api_url'],info['params'])
            Assert.assert_equal(resp.text,info['expect'])



class DoElement:
    @classmethod
    def input(cls, ele, value):
        ele.click()
        ele.clear()
        ele.send_keys(value)

class UiUtil:
    mouse = PyMouse()
    keyboard = PyKeyboard()
    driver = None
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'ui_util'))


    @classmethod
    def get_driver(cls):
        from selenium import webdriver
        try:
            browser = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'browser')
            base_url = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'base_url')
            if cls.driver is None:
                cls.driver = getattr(webdriver, browser)()
                cls.driver.implicitly_wait(5)
                cls.driver.maximize_window()
                cls.driver.get(base_url)
        except:
            cls.logger.error('浏览器对象生成错误，请检查配置文件')
        finally:
            return cls.driver


    @classmethod
    def find_element(cls, section, option):
        element_attr = FileUtil.get_ini_section('../conf/inspector.ini', section)
        for element in element_attr:
            if option in element.keys():
                attr = eval(element[option])
                return cls.driver.find_element(getattr(By, attr[0]), attr[1])


    @classmethod
    def select_ro(cls, element):
        """
        随机选择下拉框中的某一项
        :param element: 下拉框元素对象
        :return: 无
        """
        from selenium.webdriver.support.select import Select
        import random
        random_index = random.randint(0, len(Select(element).options)-1)
        Select(element).select_by_index(random_index)

    @classmethod
    def select_by_text(cls, element, text):
        """
        根据下拉文本选择该项
        :param element: 下拉框元素对象
        :param text: 可见的文本
        :return:无
        """
        from selenium.webdriver.support.select import Select
        Select(element).select_by_visible_text(text)

    @classmethod
    def is_element_present(cls, driver, how, what):
        """
        该方法用于判断某个元素是否存在
        :return:
        """
        try:
            print(how, what)
            driver.find_element(how, what)
            return True
        except:
            cls.logger.error(f'没有找到方式为{how}值为{what}的元素')
            return False

    @classmethod
    def find_image(cls, target):

        image_path = '..\\image'
        screen_path = os.path.join(image_path,'screen.png')
        from PIL import ImageGrab
        ImageGrab.grab().save(screen_path)

        # 读取大图对象
        import cv2
        screen = cv2.imread(screen_path)
        # 读取小图对象
        template = cv2.imread(os.path.join(image_path,target))
        # 进行模板匹配，参数包括大图对象、小图对象和匹配算法
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        # 获取匹配结果
        min, max, min_loc, max_loc = cv2.minMaxLoc(result)

        similarity = FileUtil.get_ini_value('..\\conf\\base.ini', 'imagematch', 'similarity')
        if max < float(similarity):
            return -1 ,-1

        x = max_loc[0] + int(template.shape[1] / 2)
        y = max_loc[1] + int(template.shape[0] / 2)
        return x, y

    @classmethod
    def screen_shot(cls, driver, path):
        driver.get_screenshot_as_file(path)

    @classmethod
    def click_image(cls, target):

        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y)

    @classmethod
    def double_click_image(cls, target):
        """
        双击一张图片
        :param target:
        :return:
        """
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y, n=2)

    @classmethod
    def input_image(cls, target, msg):
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.keyboard.type_string(msg)

    @classmethod
    def select_image(cls, target, count):
        """
        匹配图片选择下拉框
        :param target:
        :param count:
        :return:
        """
        # 点击下拉框
        cls.click_image(target)
        # count次执行键盘操作
        for i in range(count):
            cls.keyboard.press_key(cls.keyboard.down_key)
        cls.keyboard.press_key(cls.keyboard.enter_key)

class Assert:

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        print(test_result)

if __name__ == '__main__':
    # test_info = FileUtil().get_excel('../testdata/test_info.ini', 'customer', 'add_customer_api')
    # ApiUtil.assert_api(test_info)
    test = ApiUtil
    test.get_session_get()
