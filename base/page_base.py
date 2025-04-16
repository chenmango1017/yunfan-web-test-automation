from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger_utils import logger
import allure
import datetime
from PIL import Image
import io
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
class BasePage:
    def __init__(self):
        # 初始化 WebDriver
        logger.info("初始化 WebDriver")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def open_url(self, url):
        """打开指定URL"""
        logger.info(f"打开网址: {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    def find_element(self, locator):
        """查找元素"""
        logger.debug(f"查找元素: {locator}")
        return self.driver.find_element(*locator)

    def wait_element_visible(self, locator):
        """等待元素可见"""
        logger.debug(f"等待元素可见: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def send_keys(self, locator, text):
        """发送文本到指定元素"""
        masked_text = text if 'password' not in str(locator).lower() else '*****'
        logger.info(f"输入文本到元素 {locator}: {masked_text}")
        element = self.wait_element_visible(locator)
        element.clear()
        element.send_keys(text)


    def click(self, locator):
        """点击元素，如果常规点击失败则尝试使用 JS 点击"""
        logger.info(f"点击元素: {locator}")
        try:
            element = self.wait_element_visible(locator)
            element.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            logger.warning(f"常规点击失败，尝试使用 JavaScript 点击: {locator}")
            try:
                element = self.find_element(locator)
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as js_e:
                logger.error(f"JavaScript 点击也失败: {js_e}")
                self.save_screenshot(f"click_failed_{locator}")
            raise js_e


    def screenshot(self, element, filename):
        """对元素截图"""
        logger.info(f"截图元素到文件: {filename}")
        element.screenshot(filename)
        # 将截图添加到 Allure 报告
        with open(filename, "rb") as file:
            allure.attach(
                file.read(),
                name=f"截图_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                attachment_type=allure.attachment_type.PNG
            )

    def save_screenshot(self, name="screenshot"):
        """保存整个页面截图并添加到 Allure 报告，而不保存到本地"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # 截图到内存中
        screenshot = self.driver.get_screenshot_as_png()

        # 将截图内容作为附件添加到 Allure 报告
        with io.BytesIO(screenshot) as byte_io:
            image = Image.open(byte_io)  # 如果你想对图像做一些处理，可以使用PIL
            allure.attach(
                byte_io.getvalue(),
                name=f"{name}_{timestamp}",
                attachment_type=allure.attachment_type.PNG
            )

        return screenshot
    def quit(self):
        """关闭浏览器"""
        logger.info("关闭浏览器")
        self.driver.quit()