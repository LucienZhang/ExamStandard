def handle_pos(seg, text, res_seg, i, stack):
    if i == 0:
        stack["ppos"].append(seg[i])

    else:
        if seg[i - 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
            stack["ppos"].append(seg[i])

        else:
            if seg[i + 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
                if seg[i + 1][2] == "symptom_obj":
                    ppos = list()
                    ppos.append(seg[i])

                elif seg[i + 1][2] == "symptom_pos":
                    pass

                elif seg[i + 1][2] == "object_part":
                    if len(stack["ppos"]) > 0:
                        if stack["ppos"][-1][2] == "object_part":
                            stack["ppos"].pop()
                            stack["ppos"].append(seg[i])

                        elif stack["ppos"][-1][2] == "symptom_pos":
                            pass

                        elif stack["ppos"][-1][2] == "symptom_obj":
                            stack["ppos"].append(seg[i])

            elif seg[i + 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                if len(stack["ppos"]) > 0:
                    if stack["ppos"][-1][2] == "symptom_obj":
                        stack["ppos"].append(seg[i])

                    elif stack["ppos"][-1][2] == "symptom_pos":
                        stack["ppos"].pop()
                        stack["ppos"].append(seg[i])

                    elif stack["ppos"][-1][2] == "object_part":
                        # 没有遇到
                        pass

    return res_seg, stack
