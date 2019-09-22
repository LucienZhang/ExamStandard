from itertools import product
from core.utils import connect_tag_and_value, check_exam_result_build_timing
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from core.tag_args_kwargs_map import get_args_kwargs_for_build_prod_param_func


def handle_reversed_exam_item(seg, res_seg, i, stack):
    # step 1 把自己和 results 中的项拼接, 然后放入 reversed_ir 列表中 (不用考虑entity_neg)
    if len(stack["results"]) > 0:
        stack["reversed_ir"].extend([connect_tag_and_value(j) +
                                     connect_tag_and_value(seg[i]) for j in stack["results"]])
    else:
        stack["reversed_ir"].append(connect_tag_and_value(seg[i]))

    # step 2 将 ppos 中的项, 按照不同情况拼接后，放入ppo_stack中
    stack["ppo_stack"] = build_ppo_stack(ppos=stack["ppos"], ppo_stack=stack["ppo_stack"])

    # step 3 若 timing 为 True, 则可以开始流程
    timing, clean_ppo_stack = check_exam_result_build_timing(seg, i)

    if timing:
        args, kwargs = get_args_kwargs_for_build_prod_param_func(seg[i][2], stack)
        product_params = build_sorted_product_params(*args, **kwargs)

        prod_res = list(product(*product_params))

        res_seg.extend(["".join(j) for j in prod_res])

        stack["items"] = []
        stack["ir"] = []

    if clean_ppo_stack:
        stack["ppo_stack"] = []

    return res_seg, stack

