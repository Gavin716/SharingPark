import unittest
from tingna.tools.util import FileUtil
from HTMLTestRunner.HTMLTestRunner import HTMLTestRunner

class Ddttuistart:

    def start(self,path):
        """
        执行已经写好的测试用例
        :param path:   测试用例存放的路径
        :return:
        """
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()   ##加载多个模块内的测试用例
        test_class_info = FileUtil.get_txt_line(path)    ## 使用 读取txt的方式  读取  并使用去除 #开头的行     #开头的为备注行
        tests = loader.loadTestsFromNames(test_class_info)  ###读取conf里面的 测试类路径下的测试用例 依次进行执行

        suite.addTests(tests)
        with open('report.html','w') as file:
            runner = HTMLTestRunner(stream=file,verbosity=2)
            runner.run(suite)


if __name__ == '__main__':
    Ddttuistart().start("..\\conf\\case_class_path.conf")
