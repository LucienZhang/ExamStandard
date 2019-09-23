from core.test.v2_build_ppo_stack_funcs.obj import build_ppo_stack_by_obj
from core.test.v2_build_ppo_stack_funcs.part_obj import build_ppo_stack_by_part_obj
from core.test.v2_build_ppo_stack_funcs.pos_obj import build_ppo_stack_by_pos_obj
from core.test.v2_build_ppo_stack_funcs.pos_part_obj import build_ppo_stack_by_pos_part_obj


# {situation: func}
# 1 obj
# 2 obj part
# 3 obj pos
# 4 obj pos part
build_ppo_stack_func_map = {
    1: build_ppo_stack_by_obj,
    2: build_ppo_stack_by_part_obj,
    3: build_ppo_stack_by_pos_obj,
    4: build_ppo_stack_by_pos_part_obj
}
