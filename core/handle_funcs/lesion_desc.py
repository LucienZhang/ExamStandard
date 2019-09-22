from itertools import product
from core.utils import get_sort_key, connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def handle_lesion_desc(seg, res_seg, i, stack):

    if len(stack["lesion"]) > 0:
        tmp_ll_stack = [stack["lesion"], [seg[i]]]
        tmp_ll_stack.sort(key=get_sort_key)
        stack["ll_stack"] = ["".join([connect_tag_and_value(tmp[0]) for tmp in tmp_ll_stack])]

        # 构造ppo_stack
        stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

        product_params = build_sorted_product_params(stack["exam"], stack["ppos"], [seg[i]],
                                                     stack["entity_neg"], stack["time"],
                                                     exam_stack=stack["exam_stack"],
                                                     ppo_stack=stack["ppo_stack"],
                                                     ll_stack=stack["ll_stack"],
                                                     entity_neg_stack=stack["entity_neg_stack"],
                                                     time_stack=stack["time_stack"])

        prod_res = list(product(*product_params))

        # 结果存入res_x
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 ppo_stack
        stack["ppo_stack"] = []

    return res_seg, stack
