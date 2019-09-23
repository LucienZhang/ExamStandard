from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_reversed_exam_item(seg, res_seg, i, stack):
    stack["reversed_exam_item_stack"].append(connect(seg[i]))

    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    # 判断何时清空变量
    stack["reversed_exam_result_stack"] = []
    stack["reversed_exam_item_stack"] = []

    return res_seg, stack

