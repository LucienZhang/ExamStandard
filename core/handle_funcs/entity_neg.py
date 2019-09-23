from core.utils import connect


def handle_entity_neg(seg, res_seg, i, stack):
    stack["entity_neg"].append(seg[i])
    stack["entity_neg_stack"] = [connect(seg[i])]

    return res_seg, stack
