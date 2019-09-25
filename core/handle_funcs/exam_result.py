from core.logic.bu_build_work_flow import build_work_flow
from core.utils import check_build_timing


def handle_exam_result(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    can_clean_stack = check_build_timing(seg, text, i)
    if can_clean_stack:
        stack["exam_item"] = []
        stack["symptom_deco"] = []

    return res_seg, stack
