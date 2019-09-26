from itertools import product
from core.logic.build_ppo_stack_funcs.obj import check_obj_rel_for_many_objs
# from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.utils import connect


def build_ppo_stack_by_part_obj(ppos, ppo_stack, text):
    """
    :param ppos: [[127, 129, 'symptom_obj', '室间隔'], [131, 132, 'symptom_obj', '左室'], [133, 134, 'object_part', '后壁']]

    流程
    1. ppos[0] 是 obj还是part
        1.1 obj --> 4种情况:
            1.1.a obj+part+obj
            1.1.b obj+part+obj+part
            1.1.c obj+...(n个)obj + part(最后一个)
            1.1.d obj(首个) + part + ...(n个)part

        1.2 part --> 3种情况:
            1.2.a part + obj + part
            1.2.b part + part + obj (特殊, 邻近+诸+骨)
            1.2.c part(首个) + n个obj

    :return: ppo_stack
    """

    # 开头是obj
    if ppos[0][2] == "symptom_obj":
        # 样本22 气管 + 1-3级 + 支气管
        if [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj"]:

            ppo_stack.append(connect(ppos[0]))
            ppo_stack.append("".join([connect(k) for k in ppos[1:]]))

        # 样本38 胸廓o + 骨骼p + 胸壁o + 软组织p
        elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj", "object_part"]:
            tmp_1 = "".join([connect(k) for k in ppos[:2]])
            tmp_2 = "".join([connect(k) for k in ppos[2:]])
            ppo_stack.append(tmp_1)
            ppo_stack.append(tmp_2)

        # 多(obj)对一(part)
        # 肝、肾、心脏表皮
        elif "object_part" not in [j[2] for j in ppos[:-1]]:
            # 判断obj关系
            # 因为ppos[1:]中一共有多少个obj, 是不确定的，可能比2个多，所以调用 check_obj_rel_for_many_objs
            raw_obj_list = check_obj_rel_for_many_objs(sub_obj_list=ppos[:-1], text=text)

            connected_obj_list = []
            for raw_obj_one in raw_obj_list:
                connected_obj_list.append("".join([connect(tmp) for tmp in raw_obj_one]))

            for tmp in list(product(*[connected_obj_list, [connect(ppos[-1])]])):
                ppo_stack.append("".join(tmp))

        # 样本41 十二指肠o + 球部p + 降部p
        # obj + 多个part, 即ppos[0]是obj,  ppos[1:]都是part
        elif "symptom_obj" not in [j[2] for j in ppos[1:]]:
            tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
            for tmp in tmp_list:
                ppo_stack.append("".join([connect(k) for k in tmp]))

    # 开头是part
    elif ppos[0][2] == "object_part":
        # 样本92 余p + 副鼻窦o + 窦壁p
        if [j[2] for j in ppos] == ["object_part", "symptom_obj", "object_part"]:
            ppo_stack.append("".join([connect(k) for k in ppos]))

        # 样本33 邻近p + 诸p + 骨o
        elif [j[2] for j in ppos] == ["object_part", "object_part", "symptom_obj"]:
            ppo_stack.append("".join([connect(k) for k in ppos]))

        # 样本79 余p + 脑池o + 脑室o
        # 1 part 对 多个 obj
        elif "object_part" not in [j[2] for j in ppos[1:]]:
            # 试用 v2 判断关系 (2019_09_26 下午5:00 修改)
            # 因为ppos[1:]中一共有多少个obj, 是不确定的，可能比2个多，所以调用 check_obj_rel_for_many_objs
            raw_obj_list = check_obj_rel_for_many_objs(sub_obj_list=ppos[1:], text=text)

            connected_obj_list = []
            for raw_obj_one in raw_obj_list:
                connected_obj_list.append("".join([connect(tmp) for tmp in raw_obj_one]))

            connected_part_one = [connect(ppos[0])]

            for tmp in list(product(*[connected_part_one, connected_obj_list])):
                ppo_stack.append("".join(tmp))

    return ppo_stack
