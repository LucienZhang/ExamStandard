"""
该文件用来给 build_sorted_product_params 函数构造 *args, 和 **kwargs
*args 根据 tag_args_kwargs_map 构造;
**kwargs 根据 tag_args_kwargs_map 和 args_kwargs_map 2张表进行构造.
"""

args_kwargs_map = {
    "exam": "exam_stack",
    "ppos": "ppo_stack",
    "exam_result": "ir",
    "lesion": "lesion_stack",
    "medical_events": "medical_events_stack",
    "time": "time_stack",
    "treatment": "treatment_stack",
    "results": "reversed_ir",
    "symptom_desc": "deco_desc",
    "entity_neg": "entity_neg_stack"
}

tag_args_kwargs_map = {
    "exam_result": ["exam", "ppos", "exam_result", "lesion", "medical_events", "time", "treatment"],
    "reversed_exam_item": ["exam", "ppos", "results", "lesion", "medical_events", "time"],
    "symptom_desc": ["exam", "ppos", "symptom_desc", "entity_neg", "time"]
}


def get_args_kwargs_for_build_prod_param_func(tag, stack):
    args = [stack[key] for key in tag_args_kwargs_map[tag]]

    kwargs = dict()
    for key in tag_args_kwargs_map[tag]:
        kwargs[args_kwargs_map[key]] = stack[args_kwargs_map[key]]

    return args, kwargs
