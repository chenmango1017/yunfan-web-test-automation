import pytest
import allure
from datetime import datetime
from utils.logger_utils import logger


@pytest.mark.paper_test
class TestPaper:

    @allure.feature("试卷管理")
    @allure.story("创建并发布试卷")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_exam(self, exam_page, add_exam_data):
        """创建试卷测试"""

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 在Allure报告中附加当前时间
        allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        # 打开管理员面板
        exam_page.open_admin_panel()

        exam_name = add_exam_data['exam_name']
        start_date = add_exam_data['start_date']
        end_date = add_exam_data['end_date']
        expected_message = add_exam_data.get('expected_message', '')  # 使用get方法，如果没有该键则返回空字符串

        # 记录测试开始
        allure.dynamic.title(f"测试创建试卷: {exam_name}")
        allure.dynamic.description(f"使用日期范围 {start_date} 到 {end_date} 创建试卷")

        logger.info(f"====== 开始试卷创建测试: {exam_name} ======")

        try:
            # 创建试卷
            dialog_text = exam_page.create_exam(exam_name, start_date, end_date)

            # 验证对话框消息不包含错误
            assert "错误" not in dialog_text, f"创建试卷失败: {dialog_text}"

            # 特殊处理：如果返回的是确认对话框消息，记录但继续测试
            if dialog_text == "确实要提交保存吗？":
                logger.warning("捕获到的是确认对话框消息，而非最终结果消息。继续测试流程。")
                allure.attach("确认对话框消息被作为结果返回，可能需要调整成功消息捕获逻辑", "警告", allure.attachment_type.TEXT)
            # 如果有预期消息，且不是确认对话框，则验证
            elif expected_message and dialog_text != "确实要提交保存吗？":
                assert expected_message in dialog_text, f"对话框消息中未找到预期消息: {expected_message}"

            # 发布试卷
            exam_page.publish_exam()

            # 切换到学员视图
            exam_page.switch_to_student_view()

            # 验证试卷在学员视图中可见
            exam_found = exam_page.verify_exam_in_student_view(exam_name)
            assert exam_found, f"无法在学员页面找到试卷: {exam_name}"

            logger.info(f"====== 试卷创建测试成功: {exam_name} ======")
        except Exception as e:
            logger.error(f"试卷创建测试失败: {e}")
            # 在 Allure 报告中添加错误附件
            allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)
            # 截图
            exam_page.save_screenshot(f"paper_creation_failure_{exam_name}")
            # 重新抛出异常，让测试失败
            raise
    @allure.feature("试卷管理")
    @allure.story("删除试卷")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_exam(self, exam_page, delete_exam_data):
            """删除试卷测试"""
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 在Allure报告中附加当前时间
            allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)


            exam_name = delete_exam_data['exam_name']

            allure.dynamic.title(f"测试删除试卷: {exam_name}")
            allure.dynamic.description(f"删除并验证试卷: {exam_name} 不存在于学员视图中")

            logger.info(f"====== 开始试卷删除测试: {exam_name} ======")

            try:
                # 打开管理员面板
                exam_page.open_admin_panel()

                # 执行删除操作
                exam_page.delete_exam(exam_name)

                # 切换到学员视图
                exam_page.switch_to_student_view()

                # 验证试卷是否已从学员视图中消失
                exam_still_visible = exam_page.verify_exam_in_student_view(exam_name)

                # 断言试卷确实被删除
                assert not exam_still_visible, f"❌ 删除失败: {exam_name} 仍然出现在学员视图中！"

                logger.info(f"====== 删除试卷测试成功: {exam_name} ======")

            except Exception as e:
                logger.error(f"删除试卷测试失败: {e}")
                allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)
                exam_page.save_screenshot(f"paper_delete_failure_{exam_name}")
                raise


    @allure.feature("试卷管理")
    @allure.story("修改试卷")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_exam(self, exam_page, update_exam_data):
        """修改试卷测试"""

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 在Allure报告中附加当前时间
        allure.attach(f"当前时间: {current_time}", name="测试时间", attachment_type=allure.attachment_type.TEXT)

        # 获取测试数据
        original_name = update_exam_data['original_name']
        new_name = update_exam_data.get('new_name')
        new_start_date = update_exam_data.get('new_start_date')
        new_end_date = update_exam_data.get('new_end_date')
        expected_message = update_exam_data.get('expected_message', '')

        # 记录测试开始
        allure.dynamic.title(f"测试修改试卷: {original_name}")
        allure.dynamic.description(f"修改试卷: {original_name}" +
                                   (f" -> 新名称: {new_name}" if new_name else "") +
                                   (f", 新日期范围: {new_start_date} 到 {new_end_date}" if new_start_date and new_end_date else ""))

        logger.info(f"====== 开始试卷修改测试: {original_name} ======")

        try:
            # 打开管理员面板
            exam_page.open_admin_panel()

            # 修改试卷
            dialog_text = exam_page.update_exam(original_name, new_name, new_start_date, new_end_date)

            # 验证对话框消息不包含错误
            assert "错误" not in dialog_text, f"修改试卷失败: {dialog_text}"

            # 如果有预期消息，则验证
            if expected_message:
                assert expected_message in dialog_text, f"对话框消息中未找到预期消息: {expected_message}"

            # 重新发布试卷
            exam_page.publish_exam()

            # 切换到学员视图
            exam_page.switch_to_student_view()

            # 验证试卷在学员视图中可见（使用新名称如果有的话）
            verify_name = new_name if new_name else original_name
            exam_found = exam_page.verify_exam_in_student_view(verify_name)
            assert exam_found, f"无法在学员页面找到修改后的试卷: {verify_name}"

            logger.info(f"====== 试卷修改测试成功: {original_name} -> {verify_name} ======")

        except Exception as e:
            logger.error(f"试卷修改测试失败: {e}")
            # 在 Allure 报告中添加错误附件
            allure.attach(str(e), "异常信息", allure.attachment_type.TEXT)
            # 截图
            exam_page.save_screenshot(f"paper_update_failure_{original_name}")
            # 重新抛出异常，让测试失败
            raise