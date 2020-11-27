import pymysql
import xlrd
import os

class LogUtil:

    logger = None

    @classmethod
    def get_ctime(cls):

        import time             #适用于各种文件
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_ctime1(cls):
        import time
        return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())  # 设置时间，获取日志记录错误时的实时时间

    @classmethod
    def get_logger(cls, name):

        import logging
        if cls.logger is None:
            # 获取日志生成器对象
            cls.logger = logging.getLogger(name)
            # 定义获取信息的级别
            cls.logger.setLevel(level=logging.INFO)
            # 如果日志目录不存在则创建
            if not os.path.exists('../logs'):
                os.mkdir('../logs')
            # 创建logger的文件句柄与规定的文件关联
            handler = logging.FileHandler('..\\logs\\'+cls.get_ctime()+'.log', encoding='utf8')
            # 定义信息的格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            cls.logger.info('*****************************************************\n')

        return cls.logger

class DBUtil:

    logger = LogUtil.get_logger(os.path.join(os.getcwd(),'util'))

    def __init__(self,option):
        self.db_info = eval(FileUtil.get_ini_value("../conf/base.ini", 'mysql', option))

    def conn_db(self, db_info):  # 元组的形式
        conn = None
        try:
            conn = pymysql.connect(host=db_info[0], database=self.db_info[1], user=self.db_info[2], password=self.db_info[3],
                                   charset=self.db_info[4])
        except:
            self.logger.error("数据库连接失败")
        finally:
            return conn

    def query_one(self, sql):

        conn = self.conn_db(self.db_info)
        cur = conn.cursor()#游标
        result = None
        try:
            cur.execute(sql)  # 执行sql语句
            result = cur.fetchone()
        except:
            self.logger.error('查询失败')
        finally:
            cur.close()#关闭游标
            conn.close()#关闭
            return result
    def query_all(self, sql):
        conn = self.conn_db(self.db_info)
        cur = conn.cursor()  # 游标
        result = None
        try:
            cur.execute(sql)  # 执行sql语句
            result = cur.fetchall()
        except:
            self.logger.error('查询失败')
        finally:
            cur.close()  # 关闭游标
            conn.close()  # 关闭
            return result

    def update(self,sql):
        conn = self.conn_db(self.db_info)
        cur = conn.cursor()
        conn.commit()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except:
            self.logger.error("查询失败")
        finally:
            cur.close()
            conn.close()
            print(result)


class FileUtil:

    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'util'))

    @classmethod
    def get_txt(cls,path):
        with open(path,encoding='utf8') as rf:
            contents = rf.readlines()
            di = {}
            for content in contents:
                content.strip()
                datas = content.split(',')
                for d in datas:
                    d.strip()
                    d = d.split('=')
                    di[d[0]] = d[1]

            return di


    @classmethod
    def get_txt1(cls, path):
        with open(path, encoding='utf8') as rf:
            contents = rf.readlines()
            li = []
            for content in contents:
                if content.startswith('#'):
                    continue
                else:
                    c = content.strip()
                    li.append(c)
            return li


    def get_json(self,path):
        # logger = LogUtil.get_log(os.path.join(os.getcwd(), 'util'))
        import json
        content = None #文件路径不知道有没有问题，所以先设置文件内容为None
        try:
            with open(path,encoding="utf8") as rf: #针对可能出错的文件路径进行异常捕获
                content = json.load(rf)
            self.logger.info("文件读取正确")#在日志中生成信息
        except:
            self.logger.error("文件路径错误")
        finally:
            return content


            #该解析excel文件的方法的path的路径在woniutest--testdata/test_data_path.ini里面。
    def get_excel(self,path,section,option):
        params = eval(FileUtil.get_ini_value(path,section,option))
        workbook = xlrd.open_workbook(params['path'])
        # 读具体的某一页，由section决定，比如login或者customer
        sheet_content = workbook.sheet_by_name(params['sheet_name'])
        #读取xls表的首页封面，获取项目名称和版本信息的第一步
        case_sheet_content = workbook.sheet_by_name(params['case_sheet_name'])
        #如果excel表格测试内容中有新的列加入，要引用此处的test_rews。
        test_rows = sheet_content.row_values(0)#测试页面。打印出来是：['id', '模块', '测试类型', '用例描述', '步骤', '期望结果']

        case_rows = case_sheet_content.row_values(0)#caseinfo页面，打印出来是：['项目名称', '版本']


        project_name_index = case_rows.index(params['project_name'])#获取项目名称的下标
        project_name = case_sheet_content.cell(1, project_name_index).value
        version_index = case_rows.index(params['version'])#获取版本的下标
        version = case_sheet_content.cell(1,version_index).value
        url_index = test_rows.index(params['url'])
        request_method_index = test_rows.index(params['request_method'])
        data_col_index = test_rows.index(params['target_content'])#通过列表内容--登录数据来获取对应的下标
        expect_col_index = test_rows.index(params['except_content'])#通过列表内容--期望数据来获取对应的下标
        test_li = []
        for i in range(params['start_row'],params['end_row']):#table.nrows统计一个表格有多少行
            test_data = sheet_content.cell(i,data_col_index).value #先取出用户名、密码和验证码所在的那一列
            result = sheet_content.cell(i,expect_col_index).value #再取出期望值所在的那一列
            url = sheet_content.cell(i,url_index).value
            request_method = sheet_content.cell(i,request_method_index).value
            content = test_data.split("\n")#打印后发现，里面含有“\n”，可以用它来切割一下，就成了["username=admin"]等的列表
            di = {}
            data = {}  # 用来接收以上两种数据，放进字典里面
            di['project_name'] = project_name
            di['version'] = version
            di['api_url'] = url
            di['request_method'] = request_method
            for data_dict in content:
                content = data_dict.split("=")#利用等号来切割，就变成了['username', 'admin']等的列表
                data_key = content[0] #利用列表坐标来取出来要作为key的值
                data_value = content[1]#利用列表坐标来取出来要作为value的值
                data[data_key] = data_value
            di['params'] = data
            di['expect'] = result#给期望值赋一个"expect"键
            test_li.append(di)#用列表接收
        return test_li




    @classmethod
    def get_ini_value(cls,path,section,option):#从ini文件中读取某个指定的键对应的值
        import configparser
        cp = configparser.ConfigParser()
        value = None
        try:
            cp.read(path,encoding='utf-8-sig')
            value = cp.get(section,option)
        except:
            cls.logger.error("读取配置文件错误")
        return value


    @classmethod
    def get_ini_section(cls,path,section):
        import configparser
        cp = configparser.ConfigParser()
        li = []
        try:
            cp.read(path, encoding='utf-8-sig')
            temp = cp.items(section)
            for t in temp:
                di = {}
                di[t[0]] = t[1]
                li.append(di)
        except:
            cls.logger.error("读取配置文件错误")
        finally:
            return li


if __name__ == '__main__':
    result = FileUtil().get_excel('../testdata/test_parking_info.ini','property','staff_search_ui')
    print(result)