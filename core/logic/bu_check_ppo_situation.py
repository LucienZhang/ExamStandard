# 该函数用来判断当前ppo属于哪种情况
def check_ppo_situation(ppo_list):
    """
    分情况时不分先后, 只看有哪些标签
    obj: 1
    obj + part: 2
    obj + pos: 3
    obj + pos + part: 4
    若ppos中没有obj: 5 (算为异常情况)
    :param ppo_list: 即 ppos
    :return: situation
    """

    pos = "symptom_pos"
    obj = "symptom_obj"
    part = "object_part"
    tmp = [j[2] for j in ppo_list]
    check_list = []

    for j in tmp:
        if j not in check_list:
            check_list.append(j)
        if j not in check_list:
            check_list.append(j)
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
    else:
        res = 5  # 没有obj的特殊情况

    return res
