from utils import load_file, add_optional_parameters

# 获取数据
data = load_file("/users/hk/dev/ExamStandard/data/goldset_93.json")

# 添加脚本参数
add_optional_parameters(data)