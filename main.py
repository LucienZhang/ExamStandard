from core.exam_standard import ExamStandardProcessor
from datetime import datetime
from core.utils import save_res_all_to_json


def main():
    # 输入的 json 源文件路径
    source_json_file_path = "/users/hk/dev/ExamStandard/data/"
    source_json_file_name = "test.json"

    # 实例化
    esp = ExamStandardProcessor(source_json_file_path, source_json_file_name)

    # load source json file
    source_data = esp.load_source_json_file()

    res_all = []
    # run
    for source_data_idx in range(len(source_data)):
        res_segments = esp.run(source_data, source_data_idx)
        res_all.append(
            {source_data_idx: res_segments}
        )

    # 3 save 100 res_all to json
    # 存储结果的 json 文件路径
    result_save_path = "/users/hk/dev/ExamStandard/data/"
    result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d_%I:%M:%S_%p')
    save_res_all_to_json(source_data, res_all, result_save_path, result_save_name)

    return res_all


if __name__ == "__main__":
    res_all = main()
