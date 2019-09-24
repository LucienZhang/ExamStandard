from core.utils import load_json_file


source_json_file_path = "/users/hk/dev/ExamStandard/data/"
source_json_file_name = "goldset_93.json"
file_path = source_json_file_path + source_json_file_name

source_data = load_json_file(file_path)
