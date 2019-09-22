from core.utils import connect_tag_and_value


def handle_time(seg, res_seg, i, stack):
    stack["time"] = [seg[i]]
    stack["time_stack"] = [connect_tag_and_value(seg[i])]

    return res_seg, stack
