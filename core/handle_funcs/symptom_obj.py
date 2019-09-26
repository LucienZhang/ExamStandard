from core.logic.bu_check_obj_relationship import check_obj_relationship


def handle_obj(seg, text, res_seg, i, stack):
    """
    示例结构:
    A...， B C ...，D E...

    判断流程：
    1 i 是否为0
        1.1 i==0 --> 直接入栈 (即A)
        1.2 i>0:

            2 前一项是否为pos/obj/part
                2.1 若是 --> 直接入栈 (即 C 或 E)
                2.2 若不是: (B或者D)

                    3 stack["ppos"]中是否有obj
                        3.1 若有 --> 2者判断关系
                            3.1.a 若并列 --> 将栈清空 (即A和C并列, 则将stack中的A移除，再将C放入)
    """
    # step 1 定义初始 case
    case = "Normal"

    # step 2 根据 stack["ppos"], 判断特殊 case

    # 原文: "腹腔扫查，未见明显肿大淋巴结。"
    # "腹腔obj" + "扫查exam"这种结构, 因为在exam处, 腹腔已经和扫查拼到一起，所以这里"腹腔"obj不需要再入栈.
    if i == 0:
        if i < len(seg) - 1:
            if seg[i + 1][2] == "exam":
                case = "Popup_Self"

    elif i > 0:

        # 右肾盂obj、肾盏obj显影清楚，肾小盏(当前obj)杯口锐利，
        # seg[i-1] == [38, 39, 'exam_result', '清楚']
        if seg[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
            if len(stack["ppos"]) > 0:

                # stack["ppos"] = [[obj,肾盂]]
                # 需要比较"肾盂" 和 当前obj "肾小盏" 的关系
                if "symptom_obj" in [j[2] for j in stack["ppos"]]:
                    for k in stack["ppos"]:
                        if k[2] == "symptom_obj":
                            other_obj = k[3]
                            break

                    # 查看2个obj关系, 1并列 2包含
                    obj_rel = check_obj_relationship(self_obj=seg[i][3], other_obj=other_obj)
                    if obj_rel == 1:
                        case = "Popup_All"

    # step 3 根据case，处理 stack["ppos"]
    if case == "Popup_All":
        stack["ppos"] = list()

    stack["ppos"].append(seg[i])

    if case == "Popup_Self":
        stack["ppos"].pop()

    return res_seg, stack
