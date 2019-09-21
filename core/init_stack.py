stack_key_list = [
    "ppos", "ppo_stack",
    "items", "ir",
    "decorations", "deco_desc",
    "results", "reversed_ir",
    "entity_neg", "entity_neg_stack",
    "lesion", "lesion_stack", "ll_stack",
    "exam", "exam_stack",
    "time", "time_stack",
    "medical_events", "medical_events_stack",
    "treatment", "treatment_stack", "treatment_desc_stack"
]


stack_dict = dict()
for key in stack_key_list:
    stack_dict[key] = []


# ppos, ppo_stack = [], []
# items, decorations = [], []
# results, reversed_ir = [], []
# ir, deco_desc = [], []
# medical_events, medical_events_stack = [], []
# treatment, treatment_stack, tt_stack = [], [], []
# exam, exam_stack = [], []
# time, time_stack = [], []
# entity_neg, entity_neg_stack = [], []
# lesion = []
# lesion_stack = []
