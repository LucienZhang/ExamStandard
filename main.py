import core.utils as Utils
from core.exam_standard import ExamStandardProcessor


def main():
    # 实例化
    json_file_path = "/users/hk/dev/ExamStandard/data/"
    json_file_name = "test.json"
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

    return esp.output_list


if __name__ == "__main__":
    final_res = main()
    print("最终结果:\n")
    for res_seg in final_res:
        for r in res_seg:
            print(r)
