from itertools import product


# 该文件是 _build_sorted_product_params 函数的使用说明


def _get_sort_key(elem):
    ans = None
    if isinstance(elem, list):
        ans = elem[-1][0]
    elif isinstance(elem, dict):
        ans = int(list(elem.keys())[0])

    return ans


def _build_sorted_product_params(*args, **stacks):
    """
    1 该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
    2 返回的结果, 将作为 __build_product_param 函数的参数
    :param stacks: items, exam_stack, ppos 等
    :return: 根据索引排好先后顺序的列表
    """
    stack_map = {
        "exam_stack": ["exam"],
        "ppo_stack": ["symptom_pos", "symptom_obj", "object_part"],
        "ir": ["exam_item"],
        "deco_desc": ["symptom_deco"],
        "reversed_ir": ["reversed_exam_result"]
    }

    tmp1 = []
    # print(stacks)
    for i in list(args):
        if len(i) > 0:
            tmp1.append(i)
    print("排序前: ", tmp1)
    tmp1.sort(key=_get_sort_key)
    print("排序后: %s\n" % tmp1)

    tmp2 = []
    c = 0
    for j in tmp1:
        tmp2.append({c: j[0][2]})
        c += 1
    print("tmp2:\n%s\n" % tmp2)

    tmp3 = []
    for t in tmp2:
        for k, v in stack_map.items():
            if list(t.values())[0] in v:
                tmp3.append({int(list(t.keys())[0]): k})
    print("tmp3:\n%s\n" % tmp3)

    res = []
    for each_stack in tmp3:
        for stack_name, stack_value in stacks.items():
            if stack_name == list(each_stack.values())[0]:
                res.append({int(list(each_stack.keys())[0]): stack_value})
    print("加入实际数据后的res:\n%s\n" % res)

    res.sort(key=_get_sort_key)
    print("排序后res:\n%s\n" % res)
    sorted_product_params = [list(r.values())[0] for r in res]

    return sorted_product_params


# 示例数据
complete_seg = [
                   [0, 1, 'symptom_pos', '双侧'],
                   [2, 2, 'symptom_obj', '额'],
                   [3, 3, 'symptom_obj', '颞'],
                   [4, 6, 'symptom_obj', '顶枕叶'],
                   [7, 9, 'symptom_obj', '脑沟内'],
                   [12, 14, 'lesion_desc', '许多条'],
                   [15, 16, 'lesion_desc', '索状'],
                   [17, 21, 'lesion', '异常信号影'],
                   [24, 27, 'lesion_desc', '额叶明显'],
                   [29, 32, 'exam_item', 'T1WI'],
                   [33, 36, 'exam_result', '略低信号'],
                   [38, 44, 'exam_item', 'T2WI水抑制'],
                   [45, 48, 'exam_result', '稍高信号'],
                   [50, 53, 'exam_result', '边界清楚'],
                   [55, 57, 'exam', 'DWI'],
                   # [58, 61, 'reversed_exam_result', '未见明显'],
                   # [62, 64, 'reversed_exam_item', '高信号'],
                   [66, 72, 'lesion_desc', '无明显占位效应'],
                   [73, 73, 'vector_seg', '，'],
               ],
ppos = [[15, 16, 'symptom_pos', '双侧'], [17, 18, 'symptom_obj', '乳腺'], [19, 20, 'object_part', '腺体']]
results = [[34, 41, 'reversed_exam_result', '其内未见明显异常']]
exam = [[28, 31, 'exam', 'CDFI']]

ppo_stack = ['$symptom_pos&左侧$symptom_obj&乳腺$object_part&腺体']
exam_stack = ['$exam&CDFI']
reversed_ir = ['$reversed_exam_result&其内未见明显异常$reversed_exam_item&血流信号']

a = _build_sorted_product_params(ppos, results, exam,
                                 ppo_stack=ppo_stack,
                                 exam_stack=exam_stack,
                                 reversed_ir=reversed_ir)

print("使用示例数据的结果:\n%s\n" % a)
print("对以上结果进行排列组合:\n%s\n" % list(product(*a)))
