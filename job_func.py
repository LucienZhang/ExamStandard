from core.exam_standard import ExamStandardProcessor
from core.utils import load_json_file, save_res_all_to_json


def exam_standard_job_func(cfg):
    # load source data
    source_data = load_json_file(cfg["source_json_file_path"] + cfg["source_json_file_name"])

    # 实例化
    esp = ExamStandardProcessor(cfg["esp_config"])

    # run
    res_all = []
    for source_data_one in source_data:
        res_segments = esp.run(source_data_one)
        res_all.append(res_segments)

    # save as json
    save_res_all_to_json(source_data, res_all, cfg["result_save_path"])

    return res_all
