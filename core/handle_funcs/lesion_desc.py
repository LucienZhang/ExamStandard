from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_lesion_desc(seg, res_seg, i, stack):
    stack["lesion_desc_stack"] = [connect(seg[i])]

    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    return res_seg, stack
