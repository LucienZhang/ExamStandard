# 该函数用来判断当前ppo属于哪种情况
def check_ppo_situation(ppos):
    """
    分情况时不分先后, 只看有哪些标签
    obj: 1
    obj + part: 2
    obj + pos: 3
    obj + pos + part: 4
    :param: ppos
    :return: situation
    """

    pos = "symptom_pos"
    obj = "symptom_obj"
    part = "object_part"
    tmp = [j[2] for j in ppos]
    check_list = []

    for j in tmp:
        if j not in check_list:
            check_list.append(j)

    res = None
    if obj in check_list:
        if pos not in check_list:
            if part not in check_list:
                res = 1  # obj
            else:
                res = 2  # obj + part
        elif pos in check_list:
            if part not in check_list:
                res = 3  # obj + pos
            else:
                res = 4  # obj + pos + part

    return res
