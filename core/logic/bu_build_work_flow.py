from itertools import product
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.tag_args_kwargs_map import get_args_kwargs_for_build_prod_param_func
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from core.utils import check_build_timing


def build_work_flow(seg, res_seg, i, stack):
    """
    遇到 exam_result, reversed_exam_item, lesion_desc, symptom_desc, treatment_desc 时调用
    :param seg: 子seg
    :param res_seg: 存储该seg的结果
    :param i: 当前标签在seg中的索引
    :param stack: stack = {"ppos": [], "ppo_stack": [], "lesion_stack": [], ...}
    :return: itertools.product 拼接的结果
    """

    # step 1 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
    stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

    # step 2 若 timing 为 True , 则可以开始流程
    timing, clean_ppo_stack = check_build_timing(seg, i)

    if timing:
        # 构造 product_param
        args, kwargs = get_args_kwargs_for_build_prod_param_func(seg[i][2], stack)
        product_params = build_sorted_product_params(*args, **kwargs)

        # 构造结构化结果
        prod_res = list(product(*product_params))

        # 结果存入 res_x
        res_seg.extend(["".join(j) for j in prod_res])

    if clean_ppo_stack:
        stack["ppo_stack"] = []

    return res_seg, stack
