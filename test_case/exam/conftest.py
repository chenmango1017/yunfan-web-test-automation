
from pages.page_exam import ExamPage
from utils.yaml_utils import yaml_utils
import pytest

@pytest.fixture(scope="function")
def exam_page(request):
    """创建并返回ExamPage实例的Fixture"""
    page = ExamPage()
    yield page
    # 测试结束后关闭浏览器
    page.quit()

@pytest.fixture(params=yaml_utils.read_exam())
def exam_data(request):
    """从YAML文件提供考试数据的Fixture"""
    return request.param
