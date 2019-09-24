from core.utils import connect
from core.logic.bu_build_work_flow import build_work_flow


def handle_lesion(seg, text, res_seg, i, stack):
    # if seg[i] != stack["lesion_stack"][0]:
    #     stack["lesion_stack"].pop()
    #     stack["lesion_stack"].append(connect(seg[i]))
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    return res_seg, stack
