from itertools import product
from core.utils import get_sort_key, connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from core.tag_args_kwargs_map import get_args_kwargs_for_build_prod_param_func


def handle_lesion_desc(seg, res_seg, i, stack):

    if len(stack["lesion"]) > 0:
        tmp_ll_stack = [stack["lesion"], [seg[i]]]
        tmp_ll_stack.sort(key=get_sort_key)
        stack["ll_stack"] = ["".join([connect_tag_and_value(tmp[0]) for tmp in tmp_ll_stack])]

        # 构造ppo_stack
        stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

        stack["lesion_desc"] = [seg[i]]
        args, kwargs = get_args_kwargs_for_build_prod_param_func(seg[i][2], stack)
        product_params = build_sorted_product_params(*args, **kwargs)

        # 拼接
        prod_res = list(product(*product_params))

        # 结果存入res_seg
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 ppo_stack
        stack["ppo_stack"] = []

    return res_seg, stack
