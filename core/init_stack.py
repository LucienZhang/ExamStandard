stack_key_list = [
    "ppos", "ppo_stack",
    "exam_item", "exam_result",
    "symptom_deco", "symptom_desc",
    "reversed_exam_result", "reversed_exam_item",
    "entity_neg",
    "lesion", "lesion_desc",
    "exam",
    "time",
    "medical_events",
    "treatment", "treatment_desc"
]


def init_stack():
    stack_dict = dict()
    for key in stack_key_list:
        stack_dict[key] = []

    return stack_dict
