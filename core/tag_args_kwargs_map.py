from core.init_stack import init_stack

args_kwargs_map = {
        "exam": "exam_stack",
        "ppos": "ppo_stack",
        "exam_result": "ir",
        "lesion": "lesion_stack",
        "medical_events": "medical_events_stack",
        "time": "time_stack",
        "treatment": "treatment_stack"
    }

tag_args_kwargs_map = {
    "exam_result": {
        "args": ["exam", "ppos", "exam_result", "lesion", "medical_events", "time", "treatment"]
    }
}


def get_args_kwargs_for_build_prod_param_func(tag, stack):
    args = [stack[key] for key in tag_args_kwargs_map[tag]["args"]]

    kwargs = dict()
    for key in tag_args_kwargs_map[tag]["args"]:
        kwargs[[args_kwargs_map[key]]] = stack[[args_kwargs_map[key]]]

stack = init_stack()
print(stack)
