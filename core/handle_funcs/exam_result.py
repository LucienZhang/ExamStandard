from core.utils import connect_tag_and_value
from core.logic.bu_build_work_flow import build_work_flow


def handle_exam_result(seg, res_seg, i, stack):
    # step 1
    stack["exam_result"] = [seg[i]]

    # step 2 把自己和items中的项拼接, 然后放入ir列表中 (不用考虑entity_neg)
    if len(stack["items"]) > 0:
        stack["ir"].extend([connect_tag_and_value(j) + connect_tag_and_value(seg[i]) for j in stack["items"]])
    else:
        stack["ir"].append(connect_tag_and_value(seg[i]))

    # step 3 build 结果
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    return res_seg, stack
