seg = [
    [40, 40, 'symptom_pos', '双'],
    [41, 41, 'symptom_obj', '肾'],
    [42, 43, 'exam_item', '峰值'],
    [44, 46, 'exam_result', '较低平']
]


stack_dict = {
    "ppos": [],
    "ppo_stack": [],
    "items": [],
    "ir": [],
    "result": []
}

res_seg = []


def func_pos(seg, res_seg, i, stack):
    stack["ppos"].append(seg[i])
    print("func_pos函数结束, stack[ppos]: %s" % stack["ppos"])

    return res_seg, stack


def func_obj(seg, res_seg, i, stack):
    stack["ppos"].append(seg[i])
    print("func_obj函数结束, stack[ppos]: %s" % stack["ppos"])

    return res_seg, stack


def func_item(seg, res_seg, i, stack):
    print("先这样试试: ", stack)
    stack["items"].append(seg[i])
    print("item函数结束, stack[items]: ", stack["items"])

    return res_seg, stack


def func_result(seg, res_seg, i, stack):
    stack["result"].append(seg[i])
    for t in tag_res_map["exam_result"]:
        stack[t] = []

    print("func_result函数结束, stack[result]: ", stack["result"])

    return res_seg, stack


tag_func_map = {
    "symptom_pos": func_pos,
    "symptom_obj": func_obj,
    "exam_item": func_item,
    "exam_result": func_result
}


# tag_req_param_map = {
#     "obj": [],
#     "result": [2, 3]
# }
#
#
tag_res_map = {
    "symptom_obj": ["ppos"],
    "exam_item": ["items"],
    "exam_result": ["items", "ir", "ppo_stack", "exam_stack"]
}


if __name__ == "__main__":
    for i in range(len(seg)):
        res_seg, stack_dict = tag_func_map[seg[i][2]](seg, res_seg, i, stack_dict)
    print("结果:")
    print("res_seg: ", res_seg)
    print("stack: ", stack_dict)
