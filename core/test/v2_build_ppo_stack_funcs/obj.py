from core.test.test_v2 import _check_obj_relationship, _connect


def build_ppo_stack_by_obj(ppos, ppo_stack):
    obj_rel = _check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])
    if obj_rel == 1:
        ppo_stack = [_connect(j) for j in ppos]
    else:
        ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))
    return ppo_stack
