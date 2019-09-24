from core.exam_standard import ExamStandardProcessor
from datetime import datetime


def main():
    # 输入的 json 源文件路径
    source_json_file_path = "/users/hk/dev/ExamStandard/data/"
    source_json_file_name = "test.json"

    # 存储结果的 json 文件路径
    result_save_path = "/users/hk/dev/ExamStandard/data/"
    result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d_%I:%M:%S__%p')

    # 实例化
    esp = ExamStandardProcessor(source_json_file_path, source_json_file_name)

    res_all = []
    # 1 load source json file
    data = esp.load_source_json_file()

    # 2 start run
    for n in range(len(data)):
        res_segment = esp.run(n)
        res_all.append(
            {n: res_segment}
        )

    return res_all


if __name__ == "__main__":
    res_all = main()

    for res in res_all:
        for k, v in res.items():
            for vone in v:
                print(vone)
