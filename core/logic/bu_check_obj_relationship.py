from data.obj_rel_map import obj_rel_map


def check_obj_relationship(self_obj, other_obj, object_relation_map=obj_rel_map):
    """
    该函数用来判断2个obj之间关系
    :param self_obj: 自己 = "心脏"
    :param other_obj: 其他 = "肝脏"
    :param object_relation_map: obj之间的关系表
    :return: 1并列, 2从属
    """

    # 默认设置大部分是并列, 如 "肾" 与 "肝脏"
    rel = 1

    for obj in object_relation_map:
        if obj["name"] == self_obj:
            # "气管" 与 "纵隔"
            if other_obj in obj["rel"]["1"]:
                rel = 1

            # "气管" 与 "支气管"
            elif other_obj in obj["rel"]["2"]:
                rel = 2

    return rel
