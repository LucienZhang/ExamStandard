from core.logic.bu_build_work_flow import build_work_flow


def handle_symptom_desc(seg, text, res_seg, i, stack):
    res_seg, stack = build_work_flow(seg, text, res_seg, i, stack)

    # 清变量
    stack["ppo_stack"] = []
    if i < len(seg) - 1:
        if seg[i+1][2] != seg[i][2]:
            stack["symptom_deco"] = []
            stack["entity_neg"] = []

    return res_seg, stack
