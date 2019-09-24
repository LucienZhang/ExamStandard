from core.exam_standard import ExamStandardProcessor
from init_source_json_data import source_data


def exam_standard_job_func(cfg):
    # 实例化
    esp = ExamStandardProcessor()

    # run
    res_all = []
    for source_data_idx in range(len(source_data)):
        res_segments = esp.run(source_data, source_data_idx)
        res_all.append(
            {source_data_idx: res_segments}
        )

    return res_all
