def handle_exam_item(seg, res_seg, i, stack):
    stack["items"].append(seg[i])

    return res_seg, stack
