from core.utils import connect_tag_and_value


def handle_treatment(seg, res_seg, i, stack):
    stack["treatment"] = [seg[i]]
    stack["treatment_stack"] = [connect_tag_and_value(seg[i])]

    return res_seg, stack
