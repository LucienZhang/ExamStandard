from itertools import product
from core.utils import connect
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_get_product_params_func_args import get_product_params_func_args
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def build_work_flow(seg, text, res_seg, i, stack):
    """
    遇到 exam_result, reversed_exam_item, lesion_desc, symptom_desc, treatment_desc 时调用
    :param seg: 子seg
    :param res_seg: 存储该seg的结果
    :param i: 当前标签在seg中的索引
    :param stack: stack = {"ppos": [], "ppo_stack": [], "lesion_stack": [], ...}
    :return: itertools.product 拼接的结果
    """

    # # 入栈
    # stack["%s_stack" % seg[i][2]] = [connect(seg[i])]
    #
    # # 拼接 ppo_stack
    # stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"])
    #
    # # 构造 product_param
    # args = get_product_params_func_args(seg[i][2], stack)
    # product_params = build_sorted_product_params(*args)
    #
    # # 构造结构化结果
    # prod_res = list(product(*product_params))
    #
    # # 结果存入 res_x
    # for prod_res_One in prod_res:
    #     res_seg.append(prod_res_One)
    #
    # # 清空 ppo_stack
    # stack["ppo_stack"] = []

    # TODO 在原文本遇到逗号，句号等断句时，才输出
    stack["%s_stack" % seg[i][2]].append(connect(seg[i]))

    if text[seg[i][1] + 1] in [",", ".", "，", "。", "、"]:
        print("输出:%s" % seg[i])
        print("开始: %s" %  stack["%s_stack" % seg[i][2]])
        stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"])

        args = get_product_params_func_args(seg[i][2], stack)
        product_params = build_sorted_product_params(*args)

        prod_res = list(product(*product_params))

        for prod_res_One in prod_res:
            res_seg.append(prod_res_One)

        stack["ppo_stack"] = []
        stack["%s_stack" % seg[i][2]] = []

        print("输出完成, 清空stack: %s" %  stack["%s_stack" % seg[i][2]])

    return res_seg, stack
