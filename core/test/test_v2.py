from itertools import product
import sys

sys.path.insert(0, "/users/hk/dev/ExamStandard")

from core.test.utils import split_target
from core.test.data.obj_rel_map import obj_rel_map
from core.test.data.v2_test_data import samples
from core.test.build_ppo_stack_func_map import build_ppo_stack_func_map


def get_sort_key(elem):
    if isinstance(elem[0], str):
        # elem = "#0$1&symptom_obj*肾"
        return int(elem[0][elem[0].index("$")+1:elem[0].index("&")])


def _build_sorted_product_params(*unsorted_stacks):
    """
    该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
    :param 排序前的 unsorted_stacks = [ppo_stack, exam_item_stack, exam_result_stack]
    :return: 排序后的 sorted_stacks
    """

    sorted_stacks = []
    for stackOne in unsorted_stacks:
        if len(stackOne) > 0:
            sorted_stacks.append(stackOne)

    sorted_stacks.sort(key=get_sort_key)

    return sorted_stacks


def _connect(t):
    """
    输入: [53, 55, 'symptom_obj', '副鼻窦']
    输出: "$symptom_obj&副鼻窦"
    """

    connected_str = "#" + str(t[0]) + "$" + str(t[1]) + "&" + t[2] + "*" + t[3]

    return connected_str


def _check_obj_relationship(self_obj, other_obj, object_relation_map=obj_rel_map):
    """
    该函数用来判断2个obj之间关系
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
def _check_ppo_situation(ppos):
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


def _build_ppo_stack_by_ppo_situation_v2(ppos, sit):
    ppo_stack = []

    if sit is not None:
        ppo_stack = build_ppo_stack_func_map[sit](ppos, ppo_stack)

    return ppo_stack


def _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit):
    """
    该函数基于_check_ppo_situation 返回的结果, 来分析具体情况
    sit: 在函数 _check_ppo_situation 中返回的情况
    :param ppos: [[96, 97, 'symptom_obj', '中脑'], [105, 106, 'symptom_obj', '小脑']]
    :return: ppo_stack
    """

    # 只有obj
    if sit == 1:
        obj_rel = _check_obj_relationship(self_obj=ppos[0][3], other_obj=ppos[1][3])
        if obj_rel == 1:
            ppo_stack = [_connect(j) for j in ppos]
        else:
            ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))

    # obj + part
    elif sit == 2:
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

    # obj + pos
    elif sit == 3:
        # 开头是 obj
        if ppos[0][2] == "symptom_obj":
            # 样本14 心o + 肝o + 双p + 肾o
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "symptom_pos", "symptom_obj"] or \
                    [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_obj"]:
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        if k == 0:
                            ppo_stack.append(_connect(ppos[k]))
                        else:
                            if ppos[k - 1][2] == "symptom_pos":
                                ppo_stack.append("".join([_connect(ppos[k - 1]),
                                                          _connect(ppos[k])]
                                                         ))
                            else:
                                ppo_stack.append(_connect(ppos[k]))

        # 开头是 pos
        elif ppos[0][2] == "symptom_pos":
            # 样本58 左p + 肱骨o + 中段p
            if [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos"]:
                ppo_stack.append("".join([_connect(k) for k in ppos]))

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
                            tmp_1 = _connect(ppos[0]) + _connect(tmp_obj[0])
                            tmp_2 = _connect(tmp_obj[1]) + _connect(ppos[k])
                            ppo_stack.append(tmp_1)
                            ppo_stack.append(tmp_2)

                        # (pos + obj + obj + pos) 暂未遇到
                        elif obj_rel == 2:
                            ppo_stack.append("".join([_connect(m) for m in ppos]))

            # 样本 87 双侧pos + 上颌窦obj + 双侧pos + 额窦obj + 蝶窦obj + 双侧pos + 筛窦内obj
            elif [j[2] for j in ppos] == ["symptom_pos", "symptom_obj", "symptom_pos", "symptom_obj",
                                          "symptom_obj", "symptom_pos", "symptom_obj"]:

                tmp_pos = None
                lucky_obj = None

                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_pos":
                        tmp_pos = _connect(ppos[k])
                    elif ppos[k][2] == "symptom_obj":
                        tmp = list()
                        tmp.append(_connect(ppos[k]))

                        if ppos[k - 1][2] == "symptom_pos":
                            lucky_obj = ppos[k]
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
                    ppo_stack.append("".join([_connect(k) for k in ppos]))

                # 若有多个obj, 则需要判断obj之间关系
                elif len(ppos[1:]) > 1:
                    obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[2][3])

                    if obj_rel == 1:
                        tmp_list = list(product(*[[ppos[0]], ppos[1:]]))

                        for tmp in tmp_list:
                            ppo_stack.append("".join([_connect(k) for k in tmp]))
                    elif obj_rel == 2:
                        tmp_2 = "".join([_connect(k) for k in ppos[1:]])
                        ppo_stack.append(_connect(ppos[0]) + tmp_2)

    # obj + pos + part
    elif sit == 4:
        # 开头是 obj
        if ppos[0][2] == "symptom_obj":
            # 样本11 鼻咽顶o + 后部pos + 软组织part
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "object_part"]:
                ppo_stack.append("".join([_connect(k) for k in ppos]))

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
                                tmp_2.append("".join([_connect(k) for k in tmp]))

                            tmp_3 = [_connect(ppos[0])]
                            tmp_final = list(product(*[tmp_3, tmp_2]))

                            for tmp in tmp_final:
                                ppo_stack.append("".join([k for k in tmp]))

                        elif k[3] == "盲肠":
                            ppo_stack.append("".join([_connect(k) for k in ppos]))

            # 2种情况 样本15种两个part之间没有"和"或者"及"连接; 样本85两个part之间有"及"连接
            elif [j[2] for j in ppos] == ["symptom_obj", "object_part", "symptom_pos", "object_part"]:
                for k in range(len(ppos)):
                    if ppos[k][2] == "symptom_obj":
                        # 15 原文 "枕骨隆突周围软组织局限性瘤性突起。" (没有"和、及"连接词)
                        if ppos[k][3] == "枕骨":
                            ppo_stack.append("".join([_connect(m) for m in ppos]))

                        # 86 原文 "关节囊及周围软组织无明显肿胀及异常密度影。" (有"及"连接词)
                        # 85 原文 "椎体(o)骨质(part)未见骨质增生或破坏，双侧(pos)骶孔(part)对称." (有逗号"，"分隔)
                        else:
                            tmp_part_list = []
                            for m in range(k + 1, len(ppos)):
                                if ppos[m][2] == "object_part":
                                    if m > 0:
                                        if ppos[m - 1][2] == "symptom_pos":
                                            tmp_1 = "".join([_connect(n) for n in ppos[m - 1:m + 1]])
                                            tmp_part_list.append(tmp_1)
                                        else:
                                            tmp_part_list.append(_connect(ppos[m]))

                            tmp_2 = [_connect(ppos[k])]
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
                    ppo_stack.append("".join([_connect(m) for m in tmp]))

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
                        tmp_1 = ["".join([_connect(k) for k in ppos[:2]])]
                        tmp_2 = [_connect(k) for k in ppos[2:]]

                        # 将 (pos+obj) 和 part 拼接, 放入 ppo_stack
                        for m in list(product(*[tmp_1, tmp_2])):
                            ppo_stack.append("".join(m))

                    # 样本2 左侧pos + 臀大肌obj + 外侧缘pos + 皮下脂肪part
                    elif "symptom_pos" in [j[2] for j in ppos[2:]]:
                        # tmp_1 是 (pos+obj), tmp_2 是 每一个part
                        tmp_1 = ["".join([_connect(k) for k in ppos[:2]])]

                        # 需要判断part前是否有pos，若有，则拼一起pos+part
                        tmp_2 = []
                        tmp_pos = None
                        for k in range(2, len(ppos)):
                            if ppos[k][2] == "symptom_pos":
                                tmp_pos = _connect(ppos[k])
                            elif ppos[k][2] == "object_part":
                                # 左侧 + 臀大肌 + 外侧缘 + 皮下脂肪
                                # 左侧 + 臀大肌 + 外侧缘 + 间隙内
                                if tmp_pos is not None:
                                    tmp_2.append(tmp_pos + _connect(ppos[k]))
                                # 左侧+ 臀大肌 + 皮肤
                                else:
                                    tmp_2.append(_connect(ppos[k]))

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
                                    tmp.append(_connect(ppos[k]))

                                    if ppos[k - 1][2] == "symptom_pos":
                                        tmp.insert(0, _connect(ppos[k - 1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect(ppos[k + 1]))

                                    elif ppos[k - 1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect(ppos[k + 1]))

                                    ppo_stack.append("".join(tmp))

                        # pos + obj + obj + obj + part + part
                        # 样本11 双侧pos + (上颌窦obj + 筛窦obj + 蝶窦obj) + 黏膜part
                        # 样本28 双侧pos + (筛窦obj + 蝶窦obj + 上颌窦obj) + (窦壁part + 黏膜part)
                        # 情况B 筛窦obj 要和 双侧pos 拼一起
                        else:
                            tmp_pos, tmp_obj, tmp_part = [], [], []
                            pos_obj = list()

                            tmp_pos.append(_connect(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(_connect(ppos[k]))

                                    if k < len(ppos) - 1:
                                        if ppos[k + 1][2] != "symptom_obj":
                                            # 先查看obj之间关系 1并列 2从属
                                            # 先来的是other_obj, 最后来的是self_obj
                                            obj_rel = _check_obj_relationship(self_obj=ppos[k][3],
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
                                    tmp_part.append(_connect(ppos[k]))

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

                            tmp_pos.append(_connect(ppos[0]))
                            for k in range(1, len(ppos)):
                                # step 1 将obj和前面的pos拼接，放入pos_obj中
                                if ppos[k][2] == "symptom_obj":
                                    tmp_obj.append(_connect(ppos[k]))

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
                                        tmp_part.append(_connect(ppos[k - 1]) +
                                                        _connect(ppos[k]))
                                    else:
                                        tmp_part.append(_connect(ppos[k]))

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
                                    tmp.append(_connect(ppos[k]))

                                    if ppos[k - 1][2] == "symptom_pos":
                                        tmp.insert(0, _connect(ppos[k - 1]))

                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect(ppos[k + 1]))

                                    elif ppos[k - 1][2] != "symptom_pos":
                                        if k < len(ppos) - 1:
                                            if ppos[k + 1][2] == "object_part":
                                                tmp.append(_connect(ppos[k + 1]))

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
                                    tmp_pos = _connect(ppos[k])
                                elif ppos[k][2] == "symptom_obj":
                                    tmp = list()
                                    tmp.append(_connect(ppos[k]))

                                    if k > 0:
                                        if ppos[k - 1][2] == "symptom_pos":
                                            tmp.insert(0, _connect(ppos[k - 1]))
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
                                    part.append(_connect(ppos[k]))

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
                        tmp_pos.append(_connect(ppos[k]))
                    elif ppos[k][2] == "symptom_obj":
                        tmp_obj.append(_connect(ppos[k]))

                for tmp in list(product(*[tmp_pos, tmp_obj])):
                    ppo_stack.append("".join(tmp))

        # 开头是 part
        elif ppos[0][2] == "object_part":
            # 样本48 余part + 双侧pos + 大脑半球obj + [] + 灰白质part + []
            if [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj"] or \
                    [j[2] for j in ppos] == ["object_part", "symptom_pos", "symptom_obj", "object_part"]:
                ppo_stack.append("".join([_connect(m) for m in ppos]))

    elif sit == 5:
        print("异常情况,当前ppos:")
        for ppo in ppos:
            print(ppo)

    return ppo_stack


def _build_ppo_stack(ppos):
    ppo_stack = []

    if len(ppos) == 1:
        ppo_stack.append(_connect(ppos[0]))

    # 5种情况 o+o, o + part/pos, pos/part + o (肯定有o)
    elif len(ppos) == 2:
        if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj"]:
            obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])
            if obj_rel == 1:
                ppo_stack = [_connect(j) for j in ppos]
            else:
                ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))
        else:
            ppo_stack.append(_connect(ppos[0]) + _connect(ppos[1]))

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
    res_segments = []

    for x in segments:

        # 初始化变量
        ppos, ppo_stack = [], []
        symptom_pos_stack, symptom_obj_stack, object_part_stack = [], [], []

        exam_item_stack, exam_result_stack = [], []
        reversed_exam_result_stack, reversed_exam_item_stack = [], []
        symptom_deco_stack, symptom_desc_stack = [], []

        # medical
        medical_events, medical_events_stack = [], []

        treatment_stack, treatment_desc_stack = [], []

        exam_stack = []

        time_stack = []

        entity_neg_stack = []

        res_x = []

        lesion_stack, lesion_desc_stack = [], []
        for j in x:
            if j[2] == "lesion":
                lesion_stack.append(_connect(j))
                break

        # 每个seg中处理结构化拼接
        for i in range(len(x)):
            tag = x[i][2]
            value = x[i][3]

            if tag == "symptom_pos":
                # pos + obj + xxx
                if i == 0:
                    ppos.append(x[i])
                else:
                    # obj + pos(自己) + obj
                    # obj + pos(自己)
                    # obj + pos(自己) + part 等
                    if x[i - 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
                        ppos.append(x[i])

                    else:
                        # xxx + pos + obj + xxx
                        # xxx + pos + part + xxx 等等
                        if x[i + 1][2] in ["symptom_obj", "symptom_pos", "object_part"]:
                            if x[i + 1][2] == "symptom_obj":
                                ppos = list()
                                ppos.append(x[i])

                            # xxx + pos + pos + xxx
                            # 暂时没有出现过
                            elif x[i + 1][2] == "symptom_pos":
                                pass

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
                                        ppos.append(x[i])

                        elif x[i + 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                            if len(ppos) > 0:
                                if ppos[-1][2] == "symptom_obj":
                                    ppos.append(x[i])

                                elif ppos[-1][2] == "symptom_pos":
                                    ppos.pop()
                                    ppos.append(x[i])

                                elif ppos[-1][2] == "object_part":
                                    # 没有遇到
                                    pass

            elif tag == "symptom_obj":
                obj_special_sit = 0
                if i == 0:
                    if i < len(x) - 1:
                        if x[i + 1][2] == "exam":
                            obj_special_sit = 2

                elif i != 0:
                    # [] + obj + xxx
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        if len(ppos) > 0:
                            if "symptom_obj" in [j[2] for j in ppos]:
                                # 先找到ppos中的obj
                                for k in ppos:
                                    if k[2] == "symptom_obj":
                                        other_obj = k[3]
                                        break

                                # 查看2个obj关系
                                obj_rel = _check_obj_relationship(self_obj=value, other_obj=other_obj)
                                # 只有这种是特殊情况, 需要清空ppos
                                if obj_rel == 1:
                                    obj_special_sit = 1

                if obj_special_sit == 1:
                    ppos = list()

                ppos.append(x[i])

                if obj_special_sit == 2:
                    ppos.pop()

            elif tag == "object_part":
                part_special_sit = 0

                if i != 0:
                    # 以上样本 中的 "皮肤"
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        if len(ppos) > 0:
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
                exam_stack = [_connect(x[i])]

            elif tag == "time":
                time_stack = [_connect(x[i])]

            elif tag == "entity_neg":
                entity_neg_stack = [_connect(x[i])]

            elif tag == "medical_events":
                medical_events_stack = [_connect(x[i])]

            elif tag == "treatment":
                treatment_stack = [_connect(x[i])]

            elif tag == "treatment_desc":
                treatment_desc_stack = [_connect(x[i])]
                # 构造 product_param
                product_params = _build_sorted_product_params(treatment_stack, treatment_desc_stack)

                # 构造结构化结果
                prod_res = list(product(*product_params))

                # 结果存入 res_x
                for pr in prod_res:
                    res_x.append(pr)

                # 清空 stack
                treatment_stack, treatment_desc_stack = [], []

            elif tag == "exam_item":
                exam_item_stack.append(_connect(x[i]))

            elif tag == "symptom_deco":
                symptom_deco_stack.append(_connect(x[i]))

            elif tag == "reversed_exam_result":
                reversed_exam_result_stack.append(_connect(x[i]))

            elif tag == "lesion":
                if x[i] != lesion_stack[0]:
                    lesion_stack.pop()
                    lesion_stack.append(_connect(x[i]))

            elif tag == "lesion_desc":
                if value in ["其中一个", "其一", "较大的", "测一"]:
                    continue

                lesion_desc_stack.append(_connect(x[i]))

                # 构造ppo_stack
                # TODO ppo_stack 测试中
                # ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)
                ppo_stack = [
                    "#0$1&symptom_obj*胸廓#2$3&symptom_pos*两侧"
                ]

                product_params = _build_sorted_product_params(exam_stack,
                                                              ppo_stack,
                                                              lesion_stack,
                                                              lesion_desc_stack,
                                                              entity_neg_stack,
                                                              time_stack)

                prod_res = list(product(*product_params))

                # 结果存入res_x
                for pr in prod_res:
                    res_x.append(pr)

                # 清空 ppo_stack
                ppo_stack = []

            elif tag == "exam_result":
                exam_result_stack.append(_connect(x[i]))

                # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
                # TODO ppo_Stack 测试中
                # ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)
                ppo_stack = [
                    "#0$1&symptom_obj*胸廓#2$3&symptom_pos*两侧"
                ]

                if i == len(x) - 1:
                    product_params = _build_sorted_product_params(exam_stack, ppo_stack,
                                                                  exam_item_stack, exam_result_stack,
                                                                  lesion_stack,
                                                                  medical_events_stack, time_stack, treatment_stack,
                                                                  )

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    for pr in prod_res:
                        res_x.append(pr)

                    # 清空 items, ir, ppo_stack
                    exam_item_stack, exam_result_stack = [], []
                    exam_stack, ppo_stack = [], []

                elif i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        product_params = _build_sorted_product_params(exam_stack, ppo_stack, exam_result_stack,
                                                                      lesion_stack,
                                                                      medical_events_stack, time_stack, treatment_stack,
                                                                      )

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        for pr in prod_res:
                            res_x.append(pr)
                        # 清空 items, ir, ppo_stack
                        exam_item_stack, exam_result_stack = [], []

                    ppo_stack = []

            elif tag == "symptom_desc":
                symptom_desc_stack.append(_connect(x[i]))

                # step 2 将ppos中的项, 按照不同情况拼接后，放入ppo_stack中
                # TODO ppo_stack 测试
                # ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)
                ppo_stack = [
                    "#0$1&symptom_obj*胸廓#2$3&symptom_pos*两侧"
                ]

                if i == len(x) - 1:
                    product_params = _build_sorted_product_params(exam_stack, ppo_stack,
                                                                  symptom_deco_stack, symptom_desc_stack,
                                                                  entity_neg_stack, time_stack,
                                                                  )

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    for pr in prod_res:
                        res_x.append(pr)

                    # 清空 items, ir, ppo_stack
                    symptom_deco_stack, symptom_desc_stack = [], []
                    ppo_stack = []

                if i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        product_params = _build_sorted_product_params(exam_stack, ppo_stack,
                                                                      symptom_deco_stack, symptom_desc_stack,
                                                                      entity_neg_stack, time_stack,
                                                                      )

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        for pr in prod_res:
                            res_x.append(pr)

                        # 清空 items, ir, ppo_stack
                        symptom_deco_stack, symptom_desc_stack = [], []
                        ppo_stack = []

                        if x[i + 1][2] != "symptom_deco":
                            entity_neg_stack = []

            elif tag == "reversed_exam_item":
                reversed_exam_item_stack.append(_connect(x[i]))

                # step 2 将 ppos 中的项, 按照不同情况拼接后，放入ppo_stack中
                # TODO ppo_stack 测试
                # ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)
                ppo_stack = [
                    "#0$1&symptom_obj*胸廓#2$3&symptom_pos*两侧"
                ]

                if i == len(x) - 1:
                    # 将各个stack放入 itertools.product 函数所需的参数中
                    product_params = _build_sorted_product_params(exam_stack, ppo_stack,
                                                                  reversed_exam_result_stack, reversed_exam_item_stack,
                                                                  lesion_stack,
                                                                  medical_events_stack, time_stack,
                                                                  )

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    for pr in prod_res:
                        res_x.append(pr)

                    # 清空 items, ir, ppo_stack
                    reversed_exam_result_stack, reversed_exam_item_stack = [], []
                    ppo_stack = []

                elif i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        # 将各个stack放入 itertools.product 函数所需的参数中
                        product_params = _build_sorted_product_params(exam_stack, ppo_stack,
                                                                      reversed_exam_result_stack,
                                                                      reversed_exam_item_stack,
                                                                      lesion_stack,
                                                                      medical_events_stack, time_stack,
                                                                      )

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        for pr in prod_res:
                            res_x.append(pr)

                        # 清空 items, ir, ppo_stack
                        reversed_exam_result_stack, reversed_exam_item_stack = [], []
                        ppo_stack = []

        print(" ")
        for aaa in res_x:
            print(aaa)

        # 统计所有结果
        res_segments.extend(res_x)

    return res_segments


if __name__ == "__main__":
    sample = samples[int(sys.argv[1])]
    ans = exam_standard(sample)

    # 以下为存储 json
    # final_res = []
    # for d in range(len(samples)):
    #     tmp = dict()
    #     tmp["id"] = d
    #     tmp["text"] = data[d]["input"]["text"]
    #     tmp["target"] = data[d]["target"]
    #     tmp["res"] = exam_standard(samples[d])
    #     final_res.append(tmp)
    #
    # save_file_name = "v6_output_0920.json"
    # save_file_path = "/users/hk/dev/ExamStandard/data/"
    # with open(save_file_path + save_file_name, "a") as f:
    #     json_obj = json.dumps(final_res, ensure_ascii=False, indent=4)
    #     f.write(json_obj)
