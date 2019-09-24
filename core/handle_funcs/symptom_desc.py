# from core.logic.bu_build_work_flow import build_work_flow
from core.utils import connect
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_get_product_params_func_args import get_product_params_func_args
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from itertools import product


def handle_symptom_desc(seg, text, res_seg, i, stack):
    # res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    # 入栈
    stack[seg[i][2]] = [connect(seg[i])]

    # 拼接 ppo_stack
    stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"])

    # 构造 product_param
    args = get_product_params_func_args(seg[i][2], stack)
    product_params = build_sorted_product_params(*args)

    # 构造结构化结果
    prod_res = list(product(*product_params))

    # 结果存入 res_x
    for prod_res_One in prod_res:
        res_seg.append(prod_res_One)

    # 清变量
    stack["ppo_stack"] = []
    if i < len(seg) - 1:
        if seg[i+1] != seg[i][2]:
            stack["symptom_deco"] = []

    return res_seg, stack
