from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_treatment_desc(seg, res_seg, i, stack):
    # step 1
    stack["treatment_desc_stack"] = [connect(seg[i])]

    # step 2 build
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    # 清空变量
    stack["treatment_stack"] = []

    return res_seg, stack
