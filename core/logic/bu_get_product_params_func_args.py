"""
该文件作用:
给 logic / bu_build_sorted_product_params 函数构造 *args
*args 根据 tag_args_kwargs_map 构造;
"""

tag_args_map = {
    "exam_result": ["exam", "ppo_stack", "exam_item", "exam_result",
                    "lesion", "medical_events", "time", "treatment"],

    "reversed_exam_item": ["exam", "ppo_stack", "reversed_exam_item", "reversed_exam_result",
                           "lesion", "medical_events", "time"],

    "symptom_desc": ["exam", "ppo_stack", "symptom_deco", "symptom_desc",
                     "entity_neg", "time"],

    "lesion_desc": ["exam", "ppo_stack", "entity_neg",
                    "lesion", "lesion_desc", "time"],

    "treatment_desc": ["treatment", "treatment_desc"],

    "lesion": ["exam", "ppo_stack", "entity_neg", "exam_item", "exam_result",
               "lesion", "lesion_desc", "time"]
}


def get_product_params_func_args(tag, stack):
    args = [stack[key] for key in tag_args_map[tag]]

    return args
