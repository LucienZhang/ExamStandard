import core.utils as Utils
from core.exam_standard import ExamStandardProcessor

from config import json_file_path, json_file_name, result_save_path, result_save_name


def main():
    # 实例化
    esp = ExamStandardProcessor(json_file_path, json_file_name)

    # 1 读取json文件
    data = esp.load_json_file()
    # print(esp.data)

    # 2 run
    for n in range(len(data)):
        sliced_targets = esp.slice_origin_target(n)
        text = data[n]["input"]["text"]
        Utils.display_sliced_segments(n, sliced_targets)

        for seg in sliced_targets:
            esp.process_seg_one(seg, text)

        esp.put_output_list_to_all_result(n)

    # 3 save to json
    esp.save_to_json(result_save_path, result_save_name)

    return esp.all_result


if __name__ == "__main__":
    final_res = main()
