from itertools import product
import sys
from utils import split_target
from data.obj_rel_map import obj_rel_map
from data.v5_test_data import samples


# 该函数用来构造 itertools.product 所需的参数 (注: 参数中不可存在空列表)
# 正确参数举例: [["$obj&肾", "%obj&肝脏"], ["$item&大小$exam_result&正常"]]
# 错误参数举例: [["$obj&肾", "%obj&肝脏"], [], [], ["$item&大小$exam_result&正常"]]
def _build_product_param(*stacks):
    product_param = []
    for stackOne in stacks:
        if len(stackOne) > 0:
            product_param.append(stackOne)
    return product_param


# 输入: [53, 55, 'symptom_obj', '副鼻窦']
# 输出: "$symptom_obj&副鼻窦"
def _connect_tag_and_value(t):
    return "$" + t[2] + "&" + t[3]


# 该函数用来判断2个obj之间关系
def _check_obj_relationship(self_obj, other_obj, object_relation_map=obj_rel_map):
    """
    :param self_obj: 自己 = "心脏"
    :param other_obj: 其他 = "肝脏"
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


# 该函数用来判断当前ppo属于哪种情况
def _check_ppo_situation(ppo_list):
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

    if obj in check_list:
        if pos not in check_list:
            if part not in check_list:
                return 1  # obj
            else:
                return 2  # obj + part
        elif pos in check_list:
            if part not in check_list:
                return 3  # obj + pos
            else:
                return 4  # obj + pos + part
    else:
        return 5  # 没有obj的特殊情况


def _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit):
    """
    具体情况
    sit: 在函数 _check_ppo_situation 中返回的情况
    :param ppos: [[96, 97, 'symptom_obj', '中脑'], [105, 106, 'symptom_obj', '小脑']]
    :return:
    """

    # 只有obj
    # obj + obj + obj + [] (样本35)
    # obj + obj + obj + obj + [] (样本81) 中脑+桥脑+延髓+小脑
    if sit == 1:
        obj_rel = _check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])
        if obj_rel == 1:
            ppo_stack = [_connect_tag_and_value(j) for j in ppos]
        else:
            ppo_stack.append(_connect_tag_and_value(ppos[0]) + _connect_tag_and_value(ppos[1]))

    # obj + part
    elif sit == 2:
        # 开头是obj
        if ppos[0][2] == "symptom_obj":
            # 样本22 气管 + 1-3级 + 支气管
            if [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj"]:
                ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 样本38 胸廓o + 骨骼p + 胸壁o + 软组织p
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_obj", "object_part"]:
                tmp_1 = "".join([_connect_tag_and_value(k) for k in ppos[:2]])
                tmp_2 = "".join([_connect_tag_and_value(k) for k in ppos[2:]])
                ppo_stack.append(tmp_1)
                ppo_stack.append(tmp_2)

            # 样本24 室间隔o + 左室o + 后壁p
            elif [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "object_part"]:
                obj_rel = _check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])

                if obj_rel == 1:
                    pass
                    # ppo_stack.append(_connect_tag_and_value(ppos[0]))
                    # ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos[1:]]))
                elif obj_rel == 2:
                    ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 样本41 十二指肠o + 球部p + 降部p
            # obj + 多个part, 即ppos[0]是obj,  ppos[1:]都是part
            elif "symptom_obj" not in [j[2] for j in ppos[1:]]:
                tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                for tmp in tmp_list:
                    ppo_stack.append("".join([_connect_tag_and_value(k) for k in tmp]))

        # 开头是part
        elif ppos[0][2] == "object_part":
            # 样本92 余p + 副鼻窦o + 窦壁p
            if [j[2] for j in ppos] == ["object_part", "symptom_obj", "object_part"]:
                ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 样本33 邻近p + 诸p + 骨o
            elif [j[2] for j in ppos] == ["object_part", "object_part", "symptom_obj"]:
                ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 样本79 余p + 脑池o + 脑室o
            elif [j[2] for j in ppos] == ["object_part", "symptom_obj", "symptom_obj"]:
                # 判断2个obj的关系
                obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                if obj_rel == 1:
                    # tmp_list = [(["part", "余"], ["obj","脑池"]), (["part", "余"], ["obj","脑室"])]
                    tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                    for tmp in tmp_list:
                        ppo_stack.append("".join([_connect_tag_and_value(k) for k in tmp]))
                elif obj_rel == 2:
                    ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

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
                            ppo_stack.append(_connect_tag_and_value(ppos[k]))
                        else:
                            if ppos[k-1][2] == "symptom_pos":
                                ppo_stack.append("".join([_connect_tag_and_value(ppos[k-1]),
                                                          _connect_tag_and_value(ppos[k])]
                                                         ))
                            else:
                                ppo_stack.append(_connect_tag_and_value(ppos[k]))

        # 开头是 pos
        elif ppos[0][2] == "symptom_pos":
            # 样本58 左p + 肱骨o + 中段p
            if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos"]:
                ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 样本45 双侧p + 肾盂o + 输尿管o + 上段p （注意,肾盂和输尿管在医学中是并列关系，不是从属关系）
            elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_obj", "symptom_pos"]:
                tmp_obj = []
                for k in range(1, len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        tmp_obj.append(ppos[k])
                    elif ppos[k][2] == "symptom_pos":
                        # 判断tmp_obj中obj的关系
                        obj_rel = _check_obj_relationship(self_obj=tmp_obj[0][3], other_obj=tmp_obj[1][3])

                        # (pos+obj) + (obj+pos)
                        if obj_rel == 1:
                            tmp_1 = _connect_tag_and_value(ppos[0]) + _connect_tag_and_value(tmp_obj[0])
                            tmp_2 = _connect_tag_and_value(tmp_obj[1]) + _connect_tag_and_value(ppos[k])
                            ppo_stack.append(tmp_1)
                            ppo_stack.append(tmp_2)

                        # (pos + obj + obj + pos) 暂未遇到
                        elif obj_rel == 2:
                            ppo_stack.append("".join([_connect_tag_and_value(m) for m in ppos]))

            # 样本 87 双侧pos + 上颌窦obj + 双侧pos + 额窦obj + 蝶窦obj + 双侧pos + 筛窦内obj
            elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos", "symptom_obj",
                                          "symptom_obj", "symptom_pos", "symptom_obj"]:

                tmp_pos = None
                lucky_obj = None

                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_pos":
                        tmp_pos = _connect_tag_and_value(ppos[k])
                    elif ppos[k][2] == "symptom_obj":
                        tmp = list()
                        tmp.append(_connect_tag_and_value(ppos[k]))

                        if ppos[k-1][2] == "symptom_pos":
                            lucky_obj = ppos[k]
                            print(tmp_pos)
                            tmp.insert(0, tmp_pos)
                        else:
                            if lucky_obj is not None:
                                obj_rel = _check_obj_relationship(self_obj=ppos[k][3], other_obj=lucky_obj[3])

                                if obj_rel == 1:
                                    tmp.insert(0, tmp_pos)

                        ppo_stack.append("".join(tmp))

            # 样本2 双侧p + 额o + 颞o + 顶枕叶o + 脑沟内o
            elif "symptom_pos" not in [j[2] for j in ppos[1:]]:
                if len(ppos[1:]) == 1:
                    ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

                # 若有多个obj, 则需要判断obj之间关系
                elif len(ppos[1:]) > 1:
                    obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                    if obj_rel == 1:
                        tmp_list = list(product(*[[ppos[0]], ppos[1:]]))

                        for tmp in tmp_list:
                            ppo_stack.append("".join([_connect_tag_and_value(k) for k in tmp]))
                    elif obj_rel == 2:
                        tmp_2 = "".join([_connect_tag_and_value(k) for k in ppos[1:]])
                        ppo_stack.append(_connect_tag_and_value(ppos[0]) + tmp_2)

    # obj + pos + part
    elif sit == 4:
        # 开头是 obj
        if ppos[0][2] == "symptom_obj":
            # 样本11 鼻咽顶o + 后部pos + 软组织part
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "object_part"]:
                ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 该情况有2个样本45, 91, 需要2种不同拼法
            # 造成该问题的原因，可能是45的2个pos分的没有太大必要，可以吧"下方周围"标为一个pos
            # 还有一个因素,45的2个pos之间没有顿号，或者"和"，"及"等提示性连接词;
            # 但是91样本的2个pos之间有一个关键词"及"
            # 样本45 盲肠o + 下方pos + 周围pos + 腹膜part 建议先拼成"盲肠+下方+周围+腹膜"
            # 样本91 鼻咽腔o + 顶部pos + 后上壁pos + 软组织part
            # 若要系统分辨，可能后续标注时, 需要将这种"和"，"及"等关键词都标出
            elif [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_pos", "object_part"]:
                for k in ppos:
                    if k[2] == "symptom_obj":
                        if k[3] == "鼻咽腔":
                            tmp_1 = list(product(*[ppos[1:3], [ppos[-1]]]))
                            tmp_2 = []
                            for tmp in tmp_1:
                                tmp_2.append("".join([_connect_tag_and_value(k) for k in tmp]))

                            tmp_3 = [_connect_tag_and_value(ppos[0])]
                            tmp_final = list(product(*[tmp_3, tmp_2]))

                            for tmp in tmp_final:
                                ppo_stack.append("".join([k for k in tmp]))

                        elif k[3] == "盲肠":
                            ppo_stack.append("".join([_connect_tag_and_value(k) for k in ppos]))

            # 2种情况 样本15种两个part之间没有"和"或者"及"连接; 样本85两个part之间有"及"连接
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_pos", "object_part"]:
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        # 15 原文 "枕骨隆突周围软组织局限性瘤性突起。" (没有"和、及"连接词)
                        if ppos[k][3] == "枕骨":
                            ppo_stack.append("".join([_connect_tag_and_value(m) for m in ppos]))

                        # 86 原文 "关节囊及周围软组织无明显肿胀及异常密度影。" (有"及"连接词)
                        # 85 原文 "椎体(o)骨质(part)未见骨质增生或破坏，双侧(pos)骶孔(part)对称." (有逗号"，"分隔)
                        else:
                            tmp_part_list = []
                            for m in range(k+1, len(ppos)):
                                if ppos[m][2] == "object_part":
                                    if m > 0:
                                        if ppos[m-1][2] == "symptom_pos":
                                            tmp_1 = "".join([_connect_tag_and_value(n) for n in ppos[m-1:m+1]])
                                            tmp_part_list.append(tmp_1)
                                        else:
                                            tmp_part_list.append(_connect_tag_and_value(ppos[m]))

                            tmp_2 = [_connect_tag_and_value(ppos[k])]
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
                    ppo_stack.append("".join([_connect_tag_and_value(m) for m in tmp]))

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
                        tmp_1 = ["".join([_connect_tag_and_value(k) for k in ppos[:2]])]
                        tmp_2 = [_connect_tag_and_value(k) for k in ppos[2:]]

                        # 将 (pos+obj) 和 part 拼接, 放入 ppo_stack
                        for m in list(product(*[tmp_1, tmp_2])):
                            ppo_stack.append("".join(m))

                    # 样本2 左侧pos + 臀大肌obj + 外侧缘pos + 皮下脂肪part
                    elif "symptom_pos" in [j[2] for j in ppos[2:]]:
                        # tmp_1 是 (pos+obj), tmp_2 是 每一个part
                        tmp_1 = ["".join([_connect_tag_and_value(k) for k in ppos[:2]])]

                        # 需要判断part前是否有pos，若有，则拼一起pos+part
                        tmp_2 = []
                        tmp_pos = None
                        for k in range(2, len(ppos)):
                            if ppos[k][2] == "symptom_pos":
                                tmp_pos = _connect_tag_and_value(ppos[k])
                            elif ppos[k][2] == "object_part":
                                # 左侧 + 臀大肌 + 外侧缘 + 皮下脂肪
                                # 左侧 + 臀大肌 + 外侧缘 + 间隙内
                                if tmp_pos is not None:
                                    tmp_2.append(tmp_pos + _connect_tag_and_value(ppos[k]))
                                # 左侧+ 臀大肌 + 皮肤
                                else:
                                    tmp_2.append(_connect_tag_and_value(ppos[k]))

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
                                    tmp.append(_connect_tag_and_value(ppos[k]))

                                    if ppos[k-1][2] == "symptom_pos":
                                        tmp.insert(0, _connect_tag_and_value(ppos[k-1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect_tag_and_value(ppos[k + 1]))

                                    elif ppos[k - 1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect_tag_and_value(ppos[k + 1]))

                                    ppo_stack.append("".join(tmp))

                        # pos + obj + obj + obj + part + part
                        # 样本11 双侧pos + (上颌窦obj + 筛窦obj + 蝶窦obj) + 黏膜part
                        # 样本28 双侧pos + (筛窦obj + 蝶窦obj + 上颌窦obj) + (窦壁part + 黏膜part)
                        # 情况B 筛窦obj 要和 双侧pos 拼一起
                        else:
                            tmp_pos, tmp_obj, tmp_part = [], [], []
                            pos_obj = list()

                            tmp_pos.append(_connect_tag_and_value(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(_connect_tag_and_value(ppos[k]))

                                    if k < len(ppos) - 1:
                                        if ppos[k + 1][2] != "symptom_obj":
                                            # 先查看obj之间关系 1并列 2从属
                                            obj_rel = _check_obj_relationship(self_obj=ppos[1][3],
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
                                    tmp_part.append(_connect_tag_and_value(ppos[k]))

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

                            tmp_pos.append(_connect_tag_and_value(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(_connect_tag_and_value(ppos[k]))

                                    if k < len(ppos) - 1:
                                        if ppos[k + 1][2] != "symptom_obj":
                                            # 先查看obj之间关系 1并列 2从属
                                            obj_rel = _check_obj_relationship(self_obj=ppos[1][3],
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
                                        tmp_part.append(_connect_tag_and_value(ppos[k - 1]) +
                                                        _connect_tag_and_value(ppos[k]))
                                    else:
                                        tmp_part.append(_connect_tag_and_value(ppos[k]))

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
                                    tmp.append(_connect_tag_and_value(ppos[k]))

                                    if ppos[k-1][2] == "symptom_pos":
                                        tmp.insert(0, _connect_tag_and_value(ppos[k-1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k+1][2] == "object_part":
                                                tmp.append(_connect_tag_and_value(ppos[k+1]))

                                    elif ppos[k-1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k+1][2] == "object_part":
                                                tmp.append(_connect_tag_and_value(ppos[k+1]))

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
                                    tmp_pos = _connect_tag_and_value(ppos[k])
                                elif ppos[k][2] == "symptom_obj":
                                    tmp = list()
                                    tmp.append(_connect_tag_and_value(ppos[k]))

                                    if k > 0:
                                        if ppos[k-1][2] == "symptom_pos":
                                            tmp.insert(0, _connect_tag_and_value(ppos[k-1]))
                                            lucky_obj = ppos[k]

                                        else:
                                            if lucky_obj is not None:
                                                # 判断obj关系
                                                obj_rel = _check_obj_relationship(self_obj=ppos[k][3],
                                                                                  other_obj=lucky_obj[3])
                                                if obj_rel == 1:
                                                    tmp.insert(0, tmp_pos)

                                                # 若是从属关系, 则后面的obj不拼前面的pos
                                                elif obj_rel == 2:
                                                    pass
                                    pos_obj.append("".join(tmp))

                                # step 2 将最后的 part 放入 part 列表
                                elif ppos[k][2] == "object_part":
                                    part.append(_connect_tag_and_value(ppos[k]))

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
                        tmp_pos.append(_connect_tag_and_value(ppos[k]))
                    elif ppos[k][2] == "symptom_obj":
                        tmp_obj.append(_connect_tag_and_value(ppos[k]))

                for tmp in list(product(*[tmp_pos, tmp_obj])):
                    ppo_stack.append("".join(tmp))

        # 开头是 part
        elif ppos[0][2] == "object_part":
            # 样本48 余part + 双侧pos + 大脑半球obj + [] + 灰白质part + []
            if [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj"] or\
                    [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj", "object_part"]:
                ppo_stack.append("".join([_connect_tag_and_value(m) for m in ppos]))

    elif sit == 5:
        print("异常情况,当前ppos:")
        for ppo in ppos:
            print(ppo)

    return ppo_stack


def _build_ppo_stack(ppos, ppo_stack):
    if len(ppos) == 1:
        ppo_stack.append(_connect_tag_and_value(ppos[0]))

    # 5种情况 o+o, o + part/pos, pos/part + o (肯定有o)
    elif len(ppos) == 2:
        # 只有o+o需要判断2者关系(并列/从属/没关系)
        if ppos[0][2] == "symptom_obj" and ppos[1][2] == "symptom_obj":
            obj_rel = _check_obj_relationship(ppos[0][3], ppos[1][3])
            if obj_rel == 1:
                ppo_stack = [_connect_tag_and_value(j) for j in ppos]
            else:
                ppo_stack.append(_connect_tag_and_value(ppos[0]) + _connect_tag_and_value(ppos[1]))
        else:
            ppo_stack.append(_connect_tag_and_value(ppos[0]) + _connect_tag_and_value(ppos[1]))

    elif len(ppos) > 2:
        # 获得sit
        sit = _check_ppo_situation(ppos)

        # 根据sit，排列出ppo_stack
        ppo_stack = _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit)

    return ppo_stack


# 主函数
def exam_standard(origin_targets):
    # 分割为多个segments
    segments = split_target(origin_targets)

    # 定义最终返回的响应
    output_list = []

    for x in segments:

        # 初始化变量

        # ppos解释: ppo是指 pos_part_obj的简写, s是指复数
        # ppos = [['$symptom_pos&双侧'], ['symptom_obj', '额']]
        ppos, ppo_stack = [], []

        # items存放遇到的 exam_item, ir是 exam_item_exam_result简写, 存放拼好的ir,比如"大小+正常"
        items, decorations = [], []
        results, reversed_ir = [], []
        ir, deco_desc = [], []

        # 用来其他标签
        treatment_stack, medical_events_stack = [], []
        exam_stack = []

        # entity_neg, 和 exam 不需要stack, 用一个变量存储其值即可
        entity_neg = None

        # res_x: 存储一个seg (seg也就是x) 内所有拼接好的结果
        res_x = []
        # 每个seg中处理结构化拼接
        for i in range(len(x)):
            tag = x[i][2]
            value = x[i][3]

            if tag == "symptom_pos":
                # pos + obj + xxx
                if i == 0:
                    ppos.append(x[i])
                else:
                    # obj + pos + obj
                    # obj + pos
                    # obj + pos + part等
                    if x[i - 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
                        ppos.append(x[i])

                    else:
                        # xxx + pos + obj + xxx
                        # xxx + pos + part + xxx 等等
                        if x[i + 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:

                            # xxx + pos + obj + xxx
                            # [192, 192, 'symptom_pos', '双'],
                            # [193, 194, 'symptom_obj', '肾内'],
                            # [195, 200, 'reversed_exam_result', '未见明显异常'],
                            # [201, 202, 'reversed_exam_item', '声像'],
                            # [204, 207, 'exam', 'CDFI'],
                            # [210, 210, 'symptom_pos', '双'],
                            # [211, 211, 'symptom_obj', '肾'],
                            # [212, 215, 'exam_item', '彩色血流'],
                            # [216, 219, 'exam_result', '分布正常'],
                            # [221, 222, 'exam', '频谱'],
                            # [223, 228, 'exam_result', '未见明显异常']
                            if x[i + 1][2] == "symptom_obj":
                                ppos = list()
                                ppos.append(x[i])

                            # xxx + pos + pos + xxx
                            # 暂时没有出现过
                            elif x[i + 1][2] == "symptom_pos":
                                pass

                            # sample_63
                            # [58, 59, 'symptom_pos', '双侧'],
                            # [60, 61, 'symptom_obj', '股骨'],
                            # [63, 65, 'symptom_obj', '胫腓骨'],
                            # [66, 67, 'object_part', '骨骺'],
                            # [68, 69, 'symptom_desc', '对称'],
                            # [71, 72, 'exam_item', '形态'],
                            # [73, 78, 'exam_result', '未见明显异常'],
                            # [80, 81, 'symptom_pos', '周围'],
                            # [82, 84, 'object_part', '软组织'],
                            # [85, 86, 'entity_neg', '未见'],
                            # [87, 88, 'symptom_deco', '明显'],
                            # [89, 90, 'symptom_desc', '异常']
                            elif x[i + 1][2] == "object_part":
                                if len(ppos) > 0:
                                    if ppos[-1][2] == "object_part":
                                        # sample_63: 骨垢 + xxx + 周围 + 软组织
                                        # 从ppos中将 "骨垢" 移除, 将 "周围" 放入
                                        ppos.pop()
                                        ppos.append(x[i])
                                    elif ppos[-1][2] == "symptom_pos":
                                        # 没有遇到
                                        pass
                                    elif ppos[-1][2] == "symptom_obj":
                                        # 样本3 左侧臀大肌 + [] + 外侧缘pos + part + xxx
                                        # 遇到外侧缘, 因为要和后面的part拼，所以不用担心ppos中的obj，不用清空ppos，直接放入
                                        ppos.append(x[i])

                        # xxx + pos + xxx
                        # sample_29
                        # [46, 47, 'symptom_obj', '纵隔'],
                        # [48, 49, 'exam_item', '结构'],
                        # [50, 52, 'exam_result', '无偏移'],
                        # [54, 54, 'symptom_pos', '内'],
                        # [55, 56, 'entity_neg', '未见'],
                        # [57, 58, 'symptom_deco', '明显'],
                        # [59, 63, 'symptom_desc', '肿大淋巴结']
                        elif x[i + 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                            if len(ppos) > 0:
                                if ppos[-1][2] == "symptom_obj":
                                    # sample_29: 纵隔 + xxx + 内
                                    # 将自己 "内" 放入ppos, ppos = ["纵隔", "内"]
                                    ppos.append(x[i])

                                # sample_36
                                # [13, 13, 'symptom_pos', '右'],
                                # [14, 14, 'symptom_obj', '叶'],
                                # [15, 16, 'exam_item', '体积'],
                                # [17, 18, 'exam_result', '增大'],
                                # [21, 21, 'symptom_pos', '内'],
                                # [22, 26, 'exam_item', '放射性分布'],
                                # [27, 29, 'exam_result', '不均匀'],
                                # [31, 33, 'symptom_pos', '中下部'],
                                # [36, 36, 'lesion_desc', '一'],
                                # [37, 41, 'lesion_desc', '放射性分布'],
                                # [42, 46, 'lesion', '稀疏缺损区']
                                elif ppos[-1][2] == "symptom_pos":
                                    # 将ppos[-1] "内"移除，再将自己"中下部"放入ppos
                                    # ppos = ["右", "叶", "中下部"]
                                    ppos.pop()
                                    ppos.append(x[i])

                                elif ppos[-1][2] == "object_part":
                                    # 没有遇到
                                    pass

            elif tag == "symptom_obj":
                special_sit = 0
                if i != 0:
                    # [] + obj + xxx
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        if len(ppos) > 0:
                            # 2019_09_17修改逻辑，当前是只看ppos数组尾巴项是否为obj
                            # 修改后, 只要ppos中有obj，就判断obj只看的关系
                            # 样本31 左pos + 髋关节obj + 各骨part + [] + 关节obj(自己) + part + []
                            # 遇到关节（自己）时，和ppos中的 髋关节比较关系

                            # if ppos[-1][2] == "symptom_obj":
                            if "symptom_obj" in [j[2] for j in ppos]:
                                # 查看2个obj关系
                                obj_rel = _check_obj_relationship(self_obj=value, other_obj=ppos[-1][3])

                                # 只有这种是特殊情况, 不清空ppos
                                if obj_rel == 1:
                                    special_sit = 1

                if special_sit == 1:
                    ppos = list()

                ppos.append(x[i])

            elif tag == "object_part":
                part_special_sit = 0
                # [ir] + part + xxx
                # [65, 66, 'symptom_pos', '左侧'],
                # [67, 69, 'symptom_obj', '臀大肌'],
                # [70, 72, 'symptom_deco', '较右侧'],
                # [73, 74, 'symptom_desc', '缩小'],
                # [76, 77, 'exam_item', '信号'],
                # [78, 79, 'exam_result', '不均'],
                # [81, 82, 'exam_item', '边缘'],
                # [83, 84, 'exam_result', '模糊'],
                # [87, 89, 'symptom_pos', '外侧缘'],
                # [90, 93, 'object_part', '皮下脂肪'],
                # [94, 96, 'object_part', '间隙内'],
                # [99, 101, 'lesion_desc', '片状长'],
                # [102, 111, 'lesion', 'T1长T2异常信号影'],
                # [113, 114, 'exam_item', '大小'],
                # [115, 128, 'exam_result', '约0.6×1.3×2.4cm'],
                # [130, 131, 'exam_item', '边界'],
                # [132, 133, 'exam_result', '清楚'],
                # [135, 136, 'symptom_deco', '局部'],
                # [137, 138, 'object_part', '皮肤'],
                # [139, 139, 'symptom_deco', '略'],
                # [140, 141, 'symptom_desc', '凹陷']
                if i != 0:
                    # 以上样本 中的 "皮肤"
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        if ppos[-1][2] == "object_part":
                            tail_part_value = ppos[-1][3]
                            # 原 ppos = [左侧+臀大肌+外侧缘+间隙内]
                            # 截断后 ppos = [左侧+臀大肌]
                            # 然后将自己 "皮肤" 放入ppos = [左侧+臀大肌+皮肤]
                            for j in range(len(ppos) - 1, -1, -1):
                                if ppos[j][2] == "symptom_obj":
                                    part_special_sit = 1
                                    tmp_obj_idx = j
                                    # ppos = ppos[:tmp_obj_idx + 1]
                                    break

                if part_special_sit == 1:
                    # 样本 35
                    if tail_part_value != "囊性成分":
                        ppos = ppos[:tmp_obj_idx + 1]
                    else:
                        ppos.pop()

                ppos.append(x[i])

            elif tag == "exam":
                exam = x[i]
                exam_stack = [_connect_tag_and_value(x[i])]

            elif tag == "entity_neg":
                entity_neg = x[i]

            elif tag == "medical_events":
                medical_events = x[i]
                medical_events_stack.append(_connect_tag_and_value(x[i]))

            elif tag == "exam_item":
                items.append(x[i])

            elif tag == "symptom_deco":
                decorations.append(x[i])

            elif tag == "reversed_exam_result":
                results.append(x[i])

            elif tag == "exam_result":
                # step 1 把自己和items中的项拼接, 然后放入ir列表中 (不用考虑entity_neg)
                if len(items) > 0:
                    ir.extend([_connect_tag_and_value(j) + _connect_tag_and_value(x[i]) for j in items])
                else:
                    ir.append(_connect_tag_and_value(x[i]))

                # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
                ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

                # step 3 遇到最后一个exam_result ("如清楚")时, 输出+清空有关变量
                # [0, 1, 'symptom_obj', '头颅'],
                # [2, 3, 'exam_item', '形态'],
                # [4, 5, 'exam_result', '正常'],
                # [4, 5, 'exam_result', '清楚']
                if i == len(x) - 1:

                    # 根据每一个标签的索引, 比如[293, 293, 'symptom_obj', '肾'] 中的 293, 对以下各项进行先后排序:
                    # items, ppos, treatment_stack, exam_stack

                    # 将各个stack放入 itertools.product 函数所需的参数中
                    product_params = _build_product_param(exam_stack, ppo_stack, ir)

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    res_x.extend(["".join(j) for j in prod_res])

                    # 清空 items, ir, ppo_stack
                    items, ir, exam_stack, ppo_stack = [], [], [], []

                # 情况2举例 i < len(x) - 1)
                # 当遇到"均匀", "不宽"时，都会做2件事: 输出 + 清空变量
                # [9, 11, 'symptom_obj', '头部'],
                # [17, 19, 'exam_item', '骨密度'],
                # [20, 21, 'exam_result', '均匀'],
                # [23, 24, 'exam_item', '颅缝'],
                # [25, 26, 'exam_result', '不宽']
                # ...
                elif i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        # 将各个stack放入 itertools.product 函数所需的参数中
                        product_params = _build_product_param(ppo_stack, ir)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack
                        items, ir = [], []
                    ppo_stack = []

            elif tag == "symptom_desc":
                # step 1 把自己和 decorations 中的项拼接, 然后放入deco_desc列表中 (要考虑entity_neg)
                if len(decorations) > 0:
                    if entity_neg is None:
                        deco_desc.extend([_connect_tag_and_value(j) +
                                          _connect_tag_and_value(x[i]) for j in decorations])
                    else:
                        deco_desc.extend([_connect_tag_and_value(entity_neg) +
                                          _connect_tag_and_value(j) +
                                          _connect_tag_and_value(x[i]) for j in decorations])
                else:
                    if entity_neg is None:
                        deco_desc.append(_connect_tag_and_value(x[i]))
                    else:
                        deco_desc.append(_connect_tag_and_value(entity_neg) + _connect_tag_and_value(x[i]))

                # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
                if len(ppo_stack) > 0:
                    pass
                else:
                    ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

                # step 3 遇到 "扩张" 则输出
                # [80, 82, 'symptom_obj', '胆总管'],
                # [83, 84, 'entity_neg', '未见'],
                # [85, 86, 'symptom_desc', '扩张']
                if i == len(x) - 1:
                    # 将各个stack放入 itertools.product 函数所需的参数中
                    product_params = _build_product_param(ppo_stack, deco_desc)

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    res_x.extend(["".join(j) for j in prod_res])

                    # 清空 items, ir, ppo_stack
                    decorations, deco_desc, ppo_stack = [], [], []

                # 情况2举例 i < len(x) - 1)
                # 当遇到"均匀", "不宽"时，都会做2件事: 输出 + 清空变量
                # [9, 11, 'symptom_obj', '头部'],
                # [17, 19, 'exam_item', '骨密度'],
                # [20, 21, 'exam_result', '均匀'],
                # [23, 24, 'exam_item', '颅缝'],
                # [25, 26, 'exam_result', '不宽']
                # ...
                if i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        # 将各个stack放入 itertools.product 函数所需的参数中
                        product_params = _build_product_param(ppo_stack, deco_desc)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack 和 entity_neg
                        decorations, deco_desc, ppo_stack = [], [], []
                        entity_neg = None

            elif tag == "reversed_exam_item":
                # step 1 把自己和 results 中的项拼接, 然后放入 reversed_ir 列表中 (不用考虑entity_neg)
                if len(results) > 0:
                    reversed_ir.extend([_connect_tag_and_value(j) + _connect_tag_and_value(x[i]) for j in results])
                else:
                    reversed_ir.append(_connect_tag_and_value(x[i]))

                # step 2 将 ppos 中的项, 按照不同情况拼接后，放入ppo_stack中
                ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

                # step 3 遇到最后一个 reversed_exam_item ("如信号影")时, 输出+清空有关变量
                # [19, 21, 'symptom_obj', '肾脏'],
                # [22, 27, 'reversed_exam_result', '未见明显异常'],
                # [28, 30, 'reversed_exam_item', '信号影']
                if i == len(x) - 1:
                    # 将各个stack放入 itertools.product 函数所需的参数中
                    product_params = _build_product_param(medical_events_stack, ppo_stack, reversed_ir)

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    res_x.extend(["".join(j) for j in prod_res])

                    # 清空 items, ir, ppo_stack
                    results, reversed_ir, ppo_stack = [], [], []

                # 情况2举例 i < len(x) - 1)
                # 遇到 "信号影"时输出
                # [9, 11, 'symptom_obj', '头部'],
                # [17, 19, 'reversed_exam_result', '未见明显异常'],
                # [20, 21, 'reversed_exam_item', '信号影'],
                # [23, 24, 'exam_item', '颅缝'],
                # [25, 26, 'exam_result', '不宽']
                # ...
                elif i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        # 将各个stack放入 itertools.product 函数所需的参数中
                        product_params = _build_product_param(ppo_stack, reversed_ir)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack
                        results, reversed_ir, ppo_stack = [], [], []

        # 统计所有结果
        output_list.extend(res_x)

    return output_list


if __name__ == "__main__":
    sample = samples[int(sys.argv[1])]
    ans = exam_standard(sample)
    print("\n")
    for r in ans:
        print(r)
