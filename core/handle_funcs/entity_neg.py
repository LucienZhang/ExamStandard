from core.utils import connect


def handle_entity_neg(seg, text, res_seg, i, stack):
    stack[seg[i][2]] = [connect(seg[i])]

    return res_seg, stack
