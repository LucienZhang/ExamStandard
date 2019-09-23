from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_exam_result(seg, res_seg, i, stack):
    # step 1
    stack["exam_result_stack"].append(connect(seg[i]))

    # step 3 build 结果
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    return res_seg, stack
