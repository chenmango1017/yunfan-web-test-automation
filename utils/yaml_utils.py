import os
import yaml

"""
存放所有中间变量，数据请清晰，调用直接写于写出测试用例就可以，可以存放令牌token这些
一般可以在confetst.py中写入，可以在操作前后清空yaml里面数据，因为测试多次，数据会重复多次存放
"""
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(project_root, "data", "login_extract.yaml")

class yaml_utils:
    @classmethod
    def read_yaml(cls):
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            return [(item['username'], item['password']) for item in data]
    @classmethod
    def write_yaml(cls):
        with open(file_path, mode="a+", encoding="utf-8") as f:
            yaml.dump({"data": "123"}, stream=f,allow_unicode=True)

    #清空
    @classmethod
    def clear_yaml(cls):
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.truncate()
    @classmethod
    def read_url(cls):
        with open(r"D:\pycharm\code\exam_selenium\url_extract.yaml", "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            t=[(item['url']) for item in data]
            return t[0]
    @classmethod
    def read_exam(cls):
        with open(r"D:\pycharm\code\exam_selenium\data\exam_extract.yaml", "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            return data["test_cases"]
    @classmethod
    def read_exercise(cls):
        with open(r"D:\pycharm\code\exam_selenium\data\exercise_extract.yaml", "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            return data
    @classmethod
    def read_paper(cls):
        with open(r"D:\pycharm\code\exam_selenium\data\paper_extract.yaml", "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            return data

    @classmethod
    def read_question(cls):
        with open(r"D:\pycharm\code\exam_selenium\data\question_extract.yaml", "r", encoding="utf-8") as f:
            data = yaml.load(f,yaml.FullLoader)
            return data.get("test_data", [])
if __name__ == '__main__':
    # yaml_utils.write_yaml()
    # yaml_utils.clear_yaml()

     print(yaml_utils.read_question())