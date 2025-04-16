from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.page_base import BasePage
from utils.logger_utils import logger
import allure
from time import sleep

class PaperPage(BasePage):
    # 考试创建相关定位器
    ADMIN_MENU = (By.XPATH, '//span[contains(text(),"管理员")]')
    CREATE_EXAM_BUTTON = (By.XPATH, '//div[contains(text(),"创建考试")]')
    SCIENCE_SUBJECT_MARKER = (By.XPATH, '//div[contains(text(),"理科")]')
    SELECT_BUTTONS = (By.XPATH, '//button[./span[contains(text(),"选定")]]')
    EXAM_NAME_INPUT = (By.XPATH, '//label[contains(text(), "考试名称")]/following::input[1]')
    START_TIME_INPUT = (By.XPATH, '//input[@placeholder="开始时间"]')
    START_DATE_INPUT = (By.XPATH, '//input[@placeholder="开始日期"]')
    END_DATE_INPUT = (By.XPATH, '//input[@placeholder="结束日期"]')
    CONFIRM_BUTTON = (By.XPATH, '//span[contains(text(),"确定")]')
    SAVE_BUTTON = (By.XPATH, '//span[contains(text(),"保存")]')
    MESSAGE_BOX = (By.CLASS_NAME, "el-message-box")
    MESSAGE_TEXT = (By.CLASS_NAME, "el-message-box__message")
    CONFIRM_DIALOG_BUTTON = (By.XPATH, '//div[contains(@class, "el-message-box")]//span[contains(text(),"确")]')
    STATUS_DROPDOWN = (By.CSS_SELECTOR, "span.el-dropdown-link")
    # 新增成功消息通知定位器
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".el-message.el-message--success")
    SUCCESS_MESSAGE_TEXT = (By.CSS_SELECTOR, ".el-message.el-message--success p")
    # 发布考试相关定位器
    PUBLISH_BUTTON = (By.XPATH, "//li[contains(text(),'发布考试')]")

    # 学员视图相关定位器
    CLOUD_EXAM_LINK = (By.XPATH, '//div[contains(text(),"云帆考试")]')
    STUDENT_HOME_LINK = (By.XPATH, "//li[contains(text(),'学员首页')]")
    EXAM_LINKS = (By.CSS_SELECTOR, "a.d-link")

    def __init__(self):
        super().__init__()
        self.url = "https://exam.yfhl.net/pages/login/login"
        logger.info("初始化考试页面")

    def is_element_visible(self, locator, timeout=3):
        """检查元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("打开管理员面板")
    def open_admin_panel(self):
        """打开管理员面板"""
        logger.info("打开管理员面板")
        self.open_url(self.url)
        self.click(self.ADMIN_MENU)

    @allure.step("创建新考试")
    def create_exam(self, exam_name, start_date, end_date):
        """创建新的考试"""
        logger.info(f"开始创建考试: {exam_name}")
        allure.attach(f"考试名称: {exam_name}\n开始日期: {start_date}\n结束日期: {end_date}",
                      "考试信息", allure.attachment_type.TEXT)

        # 点击创建考试按钮并等待页面加载
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.CREATE_EXAM_BUTTON)).click()
        wait.until(EC.presence_of_element_located(self.SCIENCE_SUBJECT_MARKER))

        # 选择第一个选项
        buttons = self.driver.find_elements(*self.SELECT_BUTTONS)
        button = buttons[0]
        self.driver.execute_script("arguments[0].click();", button)
        sleep(2)

        # 输入考试名称
        exam_name_field = self.find_element(self.EXAM_NAME_INPUT)
        exam_name_field.clear()
        exam_name_field.send_keys(exam_name)

        # 设置考试日期
        self.click(self.START_TIME_INPUT)
        sleep(3)

        # 输入开始日期
        start_date_field = self.find_element(self.START_DATE_INPUT)
        start_date_field.click()
        start_date_field.clear()
        start_date_field.send_keys(start_date)
        sleep(2)

        # 输入结束日期
        end_date_field = self.find_element(self.END_DATE_INPUT)
        end_date_field.click()
        end_date_field.clear()
        end_date_field.send_keys(end_date)
        sleep(3)

        # 确认时间选择
        wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()

        # 保存考试
        self.click(self.SAVE_BUTTON)
        sleep(3)

        # 等待确认对话框并确认
        wait.until(EC.presence_of_element_located(self.MESSAGE_BOX))
        confirm_dialog_text = self.find_element(self.MESSAGE_TEXT).text
        logger.info(f"确认对话框消息: {confirm_dialog_text}")
        allure.attach(confirm_dialog_text, "确认对话框", allure.attachment_type.TEXT)

        # 保存确认对话框的截图
        self.save_screenshot("exam_creation_confirm_dialog")

        # 点击确认按钮
        wait.until(EC.element_to_be_clickable(self.CONFIRM_DIALOG_BUTTON)).click()
        sleep(3)  # 增加等待时间，确保成功消息有时间显示

        # 尝试捕获成功消息（可能是对话框或Toast通知）
        success_message = "未捕获到成功消息"

        # 首先尝试捕获对话框形式的成功消息
        try:
            if self.is_element_visible(self.MESSAGE_BOX, timeout=5):
                success_dialog_text = self.find_element(self.MESSAGE_TEXT).text
                logger.info(f"结果对话框消息: {success_dialog_text}")
                allure.attach(success_dialog_text, "结果对话框", allure.attachment_type.TEXT)

                # 保存成功对话框的截图
                self.save_screenshot("exam_creation_success_dialog")

                # 如果有确认按钮，点击它
                try:
                    self.click(self.CONFIRM_DIALOG_BUTTON)
                except:
                    logger.info("结果对话框无需点击确认按钮")

                success_message = success_dialog_text
        except:
            logger.info("未捕获到对话框形式的成功消息，尝试捕获Toast通知")

            # 尝试捕获Toast通知形式的成功消息
            try:
                if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
                    success_toast_text = self.find_element(self.SUCCESS_MESSAGE_TEXT).text
                    logger.info(f"成功通知消息: {success_toast_text}")
                    allure.attach(success_toast_text, "成功通知", allure.attachment_type.TEXT)

                    # 保存成功通知的截图
                    self.save_screenshot("exam_creation_success_toast")

                    success_message = success_toast_text
            except:
                logger.warning("未捕获到Toast通知形式的成功消息")

                # 捕获当前页面截图，可能有助于调试
                self.save_screenshot("exam_creation_after_confirm")

        # 如果没有捕获到任何成功消息，返回确认对话框消息作为结果
        if success_message == "未捕获到成功消息":
            logger.warning("未能捕获任何形式的成功消息，返回确认对话框消息")
            return confirm_dialog_text

        return success_message

    @allure.step("发布考试")
    def publish_exam(self):
        """发布考试"""
        logger.info("发布考试")

        try:
            # 等待页面稳定下来
            sleep(3)

            # 使用与手动脚本相同的方法查找状态下拉菜单
            wait = WebDriverWait(self.driver, 10)
            status_element = wait.until(EC.presence_of_element_located(self.STATUS_DROPDOWN))
            logger.info("找到状态下拉菜单元素")

            # 创建ActionChains对象用于悬停操作
            actions = ActionChains(self.driver)
            # 悬停在状态元素上
            actions.move_to_element(status_element).perform()
            logger.info("悬停在状态下拉菜单上")
            sleep(1)  # 给菜单足够的时间展开

            # 保存下拉菜单展开后的截图
            self.save_screenshot("exam_status_dropdown_menu")

            # 使用JavaScript点击"发布考试"选项
            result = self.driver.execute_script("""
            var elements = document.querySelectorAll("li.el-dropdown-menu__item");
            for(var i=0; i<elements.length; i++) {
                if(elements[i].textContent.includes("发布考试")) {
                    elements[i].click();
                    return true;
                }
            }
            return false;
            """)

            if result:
                logger.info("成功点击'发布考试'选项")
            else:
                logger.warning("未找到'发布考试'选项")
                self.save_screenshot("publish_button_not_found")
                raise Exception("无法找到'发布考试'选项")

            # 等待可能的确认对话框
            sleep(2)
            if self.is_element_visible(self.MESSAGE_BOX):
                confirm_text = self.find_element(self.MESSAGE_TEXT).text
                logger.info(f"发布确认对话框消息: {confirm_text}")
                wait.until(EC.element_to_be_clickable(self.CONFIRM_DIALOG_BUTTON)).click()
                logger.info("点击发布确认对话框的确认按钮")

            # 等待操作完成
            sleep(3)
            logger.info("考试已发布")

        except Exception as e:
            logger.error(f"发布考试失败: {e}")
            self.save_screenshot("publish_exam_error")
            raise

    @allure.step("切换到学员视图")
    def switch_to_student_view(self):
        """切换到学员视图"""
        logger.info("切换到学员视图")
        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable(self.CLOUD_EXAM_LINK))
            element.click()

            element = wait.until(EC.visibility_of_element_located(self.STUDENT_HOME_LINK))
            element.click()
            sleep(5)  # 等待学员页面加载
        except Exception as e:
            logger.error(f"切换到学员视图失败: {e}")
            self.save_screenshot("switch_to_student_view_error")
            raise

    @allure.step("验证考试在学员视图中可见")
    def verify_exam_in_student_view(self, exam_name):
        """验证考试在学员视图中可见"""
        logger.info(f"验证考试 '{exam_name}' 在学员视图中可见")

        try:
            # 获取所有考试链接
            exam_links = self.driver.find_elements(*self.EXAM_LINKS)

            # 检查是否找到考试
            exam_found = False
            exam_titles = []

            for link in exam_links:
                exam_titles.append(link.text)
                if link.text == exam_name:
                    exam_found = True
                    logger.info(f"在学员视图中找到考试: {link.text}")
                    break

            # 记录所有找到的考试标题
            allure.attach("\n".join(exam_titles), "学员视图中的考试列表", allure.attachment_type.TEXT)

            # 保存学员视图的截图
            self.save_screenshot("student_view_exams")

            return exam_found
        except Exception as e:
            logger.error(f"验证考试在学员视图中可见失败: {e}")
            self.save_screenshot("verify_exam_error")
            raise
    @allure.step("删除指定考试")
    def delete_exam(self, exam_name):
        """根据考试名称删除考试"""
        sleep(2)
        logger.info(f"尝试删除考试: {exam_name}")
        try:
            wait = WebDriverWait(self.driver, 10)

            # 进入考试管理页面（假设你前面已经点击管理员按钮）
            self.click((By.XPATH, '//span[contains(text(),"考试管理")]'))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"在线考试")]'))).click()
            sleep(2)

            # 找到对应考试名称的checkbox并点击
            checkbox = wait.until(EC.presence_of_element_located((
                By.XPATH,
                f'//a[contains(text(), "{exam_name}")]/ancestor::tr//span[contains(@class, "el-checkbox__inner")]'
            )))
            self.driver.execute_script("arguments[0].click();", checkbox)
            sleep(2)

            # 点击删除按钮并确认
            self.click((By.XPATH, '//span[contains(text(),"删除")]'))
            sleep(1)
            self.click((By.XPATH, '//span[contains(text(),"确定")]'))
            logger.info("点击删除并确认成功")
            sleep(2)
        except Exception as e:
            logger.error(f"删除考试失败: {e}")
            self.save_screenshot("delete_exam_error")
            raise

    @allure.step("修改指定考试")
    def update_exam(self, original_name, new_name=None, new_start_date=None, new_end_date=None):
        """修改指定考试信息"""
        logger.info(f"开始修改考试: {original_name}")
        allure.attach(f"原考试名称: {original_name}\n新名称: {new_name}\n新开始日期: {new_start_date}\n新结束日期: {new_end_date}",
                      "考试更新信息", allure.attachment_type.TEXT)

        try:
            wait = WebDriverWait(self.driver, 20)

            # 进入考试管理页面
            self.click((By.XPATH, '//span[contains(text(),"考试管理")]'))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"在线考试")]'))).click()
            sleep(2)

            # 更精确地定位考试所在行的 checkbox
            checkbox_xpath = f'//a[contains(text(), "{original_name}")]/ancestor::tr//span[contains(@class, "el-checkbox__inner")]'
            checkbox_span = wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))

            # 使用 JavaScript 点击，绕过可能的框架限制
            self.driver.execute_script("arguments[0].click();", checkbox_span)
            sleep(4)

            # 点击修改按钮
            self.click((By.XPATH, '//span[contains(text(),"修改")]'))
            sleep(2)

            # 更新考试名称（如果提供）
            if new_name:
                name_input = (By.CSS_SELECTOR, "div[data-v-5d48a21b] input.el-input__inner")
                self.click(name_input)
                self.find_element(name_input).clear()
                self.send_keys(name_input, new_name)
                sleep(2)
                logger.info(f"考试名称已更改为: {new_name}")

            # 更新开始和结束日期（如果提供）
            if new_start_date or new_end_date:
                # 点击时间输入框打开日期选择器
                self.click((By.XPATH, '//input[@placeholder="开始时间"]'))
                sleep(3)

                # 更新开始日期
                if new_start_date:
                    start_date_input = (By.XPATH, '//input[@placeholder="开始日期"]')
                    self.click(start_date_input)
                    self.find_element(start_date_input).clear()
                    self.send_keys(start_date_input, new_start_date)
                    sleep(2)
                    logger.info(f"开始日期已更改为: {new_start_date}")

                # 更新结束日期
                if new_end_date:
                    end_date_input = (By.XPATH, '//input[@placeholder="结束日期"]')
                    self.click(end_date_input)
                    self.find_element(end_date_input).clear()
                    self.send_keys(end_date_input, new_end_date)
                    sleep(2)
                    logger.info(f"结束日期已更改为: {new_end_date}")

                # 确认时间选择
                confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"确定")]')))
                confirm_btn.click()

            # 保存修改
            self.click(self.SAVE_BUTTON)
            sleep(3)

            # 等待确认对话框并确认
            wait.until(EC.presence_of_element_located(self.MESSAGE_BOX))
            confirm_dialog_text = self.find_element(self.MESSAGE_TEXT).text
            logger.info(f"确认对话框消息: {confirm_dialog_text}")
            allure.attach(confirm_dialog_text, "确认对话框", allure.attachment_type.TEXT)

            # 保存确认对话框的截图
            self.save_screenshot("exam_update_confirm_dialog")

            # 点击确认按钮
            confirm_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "el-message-box")]//span[contains(text(),"确")]'))
            )
            confirm_btn.click()
            sleep(3)

            # 尝试捕获成功消息
            success_message = "未捕获到成功消息"

            try:
                if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
                    success_toast_text = self.find_element(self.SUCCESS_MESSAGE_TEXT).text
                    logger.info(f"成功通知消息: {success_toast_text}")
                    allure.attach(success_toast_text, "成功通知", allure.attachment_type.TEXT)
                    self.save_screenshot("exam_update_success_toast")
                    success_message = success_toast_text
            except:
                logger.warning("未捕获到成功消息通知")
                self.save_screenshot("after_exam_update")

            return success_message if success_message != "未捕获到成功消息" else confirm_dialog_text

        except Exception as e:
            logger.error(f"修改考试失败: {e}")
            self.save_screenshot("update_exam_error")
            raise