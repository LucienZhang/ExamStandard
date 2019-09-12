import json


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
            idx.append(i)
    res = []
    for j in range(len(idx) - 1):
        res.append(origin_target[idx[j]:idx[j+1]])
    for k in res:
        for m in k:
            if m[2] == "vector_seg":
                k.pop(k.index(m))
    return res


def print_segment(segment):
    print("\n")
    for i in segment:
        print(i)
