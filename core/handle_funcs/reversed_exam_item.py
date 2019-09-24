from core.logic.bu_build_work_flow import build_work_flow


def handle_reversed_exam_item(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    # 清 reversed_exam_result
    if i < len(seg) - 1:
        if seg[i+1][2] != seg[i][2]:
            stack["reversed_exam_result"] = []

    return res_seg, stack
