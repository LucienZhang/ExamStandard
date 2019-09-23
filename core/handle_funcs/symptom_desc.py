from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_symptom_desc(seg, res_seg, i, stack):
    # step 1
    stack["symptom_desc_stack"].append(connect(seg[i]))

    # step3 build
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    # 判断何时清空变量
    stack["symptom_deco_stack"] = []
    stack["symptom_desc_stack"] = []

    return res_seg, stack
