from itertools import product
from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.utils import connect


def build_ppo_stack_by_pos_obj(ppos, ppo_stack):
    # 开头是 obj
    if ppos[0][2] == "symptom_obj":
        # 样本14 心o + 肝o + 双p + 肾o
        if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "symptom_pos", "symptom_obj"] or \
                [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_obj"]:
            for k in range(len(ppos)):
                if ppos[k][2] == "symptom_obj":
                    if k == 0:
                        ppo_stack.append(connect(ppos[k]))
                    else:
                        if ppos[k - 1][2] == "symptom_pos":
                            ppo_stack.append("".join([connect(ppos[k - 1]),
                                                      connect(ppos[k])]
                                                     ))
                        else:
                            ppo_stack.append(connect(ppos[k]))

    # 开头是 pos
    elif ppos[0][2] == "symptom_pos":
        # 样本58 左p + 肱骨o + 中段p
        if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos"]:
            ppo_stack.append("".join([connect(k) for k in ppos]))

        # 样本45 双侧p + 肾盂o + 输尿管o + 上段p （注意,肾盂和输尿管在医学中是并列关系，不是从属关系）
        elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_obj", "symptom_pos"]:
            tmp_obj = []
            for k in range(1, len(ppos)):
                if ppos[k][2] == "symptom_obj":
                    tmp_obj.append(ppos[k])
                elif ppos[k][2] == "symptom_pos":
                    # 判断tmp_obj中obj的关系
                    obj_rel = check_obj_relationship(self_obj=tmp_obj[0][3], other_obj=tmp_obj[1][3])

                    # (pos+obj) + (obj+pos)
                    if obj_rel == 1:
                        tmp_1 = connect(ppos[0]) + connect(tmp_obj[0])
                        tmp_2 = connect(tmp_obj[1]) + connect(ppos[k])
                        ppo_stack.append(tmp_1)
                        ppo_stack.append(tmp_2)

                    # (pos + obj + obj + pos) 暂未遇到
                    elif obj_rel == 2:
                        ppo_stack.append("".join([connect(m) for m in ppos]))

        # 样本 87 双侧pos + 上颌窦obj + 双侧pos + 额窦obj + 蝶窦obj + 双侧pos + 筛窦内obj
        elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos", "symptom_obj",
                                      "symptom_obj", "symptom_pos", "symptom_obj"]:

            tmp_pos = None
            lucky_obj = None

            for k in range(len(ppos)):
                if ppos[k][2] == "symptom_pos":
                    tmp_pos = connect(ppos[k])
                elif ppos[k][2] == "symptom_obj":
                    tmp = list()
                    tmp.append(connect(ppos[k]))

                    if ppos[k - 1][2] == "symptom_pos":
                        lucky_obj = ppos[k]
                        tmp.insert(0, tmp_pos)
                    else:
                        if lucky_obj is not None:
                            obj_rel = check_obj_relationship(self_obj=ppos[k][3], other_obj=lucky_obj[3])

                            if obj_rel == 1:
                                tmp.insert(0, tmp_pos)

                    ppo_stack.append("".join(tmp))

        # 样本2 双侧p + 额o + 颞o + 顶枕叶o + 脑沟内o
        elif "symptom_pos" not in [j[2] for j in ppos[1:]]:
            if len(ppos[1:]) == 1:
                ppo_stack.append("".join([connect(k) for k in ppos]))

            # 若有多个obj, 则需要判断obj之间关系
            elif len(ppos[1:]) > 1:
                obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                if obj_rel == 1:
                    tmp_list = list(product(*[[ppos[0]], ppos[1:]]))

                    for tmp in tmp_list:
                        ppo_stack.append("".join([connect(k) for k in tmp]))
                elif obj_rel == 2:
                    tmp_2 = "".join([connect(k) for k in ppos[1:]])
                    ppo_stack.append(connect(ppos[0]) + tmp_2)

    return ppo_stack
