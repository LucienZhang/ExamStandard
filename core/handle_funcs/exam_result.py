from core.logic.bu_build_work_flow import build_work_flow


def handle_exam_result(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    if i < len(seg) - 1:
        if seg[i+1][2] != seg[i][2]:
            stack["exam_item"] = []

    return res_seg, stack
