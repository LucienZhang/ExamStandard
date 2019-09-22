from datetime import datetime

# 输入的 json 源文件路径
source_json_file_path = "/users/hk/dev/ExamStandard/data/"
source_json_file_name = "goldset_93.json"

# 存储结果的 json 文件路径
result_save_path = "/users/hk/dev/ExamStandard/data/"
result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d %I:%M:%S %p')
