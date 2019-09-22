from itertools import product
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.tag_args_kwargs_map import get_args_kwargs_for_build_prod_param_func
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from core.utils import check_build_timing


def build_work_flow(seg, res_seg, i, stack):
    # step 1 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
    stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

    # step 2 若 timing 为 True , 则可以开始流程
    timing, clean_ppo_stack = check_build_timing(seg, i)

    if timing:
        # 构造 product_param
        stack["treatment_desc"] = [seg[i]]
        args, kwargs = get_args_kwargs_for_build_prod_param_func(seg[i][2], stack)
        product_params = build_sorted_product_params(*args, **kwargs)

        # 构造结构化结果
        prod_res = list(product(*product_params))

        # 结果存入 res_x
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 tt_stack 和 treatment
        stack["tt_stack"] = []
        stack["treatment"] = []

    if clean_ppo_stack:
        stack["ppo_stack"] = []

    return res_seg, stack
