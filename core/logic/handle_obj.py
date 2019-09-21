from core.logic.bu_check_obj_relationship import check_obj_relationship


def handle_obj(seg, ppos, i):
    obj_special_sit = 0
    # 这个特殊情况是为了 "腹腔obj" + "扫查exam"这种结构, 因为在exam处会讲腹腔和扫查拼到一起，所以这里obj就pass即可
    if i == 0:
        if i < len(seg) - 1:
            if seg[i + 1][2] == "exam":
                obj_special_sit = 2

    elif i != 0:
        # [] + obj + xxx
        if seg[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
            if len(ppos) > 0:
                if "symptom_obj" in [j[2] for j in ppos]:
                    # 先找到ppos中的obj
                    for k in ppos:
                        if k[2] == "symptom_obj":
                            other_obj = k[3]
                            break

                    # 查看2个obj关系
                    obj_rel = check_obj_relationship(self_obj=seg[i][3], other_obj=other_obj)
                    # 只有这种是特殊情况, 需要清空ppos
                    if obj_rel == 1:
                        obj_special_sit = 1

    if obj_special_sit == 1:
        ppos = list()

    ppos.append(seg[i])

    if obj_special_sit == 2:
        ppos.pop()

    return ppos
