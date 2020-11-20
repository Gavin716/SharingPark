import time
import os

import requests
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from selenium.webdriver.common.by import By

from zFrame_templates.tools.util import LogUtil,FileUtil,DBUtil,TimeUtil

class UiUtil:
    """
    UI 相关操作的工具封装包括：页面元素查找、driver生成、内容的输入、
    """
    driver = None
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'ui_util'))
    mouse = PyMouse()
    keyboard = PyKeyboard()

    @classmethod
    def get_driver(cls):
        from selenium import webdriver
        try:
            browser = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'browser')
            base_url = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'base_url')
            if cls.driver is None:
                cls.driver = getattr(webdriver, browser)()
                cls.driver.implicitly_wait(1)
                cls.driver.maximize_window()
                cls.driver.get(base_url)
        except:
            cls.logger.error('浏览器对象生成错误，请检查配置文件')
        return cls.driver

    @classmethod
    def find_elment(cls, section, option):  #### 需对比老师的查看 find element 方法写在哪里了
        """
        查找元素的方法
        :param section: inspector.ini文件中的节点
        :param option:  inspector.ini文件中对应节点下的 值     定位方式  以及定位元素
        :return:
        """
        try:
            element_attr = FileUtil.get_ini_section('..\\conf\\inspector.ini', section)
            for element in element_attr:
                if option in element.keys():
                    attr = eval(element[option])
                    return cls.driver.find_element(getattr(By, attr[0]), attr[1])
        except:
            return None

    @classmethod
    def input(cls, element, value):
        """
        对文本输入框执行点击、清理和输入值的动作
        :param element:文本元素对象
        :param value:向文本框输入的值
        :return:无
        """
        element.click()
        element.clear()
        element.send_keys(value)

    @classmethod
    def click(cls, element):
        """
        点击某个元素
        :param element:任何一个元素对象
        :return:无
        """
        element.click()

    @classmethod
    def select_ro(cls, element):
        """
        随机选择下拉框中的某一项
        :param element: 下拉框元素对象
        :return: 无
        """
        from selenium.webdriver.support.select import Select
        import random
        random_index = random.randint(0, len(Select(element).options) - 1)
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

#*********************************  图像识别方法  ***************************************************
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

        similarity = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'similarity')
        if max < float(similarity):
            return -1 ,-1

        x = max_loc[0] + int(template.shape[1] / 2)
        y = max_loc[1] + int(template.shape[0] / 2)
        return x, y

    @classmethod
    def click_image(cls, target):    ##输入图像并对找到的图像
        """
        单击一张图片
        :param target:
        :return:
        """
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y)

    @classmethod
    def double_click_image(cls, target):   ##查找提供的图像  找到后并双击
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y, n=2)

    @classmethod
    def input_image(cls, target, msg):     ##输入图像进行图像识别
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.keyboard.type_string(msg)

    @classmethod
    def select_image(cls, target, count):  #下拉框图像识别后选择某一个元素
        # 点击这个下拉框
        cls.click_image(target)
        # count次执行向下键
        for i in range(count):
            cls.keyboard.press_key(cls.keyboard.down_key)
        # 回车
        cls.keyboard.press_key(cls.keyboard.enter_key)

    @classmethod
    def screen_shot(cls, driver, path):     ##拍摄截图  用于产生bug时记录
        driver.get_screenshot_as_file(path)

class APIUtil:

    @classmethod
    def get_session(cls):
        session = requests.session()  ##获取session
        session.get('http://172.16.13.162:8080/SharedParkingPlace/image')
        login_url= FileUtil.get_ini_value('http://172.16.13.162:8080/SharedParkingPlace/image','api','login_url')
        session.get(login_url)
        print(session)
        return session

    @classmethod
    def request(cls, method, url, data=None):
        """
        发送请求获得响应
        :param method: 请求方式
        :param url: 请求url
        :param data: 请求数据
        :return: 响应结果
        """
        session = cls.get_session()     ##  调用上面获取的session   发起接口请求
        resp = getattr(session, method)(url, params = data)
        return resp

    @classmethod
    def assert_api(cls, test_info):
        """
          对输入的uri 进行请求方式method的验证并将返回值于 参数中的断言部分进行对比
        :param test_info:  接口测试相关的参数 url、请求方式、输入参数、 断言
        :return: 无
        """
        for info in test_info:       ##对上面接口请求返回值进行断言
            resp = APIUtil.request(info['request_method'], info['uri'], info['params'])
            Assert.assert_equal(resp.text, info['expect'])

class Assert:

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        print(test_result)




if __name__ == '__main__':
    # data =[{'params': {'barcode': '11111111'}, 'expect': '[{"createtime":"<option value=\'40\'>尺码:40,剩余:0件</option><option value=\'30\'>尺码:30,剩余:1件</option><option value=\'20\'>尺码:20,剩余:0件</option><option value=\'10\'>尺码:10,剩余:1件</option>##1.0##68","goodsserial":"M3Q1498B","goodsname":"米乐果后开连衣裙","barcode":"11111111","unitprice":89.0}]', 'caseid': 'sales_scan_barcode_01', 'module': 'sales', 'type': 'api', 'desc': '合法条码请求', 'version': 'V1.0', 'uri': 'http://192.168.127.150:8080/WoniuSales1.4/sell/barcode', 'request_method': 'post'}, {'params': {'barcode': 'adfasf'}, 'expect': '[]', 'caseid': 'sales_scan_barcode_02', 'module': 'sales', 'type': 'api', 'desc': '非法条码请求', 'version': 'V1.0', 'uri': 'http://192.168.127.150:8080/WoniuSales1.4/sell/barcode', 'request_method': 'post'}, {'params': {'barcode': ''}, 'expect': '[]', 'caseid': 'sales_scan_barcode_03', 'module': 'sales', 'type': 'api', 'desc': '空条码请求', 'version': 'V1.0', 'uri': 'http://192.168.127.150:8080/WoniuSales1.4/sell/barcode', 'request_method': 'post'}]
    APIUtil.get_session()
    # pass