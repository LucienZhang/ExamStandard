from json_loader import JsonLoader
from exam_standard import ExamStandardProcessor

# 1 读取json文件
json_file_path = "/users/hk/dev/ExamStandard/data/"
json_file_name = "goldset_93.json"
json_loader = JsonLoader(json_file_path, json_file_name)

# 2 从json文件中读取 原文本 text 和 原标注结果 target
data = json_loader.load_file()

# 3 对每一个文本, 初始化一个 ExamStandard 类
esp = ExamStandardProcessor(text=data[11]["input"]["text"], targets=data[11]["target"])
segments = esp.slice_targets(display=True)


