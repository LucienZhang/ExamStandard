from core.logic.bu_build_work_flow import build_work_flow


def handle_lesion_desc(seg, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    return res_seg, stack
