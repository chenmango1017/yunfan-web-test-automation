import pytest
from pages.page_login import LoginPage
from utils.yaml_utils import yaml_utils


@pytest.fixture(scope="function")
def login_page(request):
    """创建并返回LoginPage实例的Fixture"""
    page = LoginPage()
    yield page
    # 测试结束后关闭浏览器
    page.quit()

"""request 是 pytest 内置的 fixture，当 @pytest.fixture 里使用 params=... 
传入多个参数时，pytest 会自动遍历这些参数，并且 request.param 会返回当前测试用例使用的那个参数"""
@pytest.fixture(params=yaml_utils.read_yaml())
def login_data(request):
    """从YAML文件提供登录数据的Fixture"""
    return request.param
