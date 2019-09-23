from core.utils import connect


def handle_symptom_deco(seg, res_seg, i, stack):
    deco_special_sit = 0

    if "symptom_desc" not in [k[2] for k in seg[i:]]:
        deco_special_sit = 1
    else:
        if i < len(seg) - 1:
            if seg[i + 1][2] not in ["symptom_pos", "symptom_obj", "object_part"]:
                if seg[i + 1][2] not in ["symptom_deco", "symptom_desc"]:
                    deco_special_sit = 2

    if deco_special_sit not in [1, 2]:
        stack["symptom_deco_stack"].append(connect(seg[i]))

    return res_seg, stack
