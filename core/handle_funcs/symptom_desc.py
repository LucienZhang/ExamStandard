from core.utils import connect_tag_and_value
from core.logic.bu_build_work_flow import build_work_flow


def handle_symptom_desc(seg, res_seg, i, stack):
    # step 1
    stack["symptom_desc"] = [seg[i]]

    # step 2 和 decorations 中的项拼接, 然后放入deco_desc列表中
    if len(stack["decorations"]) > 0:
        stack["deco_desc"].extend([connect_tag_and_value(j) +
                                   connect_tag_and_value(seg[i]) for j in stack["decorations"]])
    else:
        stack["deco_desc"].append(connect_tag_and_value(seg[i]))

    # step3 build
    res_seg, stack = build_work_flow(seg, res_seg, i, stack)

    stack["decorations"] = []
    stack["deco_desc"] = []

    return res_seg, stack
