import core.utils as Utils
from core.exam_standard import ExamStandardProcessor

from config import source_json_file_path, source_json_file_name, result_save_path, result_save_name


def main():
    # 实例化
    esp = ExamStandardProcessor(source_json_file_path, source_json_file_name)

    # 1 load source json file
    data = esp.load_source_json_file()

    # 2 start run
    for n in range(len(data)):
        sliced_targets = esp.slice_origin_target(n)
        text = data[n]["input"]["text"]
        Utils.display_sliced_segments(n, sliced_targets)

        for seg in sliced_targets:
            esp.process_seg_one(seg, text)

        esp.put_res_segments_to_res_all(n)

    # 3 save all 100 results to json
    esp.save_res_all_to_json(result_save_path, result_save_name)


if __name__ == "__main__":
    main()
