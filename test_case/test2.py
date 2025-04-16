from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://exam.yfhl.net/pages/login/login")
driver.maximize_window()
sleep(2)

driver.find_element(By.XPATH, '//span[contains(text(),"管理员")]').click()

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"考试管理")]'))).click()
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"在线考试")]'))).click()

wait = WebDriverWait(driver, 20)

# 🔍 定位“1 - 考试”所在行的 checkbox（就是 <span class="el-checkbox__inner">）
checkbox_span = wait.until(EC.presence_of_element_located((
    By.XPATH,
    '//a[contains(text(), "数学测试001")]/ancestor::tr//span[contains(@class, "el-checkbox__inner")]'
)))

# ✅ 用 JS 点它，绕过框架限制（Element UI 很容易遮挡或绑定奇怪事件）
driver.execute_script("arguments[0].click();", checkbox_span)

sleep(4)
driver.find_element(By.XPATH, '//span[contains(text(),"删除")]').click()
sleep(3)
driver.find_element(By.XPATH, '//span[contains(text(),"确定")]').click()
sleep(2)

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"云帆考试")]'))
)
element.click()

element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//li[contains(text(),'学员首页')]"))
)
element.click()
sleep(10)

d_links = driver.find_elements(By.CSS_SELECTOR, "a.d-link")

# 假设默认是删除成功
is_deleted = True

for link in d_links:
    if link.text == "数学测试001":
        is_deleted = False
        break

# 🔥 加入断言，确保“数学测试001”确实不存在
assert is_deleted, "❌ 删除失败：数学测试001 仍然存在！"


driver.quit()