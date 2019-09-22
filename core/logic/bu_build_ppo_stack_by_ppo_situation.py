from itertools import product
from core.utils import connect_tag_and_value
from core.logic.bu_check_obj_relationship import check_obj_relationship


def build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit):
    """
    该函数基于 check_ppo_situation 返回的结果, 分析具体情况
    sit: 在函数 check_ppo_situation 中返回的情况
    :param ppos: [[96, 97, 'symptom_obj', '中脑'], [105, 106, 'symptom_obj', '小脑']]
    :return: ppo_stack
    """

    # 只有obj
    # obj + obj + obj + [] (样本35)
    # obj + obj + obj + obj + [] (样本81) 中脑+桥脑+延髓+小脑
    if sit == 1:
        obj_rel = check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])
        if obj_rel == 1:
            ppo_stack = [connect_tag_and_value(j) for j in ppos]
        else:
            ppo_stack.append(connect_tag_and_value(ppos[0]) + connect_tag_and_value(ppos[1]))

    # obj + part
    elif sit == 2:
        # 开头是obj
        if ppos[0][2] == "symptom_obj":
            # 样本22 气管 + 1-3级 + 支气管
            if [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj"]:
                ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 样本38 胸廓o + 骨骼p + 胸壁o + 软组织p
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj", "object_part"]:
                tmp_1 = "".join([connect_tag_and_value(k) for k in ppos[:2]])
                tmp_2 = "".join([connect_tag_and_value(k) for k in ppos[2:]])
                ppo_stack.append(tmp_1)
                ppo_stack.append(tmp_2)

            elif [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "object_part"]:
                obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])

                # 样本100 颅骨内外板o + 板障o + 骨质p
                # part 和 每一个object 都拼
                if obj_rel == 1:
                    tmp_1 = [connect_tag_and_value(k) for k in ppos[:-1]]
                    tmp_2 = [connect_tag_and_value(ppos[-1])]

                    for tmp in list(product(*[tmp_1, tmp_2])):
                        ppo_stack.append("".join(tmp))

                # 样本24 室间隔o + 左室o + 后壁p
                elif obj_rel == 2:
                    ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 样本41 十二指肠o + 球部p + 降部p
            # obj + 多个part, 即ppos[0]是obj,  ppos[1:]都是part
            elif "symptom_obj" not in [j[2] for j in ppos[1:]]:
                tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                for tmp in tmp_list:
                    ppo_stack.append("".join([connect_tag_and_value(k) for k in tmp]))

        # 开头是part
        elif ppos[0][2] == "object_part":
            # 样本92 余p + 副鼻窦o + 窦壁p
            if [j[2] for j in ppos] == ["object_part", "symptom_obj", "object_part"]:
                ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 样本33 邻近p + 诸p + 骨o
            elif [j[2] for j in ppos] == ["object_part", "object_part", "symptom_obj"]:
                ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 样本79 余p + 脑池o + 脑室o
            elif [j[2] for j in ppos] == ["object_part", "symptom_obj", "symptom_obj"]:
                # 判断2个obj的关系
                obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                if obj_rel == 1:
                    # tmp_list = [(["part", "余"], ["obj","脑池"]), (["part", "余"], ["obj","脑室"])]
                    tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                    for tmp in tmp_list:
                        ppo_stack.append("".join([connect_tag_and_value(k) for k in tmp]))
                elif obj_rel == 2:
                    ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

    # obj + pos
    elif sit == 3:
        # 开头是 obj
        if ppos[0][2] == "symptom_obj":
            # 样本14 心o + 肝o + 双p + 肾o
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "symptom_pos", "symptom_obj"] or\
                    [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_obj"]:
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        if k == 0:
                            ppo_stack.append(connect_tag_and_value(ppos[k]))
                        else:
                            if ppos[k-1][2] == "symptom_pos":
                                ppo_stack.append("".join([connect_tag_and_value(ppos[k-1]),
                                                          connect_tag_and_value(ppos[k])]
                                                         ))
                            else:
                                ppo_stack.append(connect_tag_and_value(ppos[k]))

        # 开头是 pos
        elif ppos[0][2] == "symptom_pos":
            # 样本58 左p + 肱骨o + 中段p
            if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos"]:
                ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

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
                            tmp_1 = connect_tag_and_value(ppos[0]) + connect_tag_and_value(tmp_obj[0])
                            tmp_2 = connect_tag_and_value(tmp_obj[1]) + connect_tag_and_value(ppos[k])
                            ppo_stack.append(tmp_1)
                            ppo_stack.append(tmp_2)

                        # (pos + obj + obj + pos) 暂未遇到
                        elif obj_rel == 2:
                            ppo_stack.append("".join([connect_tag_and_value(m) for m in ppos]))

            # 样本 87 双侧pos + 上颌窦obj + 双侧pos + 额窦obj + 蝶窦obj + 双侧pos + 筛窦内obj
            elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos", "symptom_obj",
                                          "symptom_obj", "symptom_pos", "symptom_obj"]:

                tmp_pos = None
                lucky_obj = None

                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_pos":
                        tmp_pos = connect_tag_and_value(ppos[k])
                    elif ppos[k][2] == "symptom_obj":
                        tmp = list()
                        tmp.append(connect_tag_and_value(ppos[k]))

                        if ppos[k-1][2] == "symptom_pos":
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
                    ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

                # 若有多个obj, 则需要判断obj之间关系
                elif len(ppos[1:]) > 1:
                    obj_rel = check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                    if obj_rel == 1:
                        tmp_list = list(product(*[[ppos[0]], ppos[1:]]))

                        for tmp in tmp_list:
                            ppo_stack.append("".join([connect_tag_and_value(k) for k in tmp]))
                    elif obj_rel == 2:
                        tmp_2 = "".join([connect_tag_and_value(k) for k in ppos[1:]])
                        ppo_stack.append(connect_tag_and_value(ppos[0]) + tmp_2)

    # obj + pos + part
    elif sit == 4:
        # 开头是 obj
        if ppos[0][2] == "symptom_obj":
            # 样本11 鼻咽顶o + 后部pos + 软组织part
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "object_part"]:
                ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 该情况有2个样本45, 91, 需要2种不同拼法
            # 样本45 盲肠o + 下方pos + 周围pos + 腹膜part 建议先拼成"盲肠+下方+周围+腹膜"
            # 样本91 (鼻咽腔o + 顶部pos) + (后上壁pos + 软组织part)
            elif [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_pos", "object_part"]:
                for k in ppos:
                    if k[2] == "symptom_obj":
                        if k[3] == "鼻咽腔":
                            tmp_1 = list(product(*[ppos[1:3], [ppos[-1]]]))
                            tmp_2 = []
                            for tmp in tmp_1:
                                tmp_2.append("".join([connect_tag_and_value(k) for k in tmp]))

                            tmp_3 = [connect_tag_and_value(ppos[0])]
                            tmp_final = list(product(*[tmp_3, tmp_2]))

                            for tmp in tmp_final:
                                ppo_stack.append("".join([k for k in tmp]))

                        elif k[3] == "盲肠":
                            ppo_stack.append("".join([connect_tag_and_value(k) for k in ppos]))

            # 2种情况 样本15种两个part之间没有"和"或者"及"连接; 样本85两个part之间有"及"连接
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_pos", "object_part"]:
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        # 15 原文 "枕骨隆突周围软组织局限性瘤性突起。" (没有"和、及"连接词)
                        if ppos[k][3] == "枕骨":
                            ppo_stack.append("".join([connect_tag_and_value(m) for m in ppos]))

                        # 86 原文 "关节囊及周围软组织无明显肿胀及异常密度影。" (有"及"连接词)
                        # 85 原文 "椎体(o)骨质(part)未见骨质增生或破坏，双侧(pos)骶孔(part)对称." (有逗号"，"分隔)
                        else:
                            tmp_part_list = []
                            for m in range(k+1, len(ppos)):
                                if ppos[m][2] == "object_part":
                                    if m > 0:
                                        if ppos[m-1][2] == "symptom_pos":
                                            tmp_1 = "".join([connect_tag_and_value(n) for n in ppos[m-1:m+1]])
                                            tmp_part_list.append(tmp_1)
                                        else:
                                            tmp_part_list.append(connect_tag_and_value(ppos[m]))

                            tmp_2 = [connect_tag_and_value(ppos[k])]
                            tmp_final = list(product(*[tmp_2, tmp_part_list]))
                            for tmp in tmp_final:
                                ppo_stack.append("".join(tmp))

            # 样本31, 有连接词"及". 原文 "关节囊及关节周围软组织未见异常。"
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj", "symptom_pos", "object_part"]:
                # step1 以每个obj为中心, 先拼好放在tmp_total中
                tmp_total = []
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        tmp_1 = list()
                        tmp_1.append(ppos[k])

                        if ppos[k + 1][2] == "symptom_pos":
                            if k < len(ppos) - 2:
                                # obj + (pos + part)
                                if ppos[k + 2][2] == "object_part":
                                    tmp_1.append(ppos[k + 1])
                                    tmp_1.append(ppos[k + 2])
                        elif ppos[k + 1][2] == "object_part":
                            tmp_1.append(ppos[k + 1])

                        tmp_total.append(tmp_1)

                # step2 将拼好的结果放入 ppo_stack
                for tmp in tmp_total:
                    ppo_stack.append("".join([connect_tag_and_value(m) for m in tmp]))

        # 开头是 pos
        elif ppos[0][2] == "symptom_pos":
            # pos + obj + xxx
            if ppos[1][2] == "symptom_obj":
                if "symptom_obj" not in [j[2] for j in ppos[2:]]:
                    # pos + obj + part + part + ...
                    # 样本18 双pos + 肾o + [] + 包膜part + []
                    # 样本46 双pos + 肾o + 实质part + 集合系统part + []
                    if "symptom_pos" not in [j[2] for j in ppos[2:]]:
                        # tmp_1 是 (pos+obj), tmp_2 是 每一个part
                        tmp_1 = ["".join([connect_tag_and_value(k) for k in ppos[:2]])]
                        tmp_2 = [connect_tag_and_value(k) for k in ppos[2:]]

                        # 将 (pos+obj) 和 part 拼接, 放入 ppo_stack
                        for m in list(product(*[tmp_1, tmp_2])):
                            ppo_stack.append("".join(m))

                    # 样本2 左侧pos + 臀大肌obj + 外侧缘pos + 皮下脂肪part
                    elif "symptom_pos" in [j[2] for j in ppos[2:]]:
                        # tmp_1 是 (pos+obj), tmp_2 是 每一个part
                        tmp_1 = ["".join([connect_tag_and_value(k) for k in ppos[:2]])]

                        # 需要判断part前是否有pos，若有，则拼一起pos+part
                        tmp_2 = []
                        tmp_pos = None
                        for k in range(2, len(ppos)):
                            if ppos[k][2] == "symptom_pos":
                                tmp_pos = connect_tag_and_value(ppos[k])
                            elif ppos[k][2] == "object_part":
                                # 左侧 + 臀大肌 + 外侧缘 + 皮下脂肪
                                # 左侧 + 臀大肌 + 外侧缘 + 间隙内
                                if tmp_pos is not None:
                                    tmp_2.append(tmp_pos + connect_tag_and_value(ppos[k]))
                                # 左侧+ 臀大肌 + 皮肤
                                else:
                                    tmp_2.append(connect_tag_and_value(ppos[k]))

                        # 将 (pos+obj) 和 part 拼接, 放入 ppo_stack
                        for m in list(product(*[tmp_1, tmp_2])):
                            ppo_stack.append("".join(m))

                # pos + obj + obj + xxx
                elif "symptom_obj" in [j[2] for j in ppos[2:]]:
                    if "symptom_pos" not in [j[2] for j in ppos[2:]]:
                        # 样本75 双pos + 肾区obj + 输尿管obj + 走形区part + 膀胱区obj
                        # 情况A obj输尿管 不和 双pos 拼一起
                        if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_obj",
                                                    "object_part", "symptom_obj"]:
                            for k in range(len(ppos)):
                                if ppos[k][2] == "symptom_obj":
                                    tmp = list()
                                    tmp.append(connect_tag_and_value(ppos[k]))

                                    if ppos[k-1][2] == "symptom_pos":
                                        tmp.insert(0, connect_tag_and_value(ppos[k-1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(connect_tag_and_value(ppos[k + 1]))

                                    elif ppos[k - 1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(connect_tag_and_value(ppos[k + 1]))

                                    ppo_stack.append("".join(tmp))

                        # pos + obj + obj + obj + part + part
                        # 样本11 双侧pos + (上颌窦obj + 筛窦obj + 蝶窦obj) + 黏膜part
                        # 样本28 双侧pos + (筛窦obj + 蝶窦obj + 上颌窦obj) + (窦壁part + 黏膜part)
                        # 情况B 筛窦obj 要和 双侧pos 拼一起
                        else:
                            tmp_pos, tmp_obj, tmp_part = [], [], []
                            pos_obj = list()

                            tmp_pos.append(connect_tag_and_value(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(connect_tag_and_value(ppos[k]))

                                    if k < len(ppos) - 1:
                                        if ppos[k + 1][2] != "symptom_obj":
                                            # 先查看obj之间关系 1并列 2从属
                                            # 先来的是other_obj, 最后来的是self_obj
                                            obj_rel = check_obj_relationship(self_obj=ppos[k][3],
                                                                              other_obj=ppos[1][3])

                                            if obj_rel == 1:
                                                tmp_pos_obj = list(product(*[tmp_pos, tmp_obj]))
                                            elif obj_rel == 2:
                                                tmp_pos_obj = list(product(*[tmp_pos, ["".join(n for n in tmp_obj)]]))

                                            # 再将pos和obj拼接
                                            for tmp in tmp_pos_obj:
                                                pos_obj.append("".join([m for m in tmp]))

                                # step 2 找出所有part放入 tmp_part, 并和pos_obj拼接，最后结果放入pos_obj_part
                                elif ppos[k][2] == "object_part":
                                    tmp_part.append(connect_tag_and_value(ppos[k]))

                                    if k == len(ppos) - 1:
                                        tmp_pos_obj_part = list(product(*[pos_obj, tmp_part]))
                                        for tmp in tmp_pos_obj_part:
                                            ppo_stack.append("".join([m for m in tmp]))

                    elif "symptom_pos" in [j[2] for j in ppos[2:]]:
                        # pos + obj + obj + pos + part
                        # 样本63 双侧pos + 股骨obj + 腓胫骨obj + 周围pos + 软组织part
                        if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_obj",
                                                    "symptom_pos", "object_part"]:

                            tmp_pos, tmp_obj, tmp_part = [], [], []
                            pos_obj = list()

                            tmp_pos.append(connect_tag_and_value(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(connect_tag_and_value(ppos[k]))

                                    if k < len(ppos) - 1:
                                        if ppos[k + 1][2] != "symptom_obj":
                                            # 先查看obj之间关系 1并列 2从属
                                            obj_rel = check_obj_relationship(self_obj=ppos[1][3],
                                                                              other_obj=ppos[k][3])
                                            if obj_rel == 1:
                                                tmp_pos_obj = list(product(*[tmp_pos, tmp_obj]))
                                            elif obj_rel == 2:
                                                tmp_pos_obj = list(product(*[tmp_pos, ["".join(n for n in tmp_obj)]]))

                                            # 再将pos和obj拼接
                                            for tmp in tmp_pos_obj:
                                                pos_obj.append("".join([m for m in tmp]))

                                # step 2 找出所有part放入 tmp_part, 并和pos_obj拼接，最后结果放入pos_obj_part
                                elif ppos[k][2] == "object_part":
                                    if ppos[k - 1][2] == "symptom_pos":
                                        tmp_part.append(connect_tag_and_value(ppos[k - 1]) +
                                                        connect_tag_and_value(ppos[k]))
                                    else:
                                        tmp_part.append(connect_tag_and_value(ppos[k]))

                                    if k == len(ppos) - 1:
                                        tmp_pos_obj_part = list(product(*[pos_obj, tmp_part]))
                                        for tmp in tmp_pos_obj_part:
                                            ppo_stack.append("".join([m for m in tmp]))

                        # 样本 39 双pos+肾区obj+双pos+输尿管obj+径路part+膀胱区obj
                        elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos",
                                                      "symptom_obj", "object_part", "symptom_obj"]:

                            for k in range(len(ppos)):
                                if ppos[k][2] == "symptom_obj":
                                    tmp = list()
                                    tmp.append(connect_tag_and_value(ppos[k]))

                                    if ppos[k-1][2] == "symptom_pos":
                                        tmp.insert(0, connect_tag_and_value(ppos[k-1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k+1][2] == "object_part":
                                                tmp.append(connect_tag_and_value(ppos[k+1]))

                                    elif ppos[k-1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k+1][2] == "object_part":
                                                tmp.append(connect_tag_and_value(ppos[k+1]))

                                    ppo_stack.append("".join(tmp))

                        # 样本77 双侧pos + 上颌窦obj + 筛窦obj + 双侧pos + 蝶窦内obj + 黏膜part
                        # 该样本特殊性在于, 最后的黏膜part， 要拼给所有的pos_obj组合
                        # 双侧+上颌窦+黏膜; 双侧+筛窦+黏膜; 双侧+蝶窦内+黏膜
                        else:
                            tmp_pos = None
                            lucky_obj = None
                            pos_obj = []
                            part = []

                            for k in range(len(ppos)):
                                # step 1 将 pos+obj拼好
                                if ppos[k][2] == "symptom_pos":
                                    tmp_pos = connect_tag_and_value(ppos[k])
                                elif ppos[k][2] == "symptom_obj":
                                    tmp = list()
                                    tmp.append(connect_tag_and_value(ppos[k]))

                                    if k > 0:
                                        if ppos[k-1][2] == "symptom_pos":
                                            tmp.insert(0, connect_tag_and_value(ppos[k-1]))
                                            lucky_obj = ppos[k]

                                        else:
                                            if lucky_obj is not None:
                                                # 判断obj关系
                                                obj_rel = check_obj_relationship(self_obj=ppos[k][3],
                                                                                  other_obj=lucky_obj[3])
                                                if obj_rel == 1:
                                                    tmp.insert(0, tmp_pos)

                                                # 若是从属关系, 则后面的obj不拼前面的pos
                                                elif obj_rel == 2:
                                                    pass
                                    pos_obj.append("".join(tmp))

                                # step 2 将最后的 part 放入 part 列表
                                elif ppos[k][2] == "object_part":
                                    part.append(connect_tag_and_value(ppos[k]))

                                # step 3 将 pos_obj 和 part 做 itertools.product
                                for tmp in list(product(*[pos_obj, part])):
                                    ppo_stack.append("".join(tmp))

            # 样本 57 C2-3(pos) + C3-4(pos) + 椎体obj + []
            # ppos[1][2] 不是 obj, 而是pos
            else:
                tmp_pos = []
                tmp_obj = []

                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_pos":
                        tmp_pos.append(connect_tag_and_value(ppos[k]))
                    elif ppos[k][2] == "symptom_obj":
                        tmp_obj.append(connect_tag_and_value(ppos[k]))

                for tmp in list(product(*[tmp_pos, tmp_obj])):
                    ppo_stack.append("".join(tmp))

        # 开头是 part
        elif ppos[0][2] == "object_part":
            # 样本48 余part + 双侧pos + 大脑半球obj + [] + 灰白质part + []
            if [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj"] or\
                    [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj", "object_part"]:
                ppo_stack.append("".join([connect_tag_and_value(m) for m in ppos]))

    elif sit == 5:
        print("异常情况,当前ppos:")
        for ppo in ppos:
            print(ppo)

    return ppo_stack
