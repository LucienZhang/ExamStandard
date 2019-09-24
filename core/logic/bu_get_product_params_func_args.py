"""
该文件作用:
给 logic / bu_build_sorted_product_params 函数构造 *args
*args 根据 tag_args_kwargs_map 构造;
"""

tag_args_map = {
    "exam_result": ["exam_stack", "ppo_stack", "exam_item_stack", "exam_result_stack",
                    "lesion_stack", "medical_events_stack", "time_stack", "treatment_stack"],

    "reversed_exam_item": ["exam_stack", "ppo_stack", "reversed_exam_item_stack", "reversed_exam_result_stack",
                           "lesion_stack", "medical_events_stack", "time_stack"],

    "symptom_desc": ["exam_stack", "ppo_stack", "symptom_deco_stack", "symptom_desc_stack",
                     "entity_neg_stack", "time_stack"],

    "lesion_desc": ["exam_stack", "ppo_stack", "entity_neg_stack",
                    "lesion_stack", "lesion_desc_stack", "time_stack"],

    "treatment_desc": ["treatment_stack", "treatment_desc_stack"]
}


def get_product_params_func_args(tag, stack):
    args = [stack[key] for key in tag_args_map[tag]]

    return args
