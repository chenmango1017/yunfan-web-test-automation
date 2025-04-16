# Yunfan Web Test Automation

## 项目简介
本项目是针对**在线培训考试系统**进行的Web自动化测试框架，目的是帮助开发人员通过自动化手段验证考试系统的各项功能和性能。考试系统是一个多角色在线培训考试平台，具备完善的权限控制、用户管理、题库管理、考试管理等核心功能。

## 考试系统简介
该考试系统集成了以下功能：

- **用户管理、角色管理、部门管理**：支持不同角色用户的管理和权限控制。
- **题库管理、试题管理**：支持多题型（单选题、多选题、判断题）的题库管理。
- **考试管理和在线考试**：用户可以在线参加考试，并进行错题训练。
- **错题训练**：用户可以针对错题进行专项训练，以提高考试成绩。

## 技术栈

### 被测系统技术栈
- **SpringBoot**：作为后端开发框架，提供高效的RESTful API和服务。
- **Shiro**：用于权限控制和认证管理。
- **Vue.js**：用于前端开发，提供响应式界面和用户交互功能。
- **MySQL**：作为数据库，用于存储用户信息、考试数据和题库信息。

### 测试框架技术栈
- **Python**：主要编程语言
- **Pytest**：测试框架
- **Selenium**：Web自动化工具
- **Allure**：测试报告生成工具
- **Pytest-xdist**：并行测试执行插件

## 核心功能
- **权限控制**：基于Shiro和JWT开发的权限控制功能。
- **用户系统**：包括用户管理、部门管理和角色管理功能。
- **多角色支持**：支持学生、教师、管理员等多种角色，功能权限不同。
- **考试端功能**：学生可以进行在线考试、查看分数并进行错题训练。
- **管理端功能**：管理员可以进行题库管理、试题管理、考试管理以及查看考试结果等。

## 项目背景
本自动化测试框架主要用于测试该在线培训考试系统，确保系统的各项功能能够按预期工作。使用python+pytest+selenium测试功能涵盖了登录、考试流程、题库管理、权限控制等多个方面，并通过Allure报告生成详细的测试结果，方便分析和改进。

## 功能和结构

### 项目结构
```
├── .idea/                # 项目配置文件，由IDE（如PyCharm）生成
├── base/                 # 基础页面和测试类
├── data/                 # 测试数据
├── pages/                # 页面对象模型（POM）类
├── reports/              # 测试报告目录
├── test_case/            # 测试用例
├── utils/                # 工具函数
│   ├── logger_utils.py   # 日志工具
│   └── yaml_utils.py     # 配置文件处理工具
├── captcha.png           # 验证码识别测试图像
├── conftest.py           # pytest配置文件
├── pytest.ini            # pytest配置选项
└── url_extract.yaml      # URL和其他配置信息
```

### 页面对象模型（POM）
项目使用**页面对象模型（POM）**来组织页面操作，每个页面都封装为一个类。每个类包含页面上的元素定位和操作，确保代码的高复用性和可维护性。
基础层(base/) - 封装了Selenium的基本操作，提供了元素定位、点击、输入等基础功能
页面层(pages/) - 基于POM模式，为每个页面创建独立的类，包含页面元素和业务操作
测试层(test_case/) - 实现具体的测试用例，调用页面层的方法执行测试步骤
###数据驱动
使用YAML配置文件存储测试数据，实现了测试数据与测试代码的分离，便于维护和扩展。

### 工具
- **Logger Utility**：记录测试日志，帮助调试和分析。
- **YAML Utility**：用于解析配置文件，确保测试数据的灵活性和可扩展性。

## 环境准备与安装

### 先决条件
- Python 3.7+
- Chrome浏览器（推荐最新版本）
- ChromeDriver（与Chrome浏览器版本匹配）

### 安装步骤
1. 克隆仓库
```bash
git clone https://github.com/chenmango/yunfan-web-test-automation.git
cd yunfan-web-test-automation
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境
   - 确保ChromeDriver在系统路径中
   - 更新`url_extract.yaml`中的URL配置，指向您的测试环境

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试模块
```bash
pytest -v -m login_test test_case/login/test_login.py

```

### 使用标签运行测试
```bash
pytest -v -m login_test

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

## 并行测试与插件

### 使用pytest-xdist插件进行并行测试
本项目使用了pytest-xdist插件来实现并行执行测试用例，提升测试效率。通过设置`-n`参数，测试可以并行运行在多个CPU核心上，从而缩短测试时间。

例如，运行以下命令可以使用4个核心并行执行登录相关的测试用例：
```bash
pytest -n 4 test_case/test_login.py
```

### 测试用例标记
使用pytest的mark装饰器对测试用例进行分类，便于组织和执行特定类别的测试：

```python
@pytest.mark.login_test
def test_admin_login():
    # 测试管理员登录功能
    pass
```

然后可以使用以下命令运行所有标记为login的测试：
```bash
pytest -m login_test
```

## 测试报告示例

测试完成后，Allure会生成详细的测试报告，包括：

- 测试用例执行情况概览
- 失败测试用例详情
- 测试步骤与截图
- 测试执行时长统计

![测试报告示例](./reports/sample_report.png)

## 贡献指南

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建一个Pull Request

## 常见问题

### Q: 如何处理验证码问题？
A: 项目中包含了验证码识别的功能，详见`utils/captcha_utils.py`。在测试环境中，也可以考虑禁用验证码或使用固定验证码。

### Q: 测试失败时如何排查？
A: 查看Allure报告中的失败详情和截图，同时检查日志文件获取更多信息。

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：
- Email: chenmango@gmail.com
- GitHub Issues: [提交Issue](https://github.com/chenmango/yunfan-web-test-automation/issues)
