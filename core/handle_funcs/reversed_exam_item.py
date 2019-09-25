from core.logic.bu_build_work_flow import build_work_flow


def handle_reversed_exam_item(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    stack["reversed_exam_result"] = []
    stack["reversed_exam_item"] = []
    return res_seg, stack
