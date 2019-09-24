from core.exam_standard import ExamStandardProcessor


def exam_standard_job_func(cfg):

    # 读取cfg
    source_json_file_path = cfg["source_json_file_path"]
    source_json_file_name = cfg["source_json_file_name"]

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
