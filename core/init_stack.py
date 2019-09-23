stack_key_list = [
    "ppos", "ppo_stack",
    "exam_item_stack", "exam_result_stack",
    "symptom_deco_stack", "symptom_desc_stack",
    "reversed_exam_result_stack", "reversed_exam_item_stack",
    "entity_neg_stack",
    "lesion_stack", "lesion_desc_stack",
    "exam_stack",
    "time_stack",
    "medical_events_stack",
    "treatment_stack", "treatment_desc_stack"
]


def init_stack():
    stack_dict = dict()
    for key in stack_key_list:
        stack_dict[key] = []

    return stack_dict
