from core.utils import connect_tag_and_value
from core.logic.bu_build_work_flow import build_work_flow


def handle_reversed_exam_item(seg, res_seg, i, stack):
    # step 1 把自己和 results 中的项拼接, 然后放入 reversed_ir 列表中 (不用考虑entity_neg)
    if len(stack["results"]) > 0:
        stack["reversed_ir"].extend([connect_tag_and_value(j) +
                                     connect_tag_and_value(seg[i]) for j in stack["results"]])
    else:
        stack["reversed_ir"].append(connect_tag_and_value(seg[i]))

    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    stack["items"] = []
    stack["ir"] = []

    return res_seg, stack

