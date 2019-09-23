from core.exam_standard import ExamStandardProcessor
from datetime import datetime


def exam_standard_job_func(cfg):

    # 读取cfg
    source_json_file_path = cfg["source_json_file_path"]
    source_json_file_name = cfg["source_json_file_name"]

    result_save_path = cfg["result_save_path"]
    result_save_name_prefix = cfg["result_save_name_prefix"]
    result_save_name = result_save_name_prefix + "_%s" % datetime.now().strftime('%y-%m-%d_%I:%M:%S__%p') + ".json"

    # 实例化
    esp = ExamStandardProcessor(source_json_file_path, source_json_file_name)

    # 1 load source json file
    data = esp.load_source_json_file()

    # 2 start run
    for n in range(len(data)):
        sliced_targets = esp.slice_origin_target(n)
        text = data[n]["input"]["text"]
        # display_sliced_segments(n, sliced_targets)

        for seg in sliced_targets:
            esp.process_seg_one(seg, text)

        esp.put_res_segments_to_res_all(n)

    # 3 save all 100 results to json
    esp.save_res_all_to_json(result_save_path, result_save_name)
