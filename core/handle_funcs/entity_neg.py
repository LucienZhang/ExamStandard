from core.utils import connect_tag_and_value


def handle_entity_neg(seg, res_seg, i, stack):
    stack["entity_neg"].append(seg[i])
    stack["entity_neg_stack"] = [connect_tag_and_value(seg[i])]

    return res_seg, stack
