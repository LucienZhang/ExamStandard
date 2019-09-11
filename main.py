from itertools import product
import sys
from copy import deepcopy
from utils import *
from data.samples import samples_2

"""
一 从 json 文件获取一整段 targets;
二 将 targets 根据 seg 分成几个 segment
三 定义最终输出 res = []
四 对每一个 segment(也就是x), 做以下处理:

1 初始化定义变量
stack = []
res_x = []  # 每一个x所有结构化的结果，存在res_x中
pos, obj, part = []
idx_pos, idx_obj, idx_part = None, None, None
items, results, decorations = [], [], []
ir, reversed_ir, deco_desc = [], [], []
lesion = None
ll = []  # ll是 lesion_lesion_desc的简写
times = []
treatment, treatment_desc = [], []

2 从每段segment开头开始遍历
A. 若tag为pos:
    a. 将自己放入 pos
    b. 看后一项x[i+1], 若不为pos, 则将pos 放入 stack ,并清空pos
B. 若tag为obj:
    a. 将自己放入 obj
    b. 看后一项, 若不为obj, 则将 obj 放入 stack, 并清空 obj
C. 若tag为part:
    a. 将自己放入 obj
    b. 看后一项, 若不为obj, 则将 obj 放入 stack, 并清空 obj
"""


def build_res_x(stack, res_x, print_info=True):
    # 1 复制一个stack
    copy_stack = deepcopy(stack)
    print("原始stack: ", copy_stack)
    # 2 将stack中所有 tag 为 "ir", "deco_desc", "reversed_ir" 项清空(不包括自己)
    clean_list = ["ir", "deco_desc", "reversed_ir"]
    for m in range(len(copy_stack) - 1):
        if copy_stack[m][0] in clean_list:
            copy_stack[m][1] = []
    # 3 若遇到 obj, 找前面pos, 拼成pos_obj
    # 将stack 结构化成 [['关节'], ['囊', '周围软组织'], ['无'], ['明显肿胀']] 格式
    tmp_stack = [n[1] for n in copy_stack]
    print("处理后的copy_stack: ", tmp_stack)
    # 先将 tmp_stack 中的空列表剔除掉, 防止笛卡尔积product时失败(因为0乘以任何数都为0)
    while [] in tmp_stack:
        for each in tmp_stack:
            if len(each) == 0:
                tmp_stack.pop(tmp_stack.index(each))
        if [] not in tmp_stack:
            print("复制的剔除[]后的stack: ", tmp_stack)
            break
    # 剔除空列表后的 stack = [['关节'], ['囊', '周围软组织'], ['无'], ['明显肿胀']]
    tmp_list = product(*tmp_stack)
    for tmp_tuple in tmp_list:
        tmp = "".join(tmp_tuple)
        res_x.append(tmp)
    if print_info:
        print("res_x:")
        for a in res_x:
            print(a)


def exam_standard(targets):
    segments = split_target(targets)
    res = []

    for x in segments:
        print_segment(x)
        if len(x) <= 1:
            continue

        res_x = []
        stack = []
        pos, obj, part = [], [], []
        idx_pos, idx_obj, idx_part = None, None, None
        idx_dict = dict()
        idx_dict["pos"] = dict()
        idx_dict["obj"] = dict()
        idx_dict["part"] = dict()
        pos_cnt = obj_cnt = part_cnt = 0

        items, results, decorations = [], [], []
        ir, reversed_ir, deco_desc = [], [], []
        idx_ir, idx_reversed_ir, idx_deco_desc = None, None, None
        lesion = None
        ll = []
        times = []
        treatment, treatment_desc = [], []
        idx_entity_neg = None

        for i in range(len(x)):
            tag = x[i][2]
            value = x[i][3]
            if tag == "symptom_pos":
                pos.append(value)
                if x[i + 1][2] != tag:
                    stack.append([tag, pos])
                    pos = []
                    pos_cnt += 1
                    idx_dict["pos"][pos_cnt] = len(stack) - 1
            elif tag == "symptom_obj":
                obj.append(value)
                if x[i + 1][2] != tag:
                    stack.append([tag, obj])
                    obj = []
                    obj_cnt += 1
                    idx_dict["obj"][obj_cnt] = len(stack) - 1
            elif tag == "object_part":
                part.append(value)
                if x[i + 1][2] != tag:
                    stack.append([tag, part])
                    part = []
                    part_cnt += 1
                    idx_dict["part"][part_cnt] = len(stack) - 1
            elif tag == "exam_item":
                items.append(value)
            elif tag == "reversed_exam_result":
                results.append(value)
            elif tag == "symptom_deco":
                decorations.append(value)
            elif tag == "exam_result":
                if len(items) > 0:
                    ir.extend([j + value for j in items])
                elif len(items) == 0:
                    ir.append(value)
                if i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        items = []
                        stack.append([tag, pos])
                        idx_ir = len(stack) - 1
                elif i == len(x) - 1:
                    items = []
                    stack.append([tag, ir])
                    idx_ir = len(stack) - 1
                    build_res_x(stack, res_x, print_info=True)
        res.extend(res_x)
    return res


a = [
    [30, 31, 'symptom_obj', '气管'],
    [33, 36, 'object_part', '1－3级'],
    [37, 39, 'symptom_obj', '支气管'],
    [40, 41, 'exam_result', '通畅'],
    [16, 16, 'vector_seg', '，'],
    [141, 141, 'symptom_obj', '心'],
    [142, 142, 'exam_item', '影'],
    [143, 146, 'exam_result', '始终较浓'],
    [16, 16, 'vector_seg', '，'],

]


if __name__ == "__main__":
    idx = "sample_" + sys.argv[1]
    res = exam_standard(samples_2[idx])
    print("\n最终:\n")
    for r in res:
        print(r)
