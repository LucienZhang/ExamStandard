from core.logic.build_ppo_stack_funcs.build_ppo_stack_func_map import build_ppo_stack_func_map


def build_ppo_stack_by_ppo_situation(ppos, situation, text):
    ppo_stack = []

    if situation is not None:
        ppo_stack = build_ppo_stack_func_map[situation](ppos, ppo_stack, text)

    return ppo_stack
