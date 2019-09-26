from core.utils import connect
from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.logic.bu_check_ppo_situation import check_ppo_situation
from core.logic.bu_build_ppo_stack_by_ppo_situation import build_ppo_stack_by_ppo_situation


def build_ppo_stack(ppos, text):
    """
    :param text: 原文本, "双肾大小正常,...."
    :param ppos: 即 stack["ppos"] = [[110, 110, 'symptom_pos', '双'], [111, 111, 'symptom_obj', '肾']]
    :return: ppo_stack: 即 stack["ppo_stack"] = ["#110$110&symptom_pos*双^#111$111&symptom_obj*肾^"]
    """

    ppo_stack = []

    if len(ppos) == 1:
        ppo_stack.append(connect(ppos[0]))

    elif len(ppos) == 2:

        # 如果ppos中是 obj + obj 情况, 需要判断关系
        if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj"]:
            obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])
            if obj_rel == 1:
                ppo_stack = [connect(j) for j in ppos]
            else:
                ppo_stack.append(connect(ppos[0]) + connect(ppos[1]))

        # 如果是其他情况，按ppos中的顺序放入ppo_stack
        else:
            ppo_stack.append(connect(ppos[0]) + connect(ppos[1]))

    elif len(ppos) > 2:
        # 获得situation
        situation = check_ppo_situation(ppos)

        # 根据sit，排列出ppo_stack
        ppo_stack = build_ppo_stack_by_ppo_situation(ppos, situation, text)

    return ppo_stack

