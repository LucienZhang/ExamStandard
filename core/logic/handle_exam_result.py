from core.utils import connect_tag_and_value
from core.logic.bu_build_ppo_stack import build_ppo_stack
from core.logic.bu_build_sorted_product_params import build_sorted_product_params
from itertools import product


def handle_exam_result(seg, res_seg, items, ir, i, ppos, exam, lesion, medical_events, time, treatment,
                       ppo_stack, exam_stack, lesion_stack, medical_events_stack, time_stack, treatment_stack):

    # step 1 把自己和items中的项拼接, 然后放入ir列表中 (不用考虑entity_neg)
    if len(items) > 0:
        ir.extend([connect_tag_and_value(j) + connect_tag_and_value(seg[i]) for j in items])
    else:
        ir.append(connect_tag_and_value(seg[i]))

    # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
    ppo_stack = build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

    if i == len(seg) - 1:
        # 将各个stack放入 itertools.product 函数所需的参数中
        product_params = build_sorted_product_params(exam, ppos, [seg[i]], lesion,
                                                     medical_events, time, treatment,
                                                     exam_stack=exam_stack,
                                                     ppo_stack=ppo_stack,
                                                     ir=ir,
                                                     lesion_stack=lesion_stack,
                                                     medical_events_stack=medical_events_stack,
                                                     time_stack=time_stack,
                                                     treatment_stack=treatment_stack)

        # itertools.product
        prod_res = list(product(*product_params))

        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
        res_seg.extend(["".join(j) for j in prod_res])

        # 清空 items, ir, ppo_stack
        items, ir, exam_stack, ppo_stack = [], [], [], []

    elif i < len(seg) - 1:
        if seg[i + 1][2] != seg[i][2]:
            # 将各个stack放入 itertools.product 函数所需的参数中
            product_params = build_sorted_product_params(exam, ppos, [seg[i]], lesion,
                                                         medical_events, time, treatment,
                                                         exam_stack=exam_stack,
                                                         ppo_stack=ppo_stack,
                                                         ir=ir,
                                                         lesion_stack=lesion_stack,
                                                         medical_events_stack=medical_events_stack,
                                                         time_stack=time_stack,
                                                         treatment_stack=treatment_stack)

            # itertools.product
            prod_res = list(product(*product_params))

            # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
            res_seg.extend(["".join(j) for j in prod_res])

            # 清空 items, ir, ppo_stack
            items, ir = [], []

        ppo_stack = []

    return res_seg, items, ir, ppo_stack, exam_stack
