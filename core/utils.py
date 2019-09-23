import json


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

    # print('Source file: {}'.format(abs_file_name))
    # print('Read source file finished: total={}, valid={}\n'.format(line_count, count))

    return result


# 分割初始文本
def slice_target(origin_target):
    idx = [0]
    for i in range(len(origin_target)):
        if origin_target[i][2] == "vector_seg":
            if i >= 1:
                if origin_target[i-1][2] == "exam":
                    if i >= 2:
                        if origin_target[i-2][2] == "symptom_obj" or origin_target[i-2][2] == "vector_seg":
                            continue
                    else:
                        continue

                # 样本97
                elif origin_target[i-1][2] == "vector_seg":
                    continue

            # 其他情况正常分割
            if i != 0:
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


def check_build_timing(seg, i):
    """
    检查exam_result, symptom_desc, lesion_desc, treatment_desc, reversed_exam_item 等输出的时机
    :param seg: 一段seg
    :param i: 当前标签索引
    :return: True(拼接) or False(不拼接)
    """

    timing = False

    if seg[i][2] in ["lesion_desc", "treatment_desc"]:
        timing = True

    else:
        if i == len(seg) - 1:
            timing = True

        elif i < len(seg) - 1:
            if seg[i + 1][2] != seg[i][2]:
                timing = True

    return timing


def get_sort_key(elem):
    if isinstance(elem[0], str):
        # elem = "#0$1&symptom_obj*肾"
        return int(elem[0][elem[0].index("$")+1:elem[0].index("&")])


def connect(t):
    connected_str = ""

    try:
        connected_str = "#" + str(t[0]) + "$" + str(t[1]) + "&" + str(t[2]) + "*" + str(t[3])
    except IndexError:
        print("出现问题的seg: ", t, t[0])

    return connected_str


def connect_tag_and_value(t):
    """
    输入: [53, 55, 'symptom_obj', '副鼻窦']
    输出: "$symptom_obj&副鼻窦"
    """
    return "$" + t[2] + "&" + t[3]


# 将所有结果 res_all 存储为 json
def save_res_all_to_json(data, res_all, result_save_path, result_save_name):
    abs_file_name = result_save_path + result_save_name
    save_file = []

    for idx in range(len(data)):
        tmp = dict()
        tmp["id"] = idx
        tmp["text"] = data[idx]["input"]["text"]
        tmp["result"] = res_all[idx]

        save_file.append(tmp)

    with open(abs_file_name, "w") as f:
        f_obj = json.dumps(save_file, ensure_ascii=False, indent=4)
        f.write(f_obj)
