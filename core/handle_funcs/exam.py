from core.utils import connect_tag_and_value


def handle_exam(seg, res_seg, i, stack):
    stack["exam"] = [seg[i]]
    exam_special_sit = 0

    if i == 1:
        if seg[i - 1][2] == "symptom_obj":
            exam_special_sit = 1

    if seg[i][3] == "前位显像":
        exam_special_sit = 1

    if exam_special_sit == 1:
        stack["exam_stack"] = [connect_tag_and_value(seg[i - 1]) +
                               connect_tag_and_value(seg[i])]

    else:
        stack["exam_stack"] = [connect_tag_and_value(seg[i])]

    return res_seg, stack
