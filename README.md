# Yunfan Web Test Automation

## 项目简介
本项目是针对**在线培训考试系统**的Web自动化测试框架，旨在通过自动化手段验证考试系统的各项功能和性能。该考试系统是一个多角色在线培训考试平台，具备完善的权限控制、用户管理、题库管理、考试管理等核心功能。

## 考试系统简介
该考试系统集成了以下功能：

- **用户管理、角色管理、部门管理**：支持不同角色用户的管理和权限控制
- **题库管理、试题管理**：支持多题型（单选题、多选题、判断题）的题库管理
- **考试管理和在线考试**：用户可以在线参加考试，并获得即时反馈
- **错题训练**：用户可以针对错题进行专项训练，以提高考试成绩

## 技术栈

### 被测系统技术栈
- **SpringBoot**：后端开发框架，提供高效的RESTful API和服务
- **Shiro**：权限控制和认证管理
- **Vue.js**：前端开发，提供响应式界面和用户交互功能
- **MySQL**：数据库，存储用户信息、考试数据和题库信息

### 测试框架技术栈
- **Python**：主要编程语言
- **Pytest**：测试框架
- **Selenium**：Web自动化工具
- **Allure**：测试报告生成工具
- **Pytest-xdist**：并行测试执行插件

## 项目架构

### 项目结构
```
yunfan-web-test-automation/
├── .idea/                # 项目配置文件，由IDE（如PyCharm）生成
├── base/                 # 基础页面和测试类
│   ├── base_page.py      # 页面基类，封装Selenium基本操作
│   └── base_test.py      # 测试基类，提供通用测试功能
├── data/                 # 测试数据
│   ├── login_data.yaml   # 登录测试数据
│   └── exam_data.yaml    # 考试相关测试数据
├── pages/                # 页面对象模型（POM）类
│   ├── login_page.py     # 登录页面
│   ├── admin_page.py     # 管理员页面
│   └── exam_page.py      # 考试页面
├── reports/              # 测试报告目录
├── test_case/            # 测试用例
│   ├── login/            # 登录相关测试
│   └── exam/             # 考试相关测试
├── utils/                # 工具函数
│   ├── logger_utils.py   # 日志工具
│   ├── yaml_utils.py     # 配置文件处理工具
│   └── captcha_utils.py  # 验证码处理工具
├── captcha.png           # 验证码识别测试图像
├── conftest.py           # pytest配置文件
├── pytest.ini            # pytest配置选项
├── requirements.txt      # 项目依赖
└── url_extract.yaml      # URL和其他配置信息
```

### 设计模式与架构
本项目采用**三层架构**设计：

1. **基础层 (base/)**：
   - 封装Selenium的基本操作（点击、输入、等待等）
   - 提供基础测试类，包含通用的测试前置和后置操作

2. **页面层 (pages/)**：
   - 基于页面对象模型（POM）设计
   - 每个页面单独封装为一个类，包含页面元素定位和业务操作
   - 提高代码复用性和可维护性

3. **测试层 (test_case/)**：
   - 实现具体的测试用例
   - 使用数据驱动方式组织测试场景
   - 通过调用页面层的方法执行测试步骤

### 数据驱动
使用YAML配置文件存储测试数据，实现测试数据与测试代码的分离，便于维护和扩展。例如：

```yaml
# login_data.yaml 示例
admin:
  username: admin
  password: admin
  role: administrator

student:
  username: student01
  password: student123
  role: student
```

### 工具类
- **Logger Utility**：记录测试日志，帮助调试和分析
- **YAML Utility**：解析配置文件，确保测试数据的灵活性
- **Captcha Utility**：处理登录验证码，提高测试自动化程度

## 环境准备与安装

### 先决条件
- Python 3.7+
- Chrome浏览器（推荐最新版本）
- ChromeDriver（与Chrome浏览器版本匹配）

### 安装步骤
1. 克隆仓库
```bash
git clone https://github.com/chenmango1017/yunfan-web-test-automation.git
cd yunfan-web-test-automation
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境
   - 确保ChromeDriver在系统路径中或通过webdriver-manager自动管理
   - 更新`url_extract.yaml`中的URL配置，指向您的测试环境

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试模块
```bash
pytest test_case/login/test_login.py
```

### 使用标签运行测试
```bash
pytest -m login_test
```

### 并行执行测试
```bash
pytest -n 4  # 使用4个核心并行执行
```

### 生成Allure报告
```bash
pytest --alluredir=./reports
allure serve ./reports
```

## 测试特性

### 并行测试
本项目利用pytest-xdist插件实现测试用例的并行执行，显著提升测试效率：

```bash
# 使用8个核心并行执行所有测试
pytest -n 8

# 并行执行特定模块的测试
pytest -n 4 test_case/login/
```

### 测试用例标记与分组
使用pytest的mark装饰器对测试用例进行分类：

```python
# 测试用例示例
@pytest.mark.login_test
def test_admin_login(setup_browser):
    """测试管理员登录功能"""
    login_page = LoginPage(setup_browser)
    assert login_page.login_as_admin().is_login_successful()

@pytest.mark.exam_test
def test_start_exam(login_fixture):
    """测试开始考试功能"""
    exam_page = ExamPage(login_fixture)
    assert exam_page.start_exam().is_exam_started()
```

### 测试数据参数化
使用pytest的参数化功能，结合YAML数据文件：

```python
@pytest.mark.parametrize(
    "username,password,expected", 
    get_test_data("data/login_data.yaml", "invalid_logins")
)
def test_invalid_login(setup_browser, username, password, expected):
    """测试无效登录场景"""
    login_page = LoginPage(setup_browser)
    result = login_page.login(username, password)
    assert expected in result.get_error_message()
```

### 失败重试机制
使用pytest-rerunfailures插件实现测试失败自动重试：

```bash
# 失败重试最多3次，每次等待2秒
pytest --reruns 3 --reruns-delay 2
```

## 测试报告

本项目使用Allure生成详细的测试报告，包括：

- 测试执行概览：通过率、失败率、跳过率等统计数据
- 测试用例详情：每个测试的执行状态和详细信息
- 测试步骤与截图：失败时自动捕获的屏幕截图
- 执行时间分析：各测试用例和测试套件的执行时长
- 环境信息：测试运行环境的详细配置

运行以下命令生成并查看报告：
```bash
pytest --alluredir=./reports
allure serve ./reports
```

## 最佳实践

### 验证码处理策略
本项目提供了多种验证码处理方案：

1. **自动识别**：使用OCR技术自动识别验证码
   ```python
   # 验证码识别示例
   from utils.captcha_utils import recognize_captcha
   
   captcha_text = recognize_captcha(captcha_element.screenshot_as_base64)
   ```

2. **测试环境配置**：在测试环境中配置固定验证码或绕过验证码验证

### 页面等待策略
采用显式等待和隐式等待相结合的方式，提高测试稳定性：

```python
# base_page.py 中的等待方法示例
def wait_for_element_visible(self, locator, timeout=10):
    """等待元素可见"""
    return WebDriverWait(self.driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
```

### 异常处理与截图
测试失败时自动捕获屏幕截图，便于问题排查：

```python
# conftest.py 中的失败处理钩子
@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    if report.failed:
        if "setup_browser" in node.funcargs:
            driver = node.funcargs["setup_browser"]
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
```

## 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 常见问题

### Q: 如何处理动态元素和AJAX加载的内容？
A: 使用显式等待和自定义等待条件，确保元素在操作前已完全加载。

### Q: 测试在CI环境中运行失败但在本地运行正常？
A: 检查浏览器版本和驱动匹配问题，考虑使用headless模式运行测试。

### Q: 如何添加新的测试用例？
A: 
1. 在pages/目录下添加新的页面类（如果需要）
2. 在data/目录下添加测试数据
3. 在test_case/目录下创建新的测试文件
4. 运行测试并验证结果

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：
- Email: chenmango@gmail.com
- GitHub Issues: [提交Issue](https://github.com/chenmango1017/yunfan-web-test-automation/issues)
