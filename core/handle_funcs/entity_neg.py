from core.utils import connect


def handle_entity_neg(seg, text, res_seg, i, stack):
    stack["entity_neg_stack"] = [connect(seg[i])]

    return res_seg, stack
