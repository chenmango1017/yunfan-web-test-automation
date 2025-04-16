from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.page_base import BasePage
from utils.gain_verify import gain_verify
from utils.logger_utils import logger
from utils.yaml_utils import yaml_utils
import allure
from time import sleep

class LoginPage(BasePage):
    # 登录页面定位器
    USERNAME_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input.el-input__inner[type='password']")
    CAPTCHA_IMAGE = (By.XPATH, "//img[contains(@src, '/api/common/captcha/gen')]")
    CAPTCHA_INPUT = (By.XPATH, "//input[@placeholder='输入验证码']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".el-button.el-button--primary")

    # 登录成功页面定位器
    SYSTEM_TITLE = (By.XPATH, "//div[contains(text(), '云帆学习考试系统')]")
    LOGO_CONTAINER = (By.CLASS_NAME, "sidebar-logo-container")
    SIDEBAR_MENU = (By.XPATH, "//div[contains(@class, 'sidebar-container')]")
    DASHBOARD_ELEMENT = (By.XPATH, "//div[text()='管理首页']")
    STATS_OVERVIEW = (By.XPATH, "//div[text()='统计总览']")

    # 错误消息定位器
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'el-message--error')]")

    def __init__(self):
        super().__init__()
        self.url = yaml_utils.read_url()

        logger.info("初始化登录页面")

    @allure.step("登录系统")
    def login(self, username, password):
        """登录方法"""
        # 打开页面
        self.open_url(self.url)
        allure.attach(f"用户名: {username}", "登录信息", allure.attachment_type.TEXT)
        # 密码不记录在报告中

        # 等待验证码图片加载
        logger.info("等待验证码图片加载")
        captcha_element = self.wait_element_visible(self.CAPTCHA_IMAGE)

        # 确保验证码图片完全加载
        while captcha_element.size['width'] == 0 or captcha_element.size['height'] == 0:
            logger.debug("验证码图片未完全加载，等待...")
            captcha_element = self.driver.find_element(*self.CAPTCHA_IMAGE)
            sleep(0.5)

        # 验证码识别
        self.screenshot(captcha_element, "captcha.png")
        captcha_code = gain_verify("captcha.png")
        logger.info(f"识别的验证码: {captcha_code}")
        allure.attach(captcha_code, "识别的验证码", allure.attachment_type.TEXT)

        # 输入登录信息
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.CAPTCHA_INPUT, captcha_code)

        # 点击登录
        self.click(self.LOGIN_BUTTON)
        logger.info("点击登录按钮")

        # 等待登录响应
        sleep(1)

    @allure.step("验证登录结果")
    def is_login_success(self):
        """检查是否登录成功的方法"""
        try:
            # 先检查是否有错误消息
            try:
                error_element = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(self.ERROR_MESSAGE)
                )
                error_message = error_element.text
                logger.error(f"登录失败，错误信息: {error_message}")
                allure.attach(error_message, "登录错误", allure.attachment_type.TEXT)
                # 保存错误截图
                self.save_screenshot("login_error")
                return False
            except:
                # 没有错误消息，继续检查成功标志
                logger.debug("无错误消息，检查登录成功标志")
                pass

            # 设置较短的等待时间
            wait = WebDriverWait(self.driver, 5)

            # 尝试找到登录成功的标志元素
            success_elements = {
                "系统标题": self.SYSTEM_TITLE,
                "Logo容器": self.LOGO_CONTAINER,
                "侧边栏菜单": self.SIDEBAR_MENU,
                "管理首页": self.DASHBOARD_ELEMENT,
                "统计总览": self.STATS_OVERVIEW
            }

            for name, element in success_elements.items():
                try:
                    wait.until(EC.visibility_of_element_located(element))
                    logger.info(f"找到登录成功标志: {name}")
                    # 登录成功，保存截图
                    self.save_screenshot("login_success")
                    return True
                except:
                    logger.debug(f"未找到登录成功标志: {name}")
                    continue

            # 如果上述所有元素都没找到，则登录可能失败
            logger.warning("未找到登录成功后的任何标志元素")
            self.save_screenshot("login_unknown_state")
            return False

        except Exception as e:
            logger.critical(f"登录验证过程发生异常: {e}")
            # 保存截图以供分析
            self.save_screenshot("login_verification_error")
            return False

    @allure.step("获取系统版本")
    def get_system_version(self):
        try:
            VERSION_ELEMENT = (By.XPATH, "//div[contains(text(), '系统版本')]")
            version_text = self.find_element(VERSION_ELEMENT).text
            version = version_text.split("：")[1].strip()
            logger.info(f"获取系统版本: {version}")
            allure.attach(version, "系统版本", allure.attachment_type.TEXT)
            return version
        except Exception as e:
            logger.error(f"获取系统版本失败: {e}")
            return "无法获取版本信息"