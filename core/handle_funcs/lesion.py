def handle_lesion(seg, res_seg, i, stack):
    if seg[i] != stack["lesion"][0]:
        stack["lesion"].pop()
        stack["lesion"].append(seg[i])

    return res_seg, stack
