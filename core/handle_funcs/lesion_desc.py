from core.utils import get_sort_key, connect_tag_and_value
from core.logic.bu_build_work_flow import build_work_flow


def handle_lesion_desc(seg, res_seg, i, stack):
    stack["lesion_desc"] = [seg[i]]

    tmp_ll_stack = [stack["lesion"], [seg[i]]]
    tmp_ll_stack.sort(key=get_sort_key)
    stack["ll_stack"] = ["".join([connect_tag_and_value(tmp[0]) for tmp in tmp_ll_stack])]

    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    return res_seg, stack
