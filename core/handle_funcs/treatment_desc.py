from itertools import product
from core.utils import connect_tag_and_value
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def handle_treatment_desc(seg, res_seg, i, stack):
    # 与 treatment 拼接
    if len(stack["treatment"]) > 0:
        stack["tt_stack"] = [connect_tag_and_value(stack["treatment"][0]) +
                             connect_tag_and_value(seg[i])]

    # 构造 product_param
    product_params = build_sorted_product_params([seg[i]],
                                                 tt_stack=stack["tt_stack"])

    # 构造结构化结果
    prod_res = list(product(*product_params))

    # 结果存入 res_x
    res_seg.extend(["".join(j) for j in prod_res])

    # 清空 tt_stack 和 treatment
    stack["tt_stack"] = []
    stack["treatment"] = []

    return res_seg, stack
