from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.utils import connect_tag_and_value


def build_ppo_stack_by_obj(ppos, ppo_stack):
    obj_rel = check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])
    if obj_rel == 1:
        ppo_stack = [connect_tag_and_value(j) for j in ppos]
    else:
        ppo_stack.append(connect_tag_and_value(ppos[0]) + connect_tag_and_value(ppos[1]))
    return ppo_stack
