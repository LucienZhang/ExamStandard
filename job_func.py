from core.exam_standard import ExamStandardProcessor


def exam_standard_job_func(cfg):
    # 实例化
    esp = ExamStandardProcessor(cfg["source_json_file_path"], cfg["source_json_file_name"])

    # load source json file
    source_data = esp.load_source_json_file()

    res_all = []
    # run
    for source_data_idx in range(len(source_data)):
        res_segments = esp.run(source_data, source_data_idx)
        res_all.append(
            {source_data_idx: res_segments}
        )

    for res in res_all:
        for k, v in res.items():
            print(k)
            for vone in v:
                print(vone)
            print("\n")
    return res_all
