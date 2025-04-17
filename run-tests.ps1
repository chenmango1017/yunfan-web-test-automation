# Step 1: 清除旧的 allure-results（检查目录是否存在）
if (Test-Path "allure-results") {
    Remove-Item -Recurse -Force "allure-results"
}

# Step 2: 激活虚拟环境路径
$env:VIRTUAL_ENV = "D:\pycharm\code\exam_selenium\.venv"
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"

# Step 3: 执行 pytest 测试
pytest -n 4 -m "login_test or question_test or paper_test or exercise_test" --alluredir=allure-results
