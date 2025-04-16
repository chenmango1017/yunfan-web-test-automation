import pytest
import allure
from datetime import datetime
from utils.logger_utils import logger

@pytest.mark.exercise_test
class TestExercise:\

    @allure.feature("练习功能")
    @allure.story("顺序练习")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sequential_exercise(self, exercise_page, exercise_data, question_bank_name, version):
        """顺序练习测试"""

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        allure.dynamic.title(f"测试顺序练习: {question_bank_name} - {version}")
        allure.dynamic.description(f"使用题库 {question_bank_name}（版本: {version}）进行顺序练习测试")
        allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"====== 开始顺序练习测试: {question_bank_name}（版本: {version}） ======")

        try:
            # 从 exercise_data 中找到当前测试用的题库
            question_bank = next(
                (qb for qb in exercise_data["question_banks"]
                 if qb["name"] == question_bank_name and qb.get("version", "default") == version),
                None
            )

            if not question_bank:
                pytest.fail(f"题库未找到: {question_bank_name}（版本: {version}）")

            exercise_page.start_exercise(question_bank_name)
            exercise_page.complete_all_questions(question_bank["questions"])
            exercise_page.end_exercise()

            assert exercise_page.verify_results(), "练习结果验证失败"
            logger.info(f"====== 顺序练习测试成功: {question_bank_name}（版本: {version}） ======")

        except Exception as e:
            logger.error(f"顺序练习测试失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            allure.attach(traceback.format_exc(), "异常堆栈", allure.attachment_type.TEXT)
            exercise_page.save_screenshot(f"exercise_failure_{question_bank_name}_{version}")
            raise
