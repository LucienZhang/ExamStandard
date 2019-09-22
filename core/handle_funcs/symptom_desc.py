from itertools import product
from core.utils import connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def handle_symptom_desc(seg, res_seg, i, stack):

    # step 1 把自己和 decorations 中的项拼接, 然后放入deco_desc列表中
    if len(stack["decorations"]) > 0:
        stack["deco_desc"].extend([connect_tag_and_value(j) +
                                   connect_tag_and_value(seg[i]) for j in stack["decorations"]])
    else:
        stack["deco_desc"].append(connect_tag_and_value(seg[i]))

    # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
    if len(stack["ppo_stack"]) > 0:
        pass
    else:
        stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

    if i == len(seg) - 1:
        # 将各个stack放入 itertools.product 函数所需的参数中
        # 注意, 由于较多时候,decorations都可能是空的，所以排序不用decOrations,而使用[x[i]]
        # desc 中需要考虑 entity_neg
        product_params = build_sorted_product_params(stack["exam"], stack["ppos"], [seg[i]],
                                                     stack["entity_neg"], stack["time"],
                                                     exam_stack=stack["exam_stack"],
                                                     ppo_stack=stack["ppo_stack"],
                                                     deco_desc=stack["deco_desc"],
                                                     entity_neg_stack=stack["entity_neg_stack"],
                                                     time_stack=stack["time_stack"])

        # itertools.product
        prod_res = list(product(*product_params))

        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 items, ir, ppo_stack
        stack["decorations"] = []
        stack["deco_desc"] = []
        stack["ppo_stack"] = []

    if i < len(seg) - 1:
        if seg[i + 1][2] != seg[i][2]:
            if seg[i + 1][2] == "symptom_deco":
                if i == len(seg) - 2:
                    tmp_1 = stack["deco_desc"][0]
                    tmp_2 = connect_tag_and_value(seg[i + 1])
                    stack["deco_desc"] = [tmp_1 + tmp_2]

            # 以下为正常情况下的处理流程:

            # 将各个stack放入 itertools.product 函数所需的参数中
            product_params = build_sorted_product_params(stack["exam"], stack["ppos"], [seg[i]],
                                                         stack["entity_neg"], stack["time"],
                                                         exam_stack=stack["exam_stack"],
                                                         ppo_stack=stack["ppo_stack"],
                                                         deco_desc=stack["deco_desc"],
                                                         entity_neg_stack=stack["entity_neg_stack"],
                                                         time_stack=stack["time_stack"])

            # itertools.product
            prod_res = list(product(*product_params))

            # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
            res_seg.extend(["".join(j) for j in prod_res])

            # 清空 items, ir, ppo_stack 和 entity_neg
            stack["decorations"] = []
            stack["deco_desc"] = []
            stack["ppo_stack"] = []

            if seg[i + 1][2] != "symptom_deco":
                stack["entity_neg"] = []

    return res_seg, stack
