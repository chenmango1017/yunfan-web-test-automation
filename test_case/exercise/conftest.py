import pytest
from utils.yaml_utils import yaml_utils

@pytest.fixture
def exercise_page():
    from pages.page_exercise import ExercisePage
    page = ExercisePage()
    yield page
    page.quit()

@pytest.fixture(scope="session")
def exercise_data():
    """从 YAML 读取所有练习题库配置"""
    return yaml_utils.read_exercise()
"""钩子函数以pytest开头"""
def pytest_generate_tests(metafunc):
    """
    动态生成参数化的测试用例 —— 自动从 YAML 中读取题库名和版本
    """
    if "question_bank_name" in metafunc.fixturenames and "version" in metafunc.fixturenames:
        data = yaml_utils.read_exercise()
        param_list = [
            (qb["name"], qb.get("version", "default"))
            for qb in data.get("question_banks", [])
        ]
        metafunc.parametrize("question_bank_name,version", param_list)
