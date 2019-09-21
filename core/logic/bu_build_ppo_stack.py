from core.utils import connect_tag_and_value
from core.logic.bu_check_obj_relationship import check_obj_relationship


def build_ppo_stack(ppos, ppo_stack):
    if len(ppos) == 1:
        ppo_stack.append(connect_tag_and_value(ppos[0]))

    # 5种情况 o+o, o + part/pos, pos/part + o (肯定有o)
    elif len(ppos) == 2:
        # 只有o+o需要判断2者关系(并列/从属/没关系)
        # 先来的obj是other_obj, 后来的是self_obj
        if ppos[0][2] == "symptom_obj" and ppos[1][2] == "symptom_obj":
            obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])
            if obj_rel == 1:
                ppo_stack = [connect_tag_and_value(j) for j in ppos]
            else:
                ppo_stack.append(connect_tag_and_value(ppos[0]) + connect_tag_and_value(ppos[1]))
        else:
            ppo_stack.append(connect_tag_and_value(ppos[0]) + connect_tag_and_value(ppos[1]))

    elif len(ppos) > 2:
        # 获得sit
        sit = _check_ppo_situation(ppos)

        # 根据sit，排列出ppo_stack
        ppo_stack = _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit)

    return ppo_stack