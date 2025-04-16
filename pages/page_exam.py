from selenium.webdriver.common.by import By
from base.page_base import BasePage
import time
from utils.yaml_utils import yaml_utils
class ExamPage(BasePage):
    def __init__(self):
        super().__init__()
        self.url = yaml_utils.read_url()

    def start_exam(self):
        self.open_url(self.url)

        self.click((By.XPATH, "//span[contains(text(),'学员账号')]"))
        self.click((By.PARTIAL_LINK_TEXT, "test0403 - 严格考试"))
        self.click((By.XPATH, "//span[contains(text(),'我已完成设备调试')]"))
        self.click((By.XPATH, "//span[contains(text(),'开始考试')]"))

        time.sleep(3)

        self.driver.execute_script("""
            var dialogs = document.querySelectorAll('.el-dialog__wrapper');
            if (dialogs.length > 0) {
                for (var i = 0; i < dialogs.length; i++) {
                    var buttons = dialogs[i].querySelectorAll('button');
                    for (var j = 0; j < buttons.length; j++) {
                        if (buttons[j].textContent.includes('确定')) {
                            buttons[j].click();
                            return;
                        }
                    }
                    var closeButtons = dialogs[i].querySelectorAll('.el-dialog__close');
                    if (closeButtons.length > 0) {
                        closeButtons[0].click();
                        return;
                    }
                }
            }
        """)
        time.sleep(2)

    def answer_question(self, question):
        q_type = question["type"]
        answer = question["answer"]

        if q_type == "single_choice":
            self.click((By.XPATH, f"//div[contains(text(),'{answer}')]"))

        elif q_type == "multiple_choice":
            for option in answer:
                self.click((By.XPATH, f"//div[contains(text(),'{option}')]"))
                time.sleep(0.5)

        elif q_type == "fill_blank":
            inputs = self.driver.find_elements(By.CSS_SELECTOR, ".el-input__inner")
            if inputs:
                inputs[0].click()
                inputs[0].send_keys(answer)

        elif q_type == "true_false":
            self.click((By.XPATH, f"//div[contains(text(),'{answer}')]"))

    def click_next(self):
        self.click((By.XPATH, "//span[contains(text(),'下一题')]"))
        time.sleep(1)

    def submit_exam(self):
        self.click((By.XPATH, "//span[contains(text(),'提交试卷')]"))
        time.sleep(0.5)
        self.click((By.XPATH, "//span[contains(text(),'确定')]"))
        time.sleep(3)

    def get_score_text(self):
        return self.find_element((By.XPATH, "//div[contains(text(),'用户得分')]")).text
