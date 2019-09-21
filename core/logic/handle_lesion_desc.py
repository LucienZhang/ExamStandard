from itertools import product
from core.utils import get_sort_key, connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params


def handle_lesion_desc(seg, res_seg, i, ppos, lesion, exam, entity_neg, time,
                       exam_stack, ppo_stack, entity_neg_stack, time_stack):

    if len(lesion) > 0:
        tmp_ll_stack = [lesion, [seg[i]]]
        tmp_ll_stack.sort(key=get_sort_key)
        ll_stack = ["".join([connect_tag_and_value(tmp[0]) for tmp in tmp_ll_stack])]

        # 构造ppo_stack
        ppo_stack = build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

        product_params = build_sorted_product_params(exam, ppos, [seg[i]], entity_neg, time,
                                                     exam_stack=exam_stack,
                                                     ppo_stack=ppo_stack,
                                                     ll_stack=ll_stack,
                                                     entity_neg_stack=entity_neg_stack,
                                                     time_stack=time_stack)

        prod_res = list(product(*product_params))

        # 结果存入res_x
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 ppo_stack
        ppo_stack = []

    return res_seg, ppo_stack
