import pytest

import allure
from datetime import datetime
from utils.logger_utils import logger

@pytest.mark.login_test
class TestLogin:
    @allure.feature("登录功能")
    @allure.story("使用有效账号登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, login_page, login_data):
        """登录测试"""

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 记录测试开始
        allure.dynamic.title(f"测试登录: {login_data[0]}")

        allure.dynamic.description(f"使用账号 {login_data[0]} 进行登录测试")

        # 在Allure报告中附加当前时间
        allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        logger.info(f"====== 开始登录测试: {login_data[0]} ======")

        try:
            username, password = login_data[0], login_data[1]

            # 使用测试数据进行登录
            login_page.login(username, password)

            # 验证登录结果
            assert login_page.is_login_success(), "云帆学习考试系统"

            # 登录成功后获取系统版本
            version = login_page.get_system_version()
            logger.info(f"系统版本: {version}")

            logger.info(f"====== 登录测试成功: {login_data[0]} ======")

        except Exception as e:
            logger.error(f"登录测试失败: {e}")
            # 在 Allure 报告中添加错误附件
            allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)
            # 截图
            login_page.save_screenshot(f"login_failure_{login_data[0]}")
            # 重新抛出异常，让测试失败
            raise
