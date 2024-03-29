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

            # 特殊情况1 , 当遇到 "左手腕" + "正位片" + vector_seg 时，这种seg不分割
            # [6, 6, 'symptom_pos', '左'],
            # [7, 7, 'symptom_obj', '手'],
            # [9, 9, 'symptom_obj', '腕'],
            # [11, 13, 'exam', '正位片'],
            # [24, 24, 'vector_seg', '，'],
            # [25, 26, 'symptom_obj', '尺骨'],
            # [27, 28, 'object_part', '茎突'],
            # [29, 30, 'symptom_deco', '开始'],
            # [31, 32, 'symptom_desc', '形成'],
            # [33, 33, 'vector_seg', '，'],
            # [40, 41, 'exam', '骨龄'],
            # [42, 47, 'exam_result', '约为6.5岁'],
            # [48, 48, 'vector_seg', '。'],

            # 样本1 特殊情况2
            # 遇到 "餐后扫查"时, 这种seg不分割
            # [2, 2, 'vector_seg', '，'],
            # [3, 6, 'exam', '餐后扫查'],
            # [7, 7, 'vector_seg', '，'],

            # 样本97 特殊情况3
            # 这种连着2个vector_seg, 那么2个都不分割
            # [0, 1, 'symptom_obj', '腹部'],
            # [2, 5, 'exam', '急诊扫描'],
            # [6, 6, 'vector_seg', '，'],
            # [18, 18, 'vector_seg', '。']

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


# 检查print的时机
def check_print_timing(exam_result_tag, origin_text):
    """

    :param exam_result_tag: [49, 50, 'exam_result', '正常']
    :param origin_text: "肝脏大小、形态正常，表面平整光滑，实质回声尚均匀。"
    :return: 是否是一个可以输出的时机 (True or False)
    """

    flags = [",", "，", ".", "。"]
    can_print = False

    if origin_text[exam_result_tag[1] + 1] in flags:
        can_print = True

    return can_print


def get_sort_key(elem):
    """
    用途: some_list.sort(key=_get_sort_key)
    参数: elem: 列表中的元素
    """

    if isinstance(elem, list):
        return elem[-1][0]

    elif isinstance(elem, dict):
        return int(list(elem.keys())[0])


def connect_tag_and_value(t):
    """
    输入: [53, 55, 'symptom_obj', '副鼻窦']
    输出: "$symptom_obj&副鼻窦"
    """
    return "$" + t[2] + "&" + t[3]
