from core.utils import connect


def handle_symptom_deco(seg, text, res_seg, i, stack):
    stack[seg[i][2]].append(connect(seg[i]))

    return res_seg, stack
