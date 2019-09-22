from core.utils import connect_tag_and_value


def handle_medical_events(seg, res_seg, i, stack):
    stack["medical_events"] = [seg[i]]
    stack["medical_events_stack"] = [connect_tag_and_value(seg[i])]

    return res_seg, stack
