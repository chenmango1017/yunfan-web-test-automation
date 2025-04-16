from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from base.page_base import BasePage
from utils.yaml_utils import yaml_utils
from utils.logger_utils import logger
import allure
from time import sleep
import math

class ExercisePage(BasePage):
    # 练习页面定位器
    STUDENT_ACCOUNT = (By.XPATH, "//span[contains(text(),'学员账号')]")
    PRACTICE_OPTION = (By.XPATH, "//li[contains(text(),'刷题训练')]")
    MY_QUESTION_BANK = (By.XPATH, "//div[contains(text(),'我的题库')]")
    SEQUENTIAL_PRACTICE = (By.XPATH, "//a[contains(., '顺序练习')]")
    NEXT_QUESTION = (By.XPATH, "//span[text()='下一题']")
    END_TRAINING = (By.XPATH, "//span[contains(text(),'结束训练')]")
    CONFIRM_BUTTON = (By.XPATH, "//span[contains(text(),'确定')]")

    # 结果页面定位器
    ACCURACY_RATES = (By.CSS_SELECTOR, "span[data-v-49f4b24e].t2")
    CORRECT_ANSWERS = (By.CSS_SELECTOR, ".el-icon-success.dt-item")
    ANSWERED_QUESTIONS = (By.CSS_SELECTOR, ".el-icon-info.dt-item")
    TOTAL_QUESTIONS = (By.CSS_SELECTOR, ".el-icon-circle-plus.dt-item")

    def __init__(self):
        super().__init__()
        self.url = yaml_utils.read_url()
        self.answer_data = yaml_utils.read_exercise()
        logger.info("初始化练习页面")

    @allure.step("开始练习")
    def start_exercise(self, question_bank_name="AIAI"):
        """开始指定题库的顺序练习"""
        logger.info("打开练习页面")
        self.open_url(f"{self.url}/pages/exam")

        # 选择学员账号
        logger.info("选择学员账号")
        self.click(self.STUDENT_ACCOUNT)

        # 选择刷题训练
        logger.info("选择刷题训练")
        self.click(self.PRACTICE_OPTION)

        # 选择我的题库
        logger.info("选择我的题库")
        self.click(self.MY_QUESTION_BANK)

        # 选择指定题库
        question_bank_locator = (By.PARTIAL_LINK_TEXT, question_bank_name)
        logger.info(f"选择题库: {question_bank_name}")
        self.click(question_bank_locator)

        # 选择顺序练习
        logger.info("选择顺序练习")
        self.click(self.SEQUENTIAL_PRACTICE)

        # 等待页面完全加载
        logger.info("等待页面加载")
        sleep(10)
        self.save_screenshot("exercise_started")

    @allure.step("回答题目 {q_no}")
    def answer_question(self, q_no, q_type, ans):
        """回答指定题号的题目"""
        logger.info(f"正在作答第 {q_no} 题，类型：{q_type}")
        allure.attach(f"题号: {q_no}, 类型: {q_type}, 答案: {ans}", "题目信息", allure.attachment_type.TEXT)

        try:
            if q_type in ["单选题", "判断题"]:
                option_locator = (By.XPATH, f"//div[contains(text(),'{ans}')]")
                logger.info(f"点击选项: {ans}")
                self.click(option_locator)

            elif q_type == "多选题":
                for option in ans:
                    option_locator = (By.XPATH, f"//div[contains(text(),'{option}')]")
                    logger.info(f"点击多选项: {option}")
                    self.click(option_locator)

            elif q_type in ["简答题", "填空题"]:
                logger.info(f"{q_type} 跳过作答，仅点击下一题")

            # 每题点击"下一题"
            sleep(0.5)
            self.click(self.NEXT_QUESTION)
            return True

        except Exception as e:
            logger.error(f"第 {q_no} 题作答出错: {e}")
            self.save_screenshot(f"error_q{q_no}")
            return False
    @allure.step("完成所有题目")
    def complete_all_questions(self, questions):
        """完成所有题目的作答"""
        logger.info("开始作答所有题目")

        total_questions = len(questions)
        completed_questions = 0

        for q_no in questions:
            q_type = questions[q_no]["type"]
            ans = questions[q_no]["answer"]

            if self.answer_question(q_no, q_type, ans):
                completed_questions += 1

        logger.info(f"完成作答 {completed_questions}/{total_questions} 题")
        allure.attach(f"{completed_questions}/{total_questions}", "完成题数", allure.attachment_type.TEXT)

    @allure.step("结束练习")
    def end_exercise(self):
        """结束练习并获取结果"""
        logger.info("点击结束训练")
        self.click(self.END_TRAINING)

        logger.info("确认结束")
        self.click(self.CONFIRM_BUTTON)
        sleep(10)

        # 截图保存结果
        self.save_screenshot("exercise_results")
    def set_question_bank(self, question_bank_data):
        """设置当前要使用的题库数据"""
        self.answer_data = question_bank_data

    @allure.step("验证练习结果")
    def verify_results(self):
        """验证练习结果的准确性"""
        logger.info("获取练习结果")

        # 获取正确率信息
        accuracy_rates = self.wait.until(
            EC.presence_of_all_elements_located(self.ACCURACY_RATES)
        )

        answered_correctly_rate = int(accuracy_rates[0].text)  # "已答正确率"
        overall_correctly_rate = int(accuracy_rates[1].text)   # "总体正确率"

        # 获取其他统计数据
        correct_answers = self.find_element(self.CORRECT_ANSWERS).text
        answered_questions = self.find_element(self.ANSWERED_QUESTIONS).text
        total_questions = self.find_element(self.TOTAL_QUESTIONS).text

        # 解析数字
        correct_num = int(correct_answers[3])  # 假设是格式如"正确: 5"
        answered_num = int(answered_questions[3])  # 假设是格式如"已答: 8"
        total_num = int(total_questions[3:5])  # 假设是格式如"题目总数: 10"

        # 计算预期正确率
        expected_answered_rate = int(round(correct_num / answered_num, 2) * 100)
        expected_overall_rate = int(math.floor((correct_num / total_num) * 100))

        # 记录结果
        result_data = {
            "正确题数": correct_num,
            "已答题数": answered_num,
            "总题数": total_num,
            "预期已答正确率": expected_answered_rate,
            "实际已答正确率": answered_correctly_rate,
            "预期总体正确率": expected_overall_rate,
            "实际总体正确率": overall_correctly_rate
        }

        for key, value in result_data.items():
            logger.info(f"{key}: {value}")
            allure.attach(str(value), key, allure.attachment_type.TEXT)

        # 断言验证
        try:
            assert answered_correctly_rate == expected_answered_rate, f"已答正确率不匹配，预期 {expected_answered_rate}%, 实际 {answered_correctly_rate}%"
            assert overall_correctly_rate == expected_overall_rate, f"总体正确率不匹配，预期 {expected_overall_rate}%, 实际 {overall_correctly_rate}%"
            logger.info("验证结果: 通过")
            return True
        except AssertionError as e:
            logger.error(f"验证结果: 失败 - {e}")
            return False

    @allure.step("执行完整练习流程")
    def perform_complete_exercise(self, question_bank_name="AIAI"):
        """执行从开始到结束的完整练习流程"""
        try:
            self.start_exercise(question_bank_name)
            self.complete_all_questions()
            self.end_exercise()
            result = self.verify_results()
            logger.info(f"练习流程完成，结果验证: {'通过' if result else '失败'}")
            return result
        except Exception as e:
            logger.critical(f"练习过程发生异常: {e}")
            self.save_screenshot("exercise_error")
            return False
        finally:
            logger.info("关闭浏览器")
            self.quit()