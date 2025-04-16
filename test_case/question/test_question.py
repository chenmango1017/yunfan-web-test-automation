import pytest
import allure
from datetime import datetime
from utils.logger_utils import logger

@pytest.mark.question_test
class TestQuestion:
    @allure.feature("题库管理")
    @allure.story("创建题库并使用AI生成题目")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_generate_questions(self, question_page, question_data):
        """创建题库并使用AI生成题目的测试"""
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 获取测试数据
        bank_name = question_data.get("title", "测试题库")
        category = question_data.get("category", "职业资格")
        knowledge_point = question_data.get("knowledge_point", "数据库")
        description = question_data.get("description", "题库简介")
        generate_demand = question_data.get("generate_demand", "数据库知识")
        question_count = question_data.get("question_count", 5)
        chapter = question_data.get("chapter", "新章节")
        difficulty = question_data.get("difficulty", "简单")

        # 记录测试开始
        allure.dynamic.title(f"测试创建题库并生成题目: {bank_name}")
        allure.dynamic.description(f"创建题库 {bank_name} 并使用AI生成关于 {generate_demand} 的题目")

        # 在Allure报告中附加当前时间
        allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"====== 开始题库创建和题目生成测试: {bank_name} ======")

        try:
            # 打开登录页面
            question_page.open_url(question_page.url)

            # 导航到题库管理页面
            question_page.navigate_to_question_bank()

            # 创建新题库
            assert question_page.create_question_bank(
                bank_name=bank_name,
                category=category,
                knowledge_point=knowledge_point,
                description=description
            ), f"创建题库 {bank_name} 失败"

            # 导航到智能出题页面
            question_page.navigate_to_ai_question()

            # 使用AI生成题目
            question_page.generate_questions(generate_demand, question_count)

            # 将生成的题目导入题库
            question_page.import_to_question_bank(bank_name, chapter, difficulty)

            # 导航到学员刷题页面
            question_page.navigate_to_student_practice()

            # 验证题库是否存在
            assert question_page.verify_question_bank_exists(bank_name), f"在学员刷题页面未找到题库: {bank_name}"

            logger.info(f"====== 题库创建和题目生成测试成功: {bank_name} ======")

        except Exception as e:
            logger.error(f"题库创建和题目生成测试失败: {e}")

            # 在 Allure 报告中添加错误附件
            allure.attach(str(e), "异常信息", attachment_type=allure.attachment_type.TEXT)

            # 截图
            question_page.save_screenshot(f"question_test_failure_{bank_name}")

            # 重新抛出异常，让测试失败
            raise