from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base.page_base import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from utils.logger_utils import logger
from utils.yaml_utils import yaml_utils
import allure
from time import sleep

from selenium.webdriver.support import expected_conditions as EC
class QuestionPage(BasePage):
    # 导航菜单定位器
    ADMIN_MENU = (By.XPATH, '//span[contains(text(),"管理员")]')
    QUESTION_BANK_MENU = (By.XPATH, '//span[contains(text(),"题库管理")]')
    QUESTION_BANK_SUBMENU = (By.XPATH, "//div[@class='menu-wrapper nest-menu']/a/li/span[text()='题库管理']")
    QUESTION_MANAGE_MENU = (By.XPATH, '//span[contains(text(),"试题管理")]')
    AI_QUESTION_MENU = (By.XPATH, '//span[contains(text(),"智能出题")]')

    # 题库管理页面定位器
    ADD_BUTTON = (By.XPATH, '//span[contains(text(),"添加")]')
    BANK_NAME_INPUT = (By.XPATH, '//label[contains(text(),"题库名称")]/following-sibling::div//input')
    CATEGORY_INPUT = (By.XPATH, '//input[@placeholder="请选择分类"]')
    CATEGORY_OPTION = (By.XPATH, '//span[contains(text(),"{0}")]') # 动态xpath，根据传入的分类名称定位
    KNOWLEDGE_POINT_INPUT = (By.XPATH, '//input[@placeholder="选择知识点"]')
    KNOWLEDGE_POINT_OPTION = (By.XPATH, '//span[contains(text(),"{0}")]') # 动态xpath，根据传入的知识点定位
    ADD_KNOWLEDGE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--primary') and .//i[contains(@class, 'el-icon-plus')]]")
    BANK_INTRO_TEXTAREA = (By.XPATH, "//label[contains(text(),'题库简介')]/following::textarea")
    SAVE_BUTTON = (By.XPATH, '//span[contains(text(),"保存")]')

    # 智能出题页面定位器
    REQUIREMENT_TEXTAREA = (By.XPATH, '//textarea[@placeholder="输入您的出题需求"]')
    SINGLE_CHOICE_COUNT = (By.XPATH, "//div[contains(@class, 'gen-item')][.//div[text()='单选题']]//input[@type='text']")
    GENERATE_BUTTON = (By.XPATH, '//span[contains(text(),"开始生成")]')
    IMPORT_BUTTON = (By.XPATH, '//span[contains(text(),"入库")]')

    # 入库选择定位器
    SELECT_BANK_INPUT = (By.XPATH, '//input[@placeholder="选择或搜索题库"]')
    SELECT_CHAPTER_INPUT = (By.XPATH, '//input[@placeholder="选择章节"]')
    SELECT_DIFFICULTY_INPUT = (By.XPATH, '//input[@placeholder="请选择"]')
    CONFIRM_BUTTON = (By.XPATH, '//span[contains(text(),"确认")]')
    ENTER_BANK_BUTTON = (By.XPATH, '//span[contains(text(),"进入题库")]')

    # 学员页面定位器
    CLOUD_EXAM_BUTTON = (By.XPATH, '//div[contains(text(),"云帆考试")]')
    STUDENT_HOME_BUTTON = (By.XPATH, '//li[contains(text(),"学员首页")]')
    PRACTICE_BUTTON = (By.XPATH, '//li[contains(text(),"刷题")]')
    QUESTION_BANK_LINK = (By.CSS_SELECTOR, "a.d-link")

    def __init__(self):
        super().__init__()
        self.url = yaml_utils.read_url()
        logger.info("初始化试题管理页面")

    @allure.step("登录并导航到题库管理页面")
    def navigate_to_question_bank(self):
        """登录并导航到题库管理页面"""
        logger.info("导航到题库管理页面")

        # 点击管理员菜单
        self.click(self.ADMIN_MENU)
        sleep(2)

        # 点击题库管理菜单
        # 将 wait_element_clickable 替换为 wait_element_visible
        wait_element = self.wait_element_visible(self.QUESTION_BANK_MENU)
        wait_element.click()
        sleep(2)

        # 点击题库管理子菜单
        # 将 wait_element_clickable 替换为 wait_element_visible
        wait_element = self.wait_element_visible(self.QUESTION_BANK_SUBMENU)
        wait_element.click()
        sleep(3)

        logger.info("成功导航到题库管理页面")
        self.save_screenshot("question_bank_page")
        return self

    @allure.step("创建新题库: {bank_name}")
    def create_question_bank(self, bank_name, category="职业资格", knowledge_point="数据库", description="题库简介"):
        """创建新题库"""
        logger.info(f"创建新题库: {bank_name}")
        allure.attach(f"题库名: {bank_name}\n分类: {category}\n知识点: {knowledge_point}\n简介: {description}",
                      "题库信息", allure.attachment_type.TEXT)

        # 点击添加按钮
        self.click(self.ADD_BUTTON)
        sleep(2)

        # 输入题库名称
        bank_name_input = self.find_element(self.BANK_NAME_INPUT)
        bank_name_input.click()
        bank_name_input.send_keys(bank_name)
        sleep(2)

        # 选择分类
        self.find_element(self.CATEGORY_INPUT).click()
        sleep(2)

        # 动态定位分类选项
        category_option = (By.XPATH, self.CATEGORY_OPTION[1].format(category))
        self.click(category_option)
        sleep(2)

        # 选择知识点
        self.find_element(self.KNOWLEDGE_POINT_INPUT).click()
        sleep(2)

        # 动态定位知识点选项
        knowledge_option = (By.XPATH, self.KNOWLEDGE_POINT_OPTION[1].format(knowledge_point))
        # 将 wait_element_clickable 替换为 wait_element_visible
        wait_element = self.wait_element_visible(knowledge_option)
        wait_element.click()
        sleep(3)

        # 点击添加知识点按钮
        # 将 wait_element_clickable 替换为 wait_element_visible
        add_button = self.wait_element_visible(self.ADD_KNOWLEDGE_BUTTON)
        add_button.click()
        sleep(2)

        # 输入题库简介
        textarea = self.find_element(self.BANK_INTRO_TEXTAREA)
        textarea.click()
        textarea.send_keys(description)
        sleep(2)

        # 保存题库
        self.click(self.SAVE_BUTTON)
        sleep(3)

        logger.info(f"题库 '{bank_name}' 创建成功")
        self.save_screenshot(f"bank_created_{bank_name}")
        return True

    @allure.step("导航至智能出题页面")
    def navigate_to_ai_question(self):
        """导航至智能出题页面"""
        logger.info("导航至智能出题页面")

        # 点击试题管理菜单
        # 将 wait_element_clickable 替换为 wait_element_visible
        wait_element = self.wait_element_visible(self.QUESTION_MANAGE_MENU)
        wait_element.click()
        sleep(2)

        # 点击智能出题菜单
        # 将 wait_element_clickable 替换为 wait_element_visible
        wait_element = self.wait_element_visible(self.AI_QUESTION_MENU)
        wait_element.click()
        sleep(2)

        logger.info("成功导航至智能出题页面")
        self.save_screenshot("ai_question_page")
        return self

    @allure.step("使用AI生成题目: {generate_demand}")
    def generate_questions(self, generate_demand, question_count=5):
        """使用AI生成题目"""
        logger.info(f"使用AI生成题目, 需求: {generate_demand}, 单选题数量: {question_count}")
        allure.attach(f"出题需求: {generate_demand}\n单选题数量: {question_count}",
                      "AI出题信息", allure.attachment_type.TEXT)

        # 输入出题需求
        # 将 wait_element_clickable 替换为 wait_element_visible
        textarea = self.wait_element_visible(self.REQUIREMENT_TEXTAREA)
        textarea.click()
        textarea.clear()
        textarea.send_keys(generate_demand)
        sleep(2)

        # 设置单选题数量
        # 将 wait_element_clickable 替换为 wait_element_visible
        single_choice_input = self.wait_element_visible(self.SINGLE_CHOICE_COUNT)
        single_choice_input.click()
        single_choice_input.clear()
        single_choice_input.send_keys(str(question_count))
        sleep(2)

        # 点击开始生成按钮
        self.click(self.GENERATE_BUTTON)

        # 等待生成完成
        logger.info("等待AI生成题目...")
        sleep(20) # 可能需要更长时间，实际场景可能需要等待某个元素出现

        logger.info("AI题目生成完成")
        self.save_screenshot("questions_generated")
        return self

    @allure.step("将生成的题目导入题库: {bank_name}")
    def import_to_question_bank(self, bank_name, chapter="新章节", difficulty="简单"):
        """将生成的题目导入题库"""
        logger.info(f"将生成的题目导入题库: {bank_name}, 章节: {chapter}, 难度: {difficulty}")

        # 点击入库按钮
        self.click(self.IMPORT_BUTTON)
        sleep(2)

        # 选择题库
        select_bank = self.find_element(self.SELECT_BANK_INPUT)
        select_bank.click()
        sleep(1)
        select_bank.clear()
        select_bank.send_keys(bank_name)
        sleep(1)
        select_bank.send_keys(Keys.DOWN)
        sleep(0.5)
        select_bank.send_keys(Keys.ENTER)
        sleep(2)

        # 选择章节
        select_chapter = self.find_element(self.SELECT_CHAPTER_INPUT)
        select_chapter.click()
        sleep(1)
        select_chapter.clear()
        select_chapter.send_keys(chapter)
        sleep(1)
        select_chapter.send_keys(Keys.DOWN)
        sleep(0.5)
        select_chapter.send_keys(Keys.ENTER)
        sleep(2)

        # 选择难度
        select_difficulty = self.find_element(self.SELECT_DIFFICULTY_INPUT)
        select_difficulty.click()
        sleep(1)
        select_difficulty.clear()
        select_difficulty.send_keys(difficulty)
        sleep(1)
        select_difficulty.send_keys(Keys.DOWN)
        sleep(0.5)
        select_difficulty.send_keys(Keys.ENTER)
        sleep(7)  # 增加等待时间以确保选择完成

        # 确认导入
        self.click(self.CONFIRM_BUTTON)
        sleep(2)

        # 点击进入题库按钮
        self.click(self.ENTER_BANK_BUTTON)
        sleep(4)  # 增加等待时间

        logger.info(f"成功将题目导入题库: {bank_name}")
        self.save_screenshot(f"imported_to_{bank_name}")
        return self

    @allure.step("导航至学员刷题页面")
    def navigate_to_student_practice(self):
        """导航至学员刷题页面"""
        logger.info("导航至学员刷题页面")

        # 点击云帆考试按钮
        self.click(self.CLOUD_EXAM_BUTTON)
        sleep(2)

        # 点击学员首页按钮
        self.click(self.STUDENT_HOME_BUTTON)
        sleep(2)

        # 点击刷题按钮
        self.click(self.PRACTICE_BUTTON)
        sleep(2)

        logger.info("成功导航至学员刷题页面")
        self.save_screenshot("student_practice_page")
        return self

    @allure.step("验证题库是否存在: {bank_name}")
    def verify_question_bank_exists(self, bank_name):
        """验证题库是否存在"""
        logger.info(f"验证题库是否存在: {bank_name}")

        # 获取所有题库链接
        bank_links = self.find_elements(self.QUESTION_BANK_LINK)

        # 检查是否存在指定名称的题库
        found = False
        for link in bank_links:
            text = link.text.strip()
            if text == bank_name:
                found = True
                logger.info(f"找到题库: {bank_name}")
                self.save_screenshot(f"found_bank_{bank_name}")
                break

        if not found:
            logger.warning(f"未找到题库: {bank_name}")
            self.save_screenshot(f"bank_not_found_{bank_name}")

        return found

    def find_elements(self, locator, timeout=10):
        """查找多个元素

        Args:
            locator: 元素定位器，格式为 (定位方式, 定位值)
            timeout: 等待超时时间，默认10秒

        Returns:
            找到的元素列表，如果没找到则返回空列表
        """
        logger.info(f"查找多个元素: {locator}")
        try:
            # 使用显式等待找元素
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            # 找到至少一个元素后，获取所有匹配的元素
            elements = self.driver.find_elements(*locator)
            logger.info(f"找到 {len(elements)} 个元素")
            return elements
        except TimeoutException:
            logger.warning(f"等待元素超时: {locator}")
            # 返回空列表而不是None
            return []
        except Exception as e:
            logger.error(f"查找元素时出错: {e}")
            # 返回空列表而不是None
            return []