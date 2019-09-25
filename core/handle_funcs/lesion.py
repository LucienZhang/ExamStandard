from core.logic.bu_build_work_flow import build_work_flow


def handle_lesion(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    stack["lesion_desc"] = []

    return res_seg, stack
