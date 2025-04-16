import pytest
from pages.page_question import QuestionPage
from utils.yaml_utils import yaml_utils

@pytest.fixture(scope="function")
def question_page(request):
    """创建并返回QuestionPage实例的Fixture"""
    page = QuestionPage()
    yield page
    # 测试结束后关闭浏览器
    page.quit()

@pytest.fixture(params=yaml_utils.read_question())
def question_data(request):
    """从YAML文件提供题库和AI出题数据的Fixture"""
    return request.param