def handle_reversed_exam_result(seg, res_seg, i ,stack):
    stack["results"].append(seg[i])

    return res_seg, stack
