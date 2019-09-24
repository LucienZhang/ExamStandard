from core.utils import connect


def handle_reversed_exam_result(seg, text, res_seg, i, stack):
    stack["reversed_exam_result_stack"].append(connect(seg[i]))

    return res_seg, stack
