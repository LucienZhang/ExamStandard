from core.utils import connect


def handle_exam(seg, text, res_seg, i, stack):
    # step 1 定义初始状态
    stack[seg[i][2]] = [connect(seg[i])]
    case = "Normal"

    # step 2 判断特殊情况
    # "ConcatObj case"
    # 原文: "肝胆显像示：静脉注射示踪剂 1分钟即见心、肝、双肾隐约显影，"
    if i == 1:
        if seg[i - 1][2] == "symptom_obj":
            case = "ConcatPreviousObj"

    # "ConcatObj case"
    # 原文: "静脉注射显像剂后1-30分钟、60分钟分别行腹部前位显像，1分钟可见肝脏显影, ..."
    if seg[i][3] == "前位显像":
        case = "ConcatPreviousObj"

    # step 3 根据 case，赋值
    if case == "ConcatPreviousObj":
        stack[seg[i][2]] = [connect(seg[i - 1]) + connect(seg[i])]

    elif case == "Normal":
        stack[seg[i][2]] = [connect(seg[i])]

    return res_seg, stack
