def handle_pos(seg, text, res_seg, i, stack):
    """
    由于pos又要和obj拼，又要和object_part拼，所以判断会多一些.
    判断流程:
    1 i是否为0
        1.1 i为0 --> 直接入栈
        1.2 i不为0:

            2 前一项是否为 pos/obj/part
                2.1 若是 --> 直接入栈
                2.2 若不是:

                    3 后一项是否为 pos/obj/part
                        3.1 若是 --> 3.1.a 若是obj: 清空ppos, 再入栈;
                                    3.1.b 若是pos: 目前没有这种情况，理论上直接入栈;
                                    3.1.c 若是part: 根据ppos情况处理
                        3.2 若不是 --> 则自己是一个孤伶伶的独立的pos --> 看ppos情况处理
    """

    if i == 0:
        stack["ppos"].append(seg[i])

    else:
        if seg[i - 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
            stack["ppos"].append(seg[i])

        else:
            if seg[i + 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:

                # "双肾(obj)灌注峰同时到达，左(当前pos)肾(obj)峰值较右肾略低。"
                # 由于当前pos左，要和后面的obj"肾"绑定，所以之前的ppos不需要，清空
                if seg[i + 1][2] == "symptom_obj":
                    case = "Popup_All"
                    stack["ppos"] = list()
                    stack["ppos"].append(seg[i])

                # 实际样本暂未遇到
                # 但理论上, 应该是 "肝(obj)大小正常, 左(pos1)右(当前pos2)肾(obj)形态正常"
                # 这种情况, 将当前pos2也直接放入 stack["ppos"] 即可
                elif seg[i + 1][2] == "symptom_pos":
                    case = "Normal"
                    stack["ppos"].append(seg[i])

                # "左侧臀大肌(obj)较右侧缩小，信号不均，边缘模糊，且外侧缘(**当前pos**)皮下脂肪(part)间隙内可见片状长T1长T2异常信号影.."
                elif seg[i + 1][2] == "object_part":
                    if len(stack["ppos"]) > 0:

                        # 双侧股骨(obj)、胫腓骨(obj)骨骺(part)对称，形态未见明显异常，周围(**当前pos**)软组织(part)未见明显异常。
                        # 当前ppos = [[60,61,obj,'股骨'], [63, 65,obj,'胫腓骨'], [66, 67, part,'骨骺']]
                        # 将末尾的 "骨垢", 从 stack['ppos'] 移除, 再将自己入栈
                        if stack["ppos"][-1][2] == "object_part":
                            stack["ppos"].pop()
                            stack["ppos"].append(seg[i])

                        # 实际情况未遇到, 理论上应该是直接入栈, 例如:
                        # "肾(obj)右侧(pos)大小正常, 下方(**当前pos**) 表皮(part)光滑."
                        # stack["ppos"] = [[obj,"肾"], [pos, "右侧"]]
                        # 由于当前pos "下方" 和后面的part"表皮绑定"， 所以"下方"直接入栈即可.
                        elif stack["ppos"][-1][2] == "symptom_pos":
                            stack["ppos"].append(seg[i])

                        # "左侧臀大肌较右侧缩小，信号不均，边缘模糊，且外侧缘(**当前pos**)皮下脂肪(part)可见异常信号影..."
                        # stack["ppos"] = [[65, 66, 'symptom_pos', '左侧'], [67, 69, 'symptom_obj', '臀大肌']]
                        # 当前pos"外侧缘" 绑定的是后面的 part "皮下脂肪"， 所以直接入栈即可.
                        elif stack["ppos"][-1][2] == "symptom_obj":
                            stack["ppos"].append(seg[i])

            # 这种情况, 等于前项也不是ppo, 后项也不是ppo, 就是一个孤零零的独立的 pos
            elif seg[i + 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                if len(stack["ppos"]) > 0:

                    # "纵隔结构无偏移，内(**当前pos**) 未见明显肿大淋巴结"
                    # stack["ppos"] = [[46, 47, 'symptom_obj', '纵隔']]
                    # 当前pos "内", 直接入栈即可
                    if stack["ppos"][-1][2] == "symptom_obj":

                        stack["ppos"].append(seg[i])

                    # "右(pos)叶(obj)体积增大，其内(pos)放射性分布不均匀，中下部(**当前pos**)可见一放射性分布区.."
                    # stack["ppos"] = [['pos', '右'], ['obj', '叶'], ['pos', '内']]
                    # 当前pos"中下部"遇到这种ppos, 因为内是和"叶"绑定的，和自己属于并列pos，那么将"内"出栈，自己"中下部"入栈.
                    elif stack["ppos"][-1][2] == "symptom_pos":
                        stack["ppos"].pop()
                        stack["ppos"].append(seg[i])

                    # 实际暂未遇到, 先按直接入栈处理
                    elif stack["ppos"][-1][2] == "object_part":
                        stack["ppos"].append(seg[i])

    return res_seg, stack
