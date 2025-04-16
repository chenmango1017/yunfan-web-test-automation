import os
import subprocess
import time
import pytest
@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束后自动生成并打开 Allure 报告"""
    if exitstatus == 0 or exitstatus == 1:  # 测试成功或部分失败
        print("\n正在生成 Allure 报告...")

        #命令中的--clean参数会清除之前生成的报告
        subprocess.run("allure generate D:/pycharm/code/exam_selenium/reports/allure-results -o D:/pycharm/code/exam_selenium/reports/allure-report --clean", shell=True)

        print("正在打开 Allure 报告...")


        allure_process = subprocess.Popen("allure open D:/pycharm/code/exam_selenium/reports/allure-report", shell=True)

        # 等待一段时间让报告在浏览器中打开
        time.sleep(5)

        # 终止allure进程
        try:
            if os.name == 'nt':  # Windows
                # 使用taskkill终止allure进程
                subprocess.run("taskkill /f /im allure.exe", shell=True)
            else:

                subprocess.run("pkill -f allure", shell=True)
        except Exception as e:
            print(f"无法终止Allure进程: {e}")

        print("Allure报告已生成，程序将在5秒后退出...")
        time.sleep(5)

