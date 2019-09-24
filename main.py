from core.exam_standard import ExamStandardProcessor
from datetime import datetime


def main():
    # 输入的 json 源文件路径
    source_json_file_path = "/users/hk/dev/ExamStandard/data/"
    source_json_file_name = "goldset_93.json"

    # 存储结果的 json 文件路径
    result_save_path = "/users/hk/dev/ExamStandard/data/"
    result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d_%I:%M:%S__%p')

    # 实例化
    esp = ExamStandardProcessor(source_json_file_path, source_json_file_name)

    # 1 load source json file
    data = esp.load_source_json_file()

    # 2 start run
    for n in range(len(data)):
        sliced_targets = esp.slice_origin_target(n)
        text = data[n]["input"]["text"]

        for seg in sliced_targets:
            esp.process_seg_one(seg, text)

        esp.put_res_segments_to_res_all(n)

    # 3 save all 100 results to json
    esp.save_res_all_to_json(result_save_path, result_save_name)


if __name__ == "__main__":
    main()
