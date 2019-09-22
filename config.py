from datetime import datetime

# 作为输入的json文件路径
json_file_path = "/users/hk/dev/ExamStandard/data/"
json_file_name = "goldset_93.json"

# 存储结果的json文件路径
result_save_path = "/users/hk/dev/ExamStandard/data/"
result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d %I:%M:%S %p')
