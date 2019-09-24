from core.utils import connect


def handle_medical_events(seg, text, res_seg, i, stack):
    stack["medical_events_stack"] = [connect(seg[i])]

    return res_seg, stack
