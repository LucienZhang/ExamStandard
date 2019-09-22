from itertools import product
from core.utils import connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def handle_reversed_exam_item(seg, res_seg, i, stack):
    # step 1 把自己和 results 中的项拼接, 然后放入 reversed_ir 列表中 (不用考虑entity_neg)
    if len(stack["results"]) > 0:
        stack["reversed_ir"].extend([connect_tag_and_value(j) +
                                     connect_tag_and_value(seg[i]) for j in stack["results"]])
    else:
        stack["reversed_ir"].append(connect_tag_and_value(seg[i]))

    # step 2 将 ppos 中的项, 按照不同情况拼接后，放入ppo_stack中
    stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

    # step 3 遇到最后一个 reversed_exam_item ("如信号影")时, 输出+清空有关变量
    if i == len(seg) - 1:
        # 将各个stack放入 itertools.product 函数所需的参数中
        product_params = build_sorted_product_params(stack["exam"], stack["ppos"],
                                                     stack["results"], stack["lesion"],
                                                     stack["medical_events"], stack["time"],
                                                     ppo_stack=stack["ppo_stack"],
                                                     exam_stack=stack["exam_stack"],
                                                     reversed_ir=stack["reversed_ir"],
                                                     lesion_stack=stack["lesion_stack"],
                                                     medical_events_stack=stack["medical_events_stack"],
                                                     time_stack=stack["time_stack"])

        # itertools.product
        prod_res = list(product(*product_params))

        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 items, ir, ppo_stack
        stack["results"] = []
        stack["reversed_ir"] = []
        stack["ppo_stack"] = []

    elif i < len(seg) - 1:
        if seg[i + 1][2] != seg[i][2]:
            # 将各个stack放入 itertools.product 函数所需的参数中
            product_params = build_sorted_product_params(stack["exam"], stack["ppos"],
                                                         stack["results"], stack["lesion"],
                                                         stack["medical_events"], stack["time"],
                                                         ppo_stack=stack["ppo_stack"],
                                                         exam_stack=stack["exam_stack"],
                                                         reversed_ir=stack["reversed_ir"],
                                                         lesion_stack=stack["lesion_stack"],
                                                         medical_events_stack=stack["medical_events_stack"],
                                                         time_stack=stack["time_stack"])

            # itertools.product
            prod_res = list(product(*product_params))

            # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
            res_seg.extend(["".join(j) for j in prod_res])

            # 清空 items, ir, ppo_stack
            stack["results"] = []
            stack["reversed_ir"] = []
            stack["ppo_stack"] = []

    return res_seg, stack
