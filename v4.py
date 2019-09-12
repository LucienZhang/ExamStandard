from itertools import product


# 之前将所有标签放入一个统一 stack
# v4.py 分成多个 stack (ppo_stack, ir_stack, exam_stack等)


# 该函数用来构造 itertools.product 所需的参数
# 正确参数举例: [["$obj&肾", "%obj&肝脏"], ["$item&大小$exam_result&正常"]]
# 错误参数举例: [["$obj&肾", "%obj&肝脏"], [], [], ["$item&大小$exam_result&正常"]]
def _build_product_param(*stacks):
    ans = []
    for stackOne in stacks:
        if len(stackOne) > 0:
            ans.append(stackOne)
    return ans


# 示例seg
x = [
    [0, 1, 'symptom_obj', '胸廓'],
    [2, 3, 'symptom_pos', '两侧'],
    [2, 3, 'exam_item', '形态'],
    [4, 5, 'exam_result', '正常'],
    [6, 7, 'exam_result', '清楚']
]

# 初始化参数
pos_or_obj_or_part = ["symptom_pos", "symptom_obj", "object_part"]

ppos, ppo_stack = [], []

items, ir = [], []

exam_stack, treatment_stack, medical_events = [], [], []

# res_x 存储一个seg (seg也就是x) 内所有拼接好的结果
res_x = []


# 主函数
for i in range(len(x)):
    tag = x[i][2]
    value = "$" + x[i][2] + "&" + x[i][3]

    if tag == "symptom_pos":
        ppos.append([value])

    elif tag == "symptom_obj":
        if len(ppos) == 0:
            ppos.append(value)
            if x[i + 1][2] not in pos_or_obj_or_part:
                ppo_stack.append(value)
        else:
            if tag not in [j[j.index("$") + 1:j.index("&")] for j in ppos]:
                ppos.append(x[i][2:])
            else:
                # 这里做两个obj之间的关系判断, 目前先直接拼一起
                # 例子: ppo_stack = ["$obj&肾"]
                # 加入新的后: []
                pass

    elif tag == "exam_item":
        items.append(value)
    elif tag == "exam_result":
        # 遇到 exam_result, 一般做3件事:
        # a 把自己和items中的项拼接, 然后放入ir列表中
        # 剩下的2件事是: b 把拼好的输出写入 res_x; c 并且在适当时候清空有关变量值
        # 但是b和c在处理时, 分为情况1和情况2, 下面有具体解释

        # step_a: 和 item 拼接, 并放入ir (ir 是 item_result简写)
        if len(items) > 0:
            ir.extend([j + value for j in items])
        else:
            ir.append(value)

        # 情况1举例 (i == len(x) - 1)
        # 遇到"正常"时，不会输出到 res_x中;
        # 遇到"清楚"时, 会做2件事: 输出到res_x + 清空items, ir, ppo_stack
        # [0, 1, 'symptom_obj', '头颅'],
        # [2, 3, 'exam_item', '形态'],
        # [4, 5, 'exam_result', '正常'],
        # [4, 5, 'exam_result', '清楚']
        if i == len(x) - 1:
            # 将各个stack放入 itertools.product 函数所需的参数中
            product_params = _build_product_param(ppo_stack, ir, exam_stack, treatment_stack)

            # itertools.product
            prod_res = list(product(*product_params))

            # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
            res_x.extend(["".join(j) for j in prod_res])

            # 清空 items, ir, ppo_stack
            items, ir, ppo_stack = [], [], []

        # 情况2举例 i < len(x) - 1)
        # 当遇到"均匀", "不宽"时，都会做2件事: 输出 + 清空变量
        # [9, 11, 'symptom_obj', '头部'],
        # [17, 19, 'exam_item', '骨密度'],
        # [20, 21, 'exam_result', '均匀'],
        # [23, 24, 'exam_item', '颅缝'],
        # [25, 26, 'exam_result', '不宽']
        # ...
        if i < len(x) - 1:
            if x[i + 1][2] != tag:
                # 将各个stack放入 itertools.product 函数所需的参数中
                product_params = _build_product_param(ppo_stack, ir, exam_stack, treatment_stack)

                # itertools.product
                prod_res = list(product(*product_params))

                # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                res_x.extend(["".join(j) for j in prod_res])

                # 清空 items, ir, ppo_stack
                items, ir, ppo_stack = [], [], []


if __name__ == "__main__":
    print('items: ', items)
    print("ir: ", ir)
    print("ppos: ", ppos)
    print("ppo_stack: ", ppo_stack)
    print("product_param: ", product_params)
    print("prod_res: ", prod_res)
    print("res_x: ", res_x)
