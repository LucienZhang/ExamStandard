from itertools import product
from core.utils import connect_tag_and_value, check_exam_result_build_timing
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from core.tag_args_kwargs_map import get_args_kwargs_for_build_prod_param_func


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

    print("遇到desc:", seg[i])
    # step 3 若 timing 为 True, 则可以开始流程
    timing, clean_ppo_stack = check_exam_result_build_timing(seg, i)

    if timing:
        print("timing:", seg[i], "deco_desc:", stack["deco_desc"])
        stack["symptom_desc"] = [seg[i]]
        args, kwargs = get_args_kwargs_for_build_prod_param_func(seg[i][2], stack)
        print("kwargs:", kwargs)
        product_params = build_sorted_product_params(*args, **kwargs)

        prod_res = list(product(*product_params))

        res_seg.extend(["".join(j) for j in prod_res])

        stack["decorations"] = []
        stack["deco_desc"] = []

    if clean_ppo_stack:
        stack["ppo_stack"] = []

    return res_seg, stack
