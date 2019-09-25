import json
from datetime import datetime


# 读取json数据
def load_json_file(abs_file_name):
    result = []
    line_count = 0
    count = 0

    with open(abs_file_name, 'r', encoding='utf-8') as f:
        for line in f:
            line_count = line_count + 1
            if line_count % 1000 == 0:
                print('line --- {}'.format(line_count))
            try:
                dic = json.loads(line)
                result.append(dic)
                count = count + 1
            except Exception as e:
                print(e)
                print('error line: {}'.format(line))

    return result


# 分割初始文本
def slice_target(origin_target):
    idx = [0]
    for i in range(len(origin_target)):
        if origin_target[i][2] != "vector_seg":
            continue

        if i == 0:
            continue

        if i >= 1:
            if origin_target[i - 1][2] == "exam":
                if i >= 2:
                    # 原文本: 根据标准左手、腕的正位片，与女孩骨龄标准对比，尺骨茎突开始形成，该女孩的实际骨龄约为 6.5 岁。
                    # 遇到"正位片"则不切分
                    # [6, 6, 'symptom_pos', '左'],
                    # [7, 7, 'symptom_obj', '手'],
                    # [9, 9, 'symptom_obj', '腕'],
                    # [11, 13, 'exam', '正位片'],
                    # [24, 24, 'vector_seg', '，']
                    if origin_target[i-2][2] == "symptom_obj" or origin_target[i-2][2] == "vector_seg":
                        continue
                else:
                    # i = 1
                    # 原文: "急诊，餐后扫查，肠气干扰明显，图像质量欠佳: ...."
                    # [3, 6, 'exam', '餐后扫查'],
                    # [7, 7, 'vector_seg', '，'],
                    continue

            # 连续2个vector_seg, 2个都不分割
            # 原文: ""腹部急诊扫描，胃肠道未准备，大致观察。"
            # [0, 1, 'symptom_obj', '腹部'],
            # [2, 5, 'exam', '急诊扫描'],
            # [6, 6, 'vector_seg', '，'],
            # [18, 18, 'vector_seg', '。']
            elif origin_target[i - 1][2] == "vector_seg":
                continue

            # 其他情况正常分割
            idx.append(i)

    res = []
    for j in range(len(idx) - 1):
        res.append(origin_target[idx[j]:idx[j + 1]])
    for k in res:
        for m in k:
            if m[2] == "vector_seg":
                k.pop(k.index(m))

    return res


# 逐个打印 seg
def display_sliced_segments(idx, sliced_segments):
    print("\n第%d个标注:\n" % idx)
    for seg in sliced_segments:
        for s in seg:
            print(s)
        print("")


def get_sort_key(elem):
    start_idx = None
    end_idx = None
    
    # elem = ["#0$1&symptom_obj*肾"]
    for i in range(len(elem[-1]) - 1, -1, -1):
        if elem[-1][i] == "&":
            end_idx = i
        elif elem[-1][i] == "$":
            start_idx = i
            break

    return elem[-1][start_idx+1:end_idx]


def connect(t):
    connected_str = ""

    try:
        connected_str = "#" + str(t[0]) + "$" + str(t[1]) + "&" + str(t[2]) + "*" + str(t[3]) + "^"
    except IndexError:
        print("出现问题的seg: ", t, t[0])

    return connected_str


def check_build_timing(seg, text, i):
    can_build = True
    tag = seg[i][2]

    # symptom_desc 和 treatment_desc 默认 True
    if tag in ["exam_result", "lesion", "lesion_desc", "reversed_exam_item"]:
        if text[seg[i][1] + 1] not in [",", "，", ".", "。", ";", "；", "("]:
            can_build = False

    return can_build


# 将所有结果 res_all 存储为 json
def save_res_all_to_json(data, res_all, result_save_path):
    result_save_name = "result_%s.json" % datetime.now().strftime('%y-%m-%d_%I:%M:%S_%p')
    abs_file_name = result_save_path + result_save_name

    save_file = []
    for idx in range(len(data)):
        save_file.append(
            {
                "id": idx,
                "text": data[idx]["input"]["text"],
                "res": res_all[idx]
            }
        )

    with open(abs_file_name, "w") as f:
        f_obj = json.dumps(save_file, ensure_ascii=False, indent=4)
        f.write(f_obj)
