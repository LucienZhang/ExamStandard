import json
import sys
import getopt


# 读取json数据
def load_file(file_name="goldset.json"):
    result = []
    line_count = 0
    count = 0
    print('Source file: {}'.format(file_name))
    with open(file_name, 'r', encoding='utf-8') as f:
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
    print('Read source file finished: total={}, valid={}\n'.format(line_count, count))

    return result


# 分割初始文本
def split_target(origin_target):
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
        res.append(origin_target[idx[j]:idx[j+1]])
    for k in res:
        for m in k:
            if m[2] == "vector_seg":
                k.pop(k.index(m))

    return res


def add_optional_parameters(data):
    # 函数所需的参数: data 是加载的初始数据
    # -h --help
    # --text= 输出第x个初始文本
    # --target= 输出第x个标签
    opts, args = getopt.getopt(sys.argv[1:], "-h-o:", ["help", "json=", "csv=",
                                                       "text=", "target=", "output="])

    for opt_name, opt_value in opts:
        if opt_name in ("-h", "--help"):
            print(r'''Optional parameters:
            python load_data_script.py --text <n>  // Print n-th text
            python load_data_script.py --target <n>  // Print n-th target
            ''')
            exit()

        elif opt_name in ("--text",):
            n = int(opt_value)
            print("\n第%d个文本\n" % n)
            print(data[n]["input"]["text"])
        elif opt_name in ("--target",):
            n = int(opt_value)
            print("\n第%d个标签\n" % n)
            for tag in data[n]["target"]:
                print(str(tag) + ",")
                if tag[2] == "vector_seg":
                    print("")
