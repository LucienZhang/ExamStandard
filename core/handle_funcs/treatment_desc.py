from core.utils import connect_tag_and_value
from core.logic.bu_build_work_flow import build_work_flow


def handle_treatment_desc(seg, res_seg, i, stack):
    # step 1
    stack["treatment_desc"] = [seg[i]]

    # step 2 与 treatment 拼接
    if len(stack["treatment"]) > 0:
        stack["tt_stack"] = [connect_tag_and_value(stack["treatment"][0]) +
                             connect_tag_and_value(seg[i])]

    # step 3 build
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    stack["tt_stack"] = []
    stack["treatment"] = []

    return res_seg, stack
