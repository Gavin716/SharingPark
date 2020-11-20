
from sharingparktest.tools.util import FileUtil
from sharingparktest.tools.lib_util import APIutil

class LessorAPI():

    def test_add_stall(self):
        test_info = FileUtil.get_test_info_api("..\\conf\\test_info.ini", "lessor", "lessor_api")
        APIutil.assert_api(test_info)



if __name__ == '__main__':
    test = LessorAPI()
    test.test_add_stall()