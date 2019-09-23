from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_exam_result(seg, res_seg, i, stack):
    # step 1
    stack["exam_result_stack"].append(connect(seg[i]))

    # step 2 build 结果
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    # 判断何时清空变量
    stack["exam_item_stack"] = []
    stack["exam_result_stack"] = []

    return res_seg, stack
