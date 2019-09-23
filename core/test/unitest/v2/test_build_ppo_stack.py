import sys
sys.path.insert(0, "/users/hk/dev/ExamStandard")
from core.test.test_v2 import _check_obj_relationship, _build_ppo_stack_by_ppo_situation,\
    _check_ppo_situation, _connect


def _build_ppo_stack(ppos):
    ppo_stack = []

    if len(ppos) == 1:
        ppo_stack.append(_connect(ppos[0]))

    # 5种情况 o+o, o + part/pos, pos/part + o (肯定有o)
    elif len(ppos) == 2:
        if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj"]:
            obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])
            if obj_rel == 1:
                ppo_stack = [_connect(j) for j in ppos]
            else:
                ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))
        else:
            ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))

    elif len(ppos) > 2:
        # 获得sit
        sit = _check_ppo_situation(ppos)

        # 根据sit，排列出ppo_stack
        ppo_stack = _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit)

    return ppo_stack


if __name__ == "__main__":
    print("ppos长度为1 的测试:\n")
    ppo_stack = []
    ppos = [[0, 1, 'symptom_obj', '胸廓']]
    ppo_stack = _build_ppo_stack(ppos)
    print("ppo_stack:", ppo_stack)

    print("\nppos长度为2的测试:\n")
    ppos = [0, 1, 'symptom_obj', '胸廓'], [2, 3, 'symptom_pos', '两侧']
    ppo_stack = _build_ppo_stack(ppos)
    print("ppo_stack: ", ppo_stack)
