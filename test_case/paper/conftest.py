import pytest
from pages.page_paper import PaperPage
from utils.yaml_utils import yaml_utils


@pytest.fixture(scope="function")
def exam_page(request):
    """创建并返回ExamPage实例的Fixture"""
    page = PaperPage()
    yield page
    # 测试结束后关闭浏览器
    page.quit()

# 只读创建考试的数据
@pytest.fixture(params=yaml_utils.read_paper()['add'])
def add_exam_data(request):
    return request.param

# 只读删除考试的数据
@pytest.fixture(params=yaml_utils.read_paper()['delete'])
def delete_exam_data(request):
    return request.param

#只读修改考试的数据
@pytest.fixture(params=yaml_utils.read_paper()['update'])
def update_exam_data(request):
    return request.param
