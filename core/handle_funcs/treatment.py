from core.utils import connect


def handle_treatment(seg, text, res_seg, i, stack):
    stack["treatment_stack"] = [connect(seg[i])]

    return res_seg, stack
