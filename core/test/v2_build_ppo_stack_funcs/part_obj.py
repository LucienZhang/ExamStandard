from itertools import product
from core.test.test_v2 import _connect, _check_obj_relationship


def build_ppo_stack_by_part_obj(ppos, ppo_stack):
    # 开头是obj
    if ppos[0][2] == "symptom_obj":
        # 样本22 气管 + 1-3级 + 支气管
        if [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj"]:
            ppo_stack.append("".join([_connect(k) for k in ppos]))

        # 样本38 胸廓o + 骨骼p + 胸壁o + 软组织p
        elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj", "object_part"]:
            tmp_1 = "".join([_connect(k) for k in ppos[:2]])
            tmp_2 = "".join([_connect(k) for k in ppos[2:]])
            ppo_stack.append(tmp_1)
            ppo_stack.append(tmp_2)

        elif [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "object_part"]:
            obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])

            # 样本100 颅骨内外板o + 板障o + 骨质p
            # part 和 每一个object 都拼
            if obj_rel == 1:
                tmp_1 = [_connect(k) for k in ppos[:-1]]
                tmp_2 = [_connect(ppos[-1])]

                for tmp in list(product(*[tmp_1, tmp_2])):
                    ppo_stack.append("".join(tmp))

            # 样本24 室间隔o + 左室o + 后壁p
            elif obj_rel == 2:
                ppo_stack.append("".join([_connect(k) for k in ppos]))

        # 样本41 十二指肠o + 球部p + 降部p
        # obj + 多个part, 即ppos[0]是obj,  ppos[1:]都是part
        elif "symptom_obj" not in [j[2] for j in ppos[1:]]:
            tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
            for tmp in tmp_list:
                ppo_stack.append("".join([_connect(k) for k in tmp]))

    # 开头是part
    elif ppos[0][2] == "object_part":
        # 样本92 余p + 副鼻窦o + 窦壁p
        if [j[2] for j in ppos] == ["object_part", "symptom_obj", "object_part"]:
            ppo_stack.append("".join([_connect(k) for k in ppos]))

        # 样本33 邻近p + 诸p + 骨o
        elif [j[2] for j in ppos] == ["object_part", "object_part", "symptom_obj"]:
            ppo_stack.append("".join([_connect(k) for k in ppos]))

        # 样本79 余p + 脑池o + 脑室o
        elif [j[2] for j in ppos] == ["object_part", "symptom_obj", "symptom_obj"]:
            # 判断2个obj的关系
            obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

            if obj_rel == 1:
                # tmp_list = [(["part", "余"], ["obj","脑池"]), (["part", "余"], ["obj","脑室"])]
                tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                for tmp in tmp_list:
                    ppo_stack.append("".join([_connect(k) for k in tmp]))
            elif obj_rel == 2:
                ppo_stack.append("".join([_connect(k) for k in ppos]))

    return ppo_stack
