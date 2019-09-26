from core.logic.build_ppo_stack_funcs.obj import build_ppo_stack_by_obj
from core.logic.build_ppo_stack_funcs.part_obj import build_ppo_stack_by_part_obj
from core.logic.build_ppo_stack_funcs.pos_obj import build_ppo_stack_by_pos_obj
from core.logic.build_ppo_stack_funcs.pos_part_obj import build_ppo_stack_by_pos_part_obj


# {situation: func}
# 1 stack["ppos"]中只有 obj, 例:
# ppos = [["obj","肾"], ["obj","肝"], ["obj", "肺"]]

# 2 stack["ppos"]中有 obj, part, 例:
# ppos = [["obj","肾"], ["part","皮质"], ["obj", "肺"]]

# 3 stack["ppos"]中有 obj pos, 例:
# ppos = [["obj","肾"], ["pos","左侧"], ["obj", "肺"]]

# 4 stack["ppos"]中有 obj pos part, 例:
# ppos = [["obj","肾"], ["part","皮质"], ["pos","左侧"], ["obj", "肺"], ["part","肺泡"]]
build_ppo_stack_func_map = {
    1: build_ppo_stack_by_obj,
    2: build_ppo_stack_by_part_obj,
    3: build_ppo_stack_by_pos_obj,
    4: build_ppo_stack_by_pos_part_obj
}


def build_ppo_stack_by_ppo_situation(ppos, situation, text):
    ppo_stack = []

    if situation is not None:
        ppo_stack = build_ppo_stack_func_map[situation](ppos, ppo_stack, text)

    return ppo_stack
