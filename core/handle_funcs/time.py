from core.utils import connect


def handle_time(seg, text, res_seg, i, stack):
    stack["time_stack"] = [connect(seg[i])]

    return res_seg, stack
