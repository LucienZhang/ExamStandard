from core.utils import connect


def handle_lesion(seg, res_seg, i, stack):
    if seg[i] != stack["lesion_stack"][0]:
        stack["lesion_stack"].pop()
        stack["lesion_stack"].append(connect(seg[i]))

    return res_seg, stack
