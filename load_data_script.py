from utils import load_file, add_optional_parameters


# 获取数据
file_path = "/users/hk/dev/ExamStandard/data/"
file_name = "goldset_93.json"
data = load_file(file_path + file_name)

# 添加脚本参数
add_optional_parameters(data)