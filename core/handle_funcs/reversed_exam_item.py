from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_reversed_exam_item(seg, res_seg, i, stack):
    stack["reversed_exam_item_stack"].append(connect(seg[i]))

    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    stack["items"] = []
    stack["ir"] = []

    return res_seg, stack

