def handle_obj_part(seg, res_seg, i, stack):
    part_special_sit = 0

    if i != 0:
        if seg[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
            if len(stack["ppos"]) > 0:
                if stack["ppos"][-1][2] == "object_part":
                    tail_part_value = stack["ppos"][-1][3]

                    for j in range(len(stack["ppos"]) - 1, -1, -1):
                        if stack["ppos"][j][2] == "symptom_obj":
                            part_special_sit = 1
                            tmp_obj_idx = j
                            break

    if part_special_sit == 1:
        if tail_part_value != "囊性成分":
            stack["ppos"] = stack["ppos"][:tmp_obj_idx + 1]
        else:
            stack["ppos"].pop()

    stack["ppos"].append(seg[i])

    return res_seg, stack
