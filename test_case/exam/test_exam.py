import pytest
import allure
from utils.logger_utils import logger
from datetime import datetime
@pytest.mark.exam_test
class TestExam:
    @allure.feature("考试功能")
    @allure.story("考试答题与评分")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_exam_score(self, exam_page, exam_data):
        """考试答题与评分测试"""
        # 获取当前时间
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 在Allure报告中附加当前时间
        allure.attach(f"当前时间: {now_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        # 记录测试开始
        allure.dynamic.title(f"测试考试: {exam_data['title']}")
        allure.dynamic.description(f"参与考试 {exam_data['title']} 并验证得分")
        logger.info(f"====== 开始考试测试: {exam_data['title']} ======")

        try:
            # 开始考试
            exam_page.start_exam()

            # 回答所有题目
            for question in exam_data["questions"]:
                logger.info(f"回答问题: {question.get('question_text', '未知问题')}")
                exam_page.answer_question(question)
                exam_page.click_next()

            # 提交考试
            exam_page.submit_exam()

            # 获取分数并验证
            score_text = exam_page.get_score_text()
            expected_score = f"用户得分：{exam_data['expected_score']}"

            assert score_text == expected_score, f"得分验证失败，实际:{score_text}，预期:{expected_score}"

            logger.info(f"====== 考试测试成功: {exam_data['title']} ======")
        except Exception as e:
            logger.error(f"考试测试失败: {e}")
            # 在 Allure 报告中添加错误附件
            allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)
            # 截图
            exam_page.save_screenshot(f"exam_failure_{exam_data['title']}")
            # 重新抛出异常，让测试失败
            raise