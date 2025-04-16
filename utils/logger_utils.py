import logging
import allure
import os
import datetime

class AllureLogger:
    """
    将日志输出到控制台和 Allure 报告的日志工具类
    """

    def __init__(self, name="TestLogger"):
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # 设置文件日志名称（使用当前时间）
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_{current_time}.log")

        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 清除已有的处理器，避免重复日志
        if self.logger.handlers:
            self.logger.handlers.clear()

        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器到 logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """输出 INFO 级别日志"""
        self.logger.info(message)
        with allure.step(f"INFO: {message}"):
            pass

    def debug(self, message):
        """输出 DEBUG 级别日志"""
        self.logger.debug(message)
        with allure.step(f"DEBUG: {message}"):
            pass

    def warning(self, message):
        """输出 WARNING 级别日志"""
        self.logger.warning(message)
        with allure.step(f"WARNING: {message}"):
            pass

    def error(self, message):
        """输出 ERROR 级别日志"""
        self.logger.error(message)
        with allure.step(f"ERROR: {message}"):
            allure.attach(message, "错误详情", allure.attachment_type.TEXT)

    def critical(self, message):
        """输出 CRITICAL 级别日志"""
        self.logger.critical(message)
        with allure.step(f"CRITICAL: {message}"):
            allure.attach(message, "严重错误详情", allure.attachment_type.TEXT)

# 创建全局日志实例，方便在各个模块中使用
logger = AllureLogger()