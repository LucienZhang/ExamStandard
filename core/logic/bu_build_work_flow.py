from itertools import product
from core.utils import connect, check_build_timing
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_get_product_params_func_args import get_product_params_func_args
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def build_work_flow(seg, text, res_seg, i, stack):
    """
    遇到 exam_result, reversed_exam_item, lesion, lesion_desc, treatment_desc, symptom_desc 时调用
    :param seg: 子seg
    :param text: 原文本, "肝大小正常, 形态规则,...."
    :param res_seg: 存储该seg的结果
    :param i: 当前标签在seg中的索引
    :param stack: stack = {"ppos": [..], "ppo_stack": [..], "lesion": [..], "exam_item": [..], ...}
    :return: res_seg: itertools.product 拼接的结果
    """

    stack[seg[i][2]].append(connect(seg[i]))

    can_build = check_build_timing(seg, text, i)

    if can_build:
        stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], text=text)

        args = get_product_params_func_args(seg[i][2], stack)
        product_params = build_sorted_product_params(*args)

        prod_res = list(product(*product_params))

        for prod_res_One in prod_res:
            res_seg.append(prod_res_One)

        stack["ppo_stack"] = []

        if seg[i][2] != "lesion":
            stack[seg[i][2]] = []

    return res_seg, stack
