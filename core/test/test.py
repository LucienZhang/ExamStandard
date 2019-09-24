from itertools import product
import sys

sys.path.insert(0, "/users/hk/dev/ExamStandard")

from core.test.utils import split_target
from data.obj_rel_map import obj_rel_map
from core.test.test_data import samples

# test_v2.py 可以 git checkout v1_2019_09_23_Monday


"""
# test.py 的更新:
# 1 加入了 lesion 和 lesion_desc 的输出 (line 1136 左右);
# 2 废弃了 _build_product_params 函数, 使用新的 _build_sorted_product_params 函数构造itertools.product所需的参数.
# 2.1 _build_sorted_product_params 支持根据每种stack的索引，排序后进行排列组合(比如exam出现在ppos前后，可以有不同的排序效果)

# 示例数据 (python v6.py 58):
[0, 1, 'symptom_pos', '双侧'],
[2, 2, 'symptom_obj', '额'],
[15, 16, 'lesion_desc', '索状'],
[17, 21, 'lesion', '异常信号影'],
[29, 32, 'exam_item', 'T1WI'],
[33, 36, 'exam_result', '略低信号'],
[55, 57, 'exam', 'DWI'],
[58, 61, 'reversed_exam_result', '未见明显'],
[62, 64, 'reversed_exam_item', '高信号'],
[73, 73, 'vector_seg', '，'],


若使用新的 _build_sorted_product_params 构造函数, 则输出结果如下:
(该示例中，按出现顺序，是 ppos先于 lesion先于 item_result 先于 reversed_result_item)

$symptom_pos&双侧$symptom_obj&额$lesion_desc&索状$lesion&异常信号影
$symptom_pos&双侧$symptom_obj&额$lesion&异常信号影$exam_item&T1WI$exam_result&略低信号
$symptom_pos&双侧$symptom_obj&额$exam&DWI$lesion&异常信号影$reversed_exam_result&未见明显$reversed_exam_item&高信号
"""


def _build_sorted_product_params(*args, **stacks):
    """
    该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
    :param args: items, exam_stack, ppos 等, 用来排序
            stacks: ppo_stack, exam_stack, ir, deco_desc等, 根据排序结果, 将stacks按顺序构造最终返回的响应.
    :return: 根据索引排好先后顺序的列表, 直接作为 itertools.product 函数的参数
    """

    # stack_map中, key是每个stack名称, value是列表, 是该 stack 的排序依据标签
    stack_map = {
        "exam_stack": ["exam"],
        "ppo_stack": ["symptom_pos", "symptom_obj", "object_part"],
        # 因为有可能items=[], 所以ir中加入"exam_result"也作为排序依据之一, 避免items为空, 导致无法排序的情况
        "ir": ["exam_item", "exam_result"],
        "deco_desc": ["symptom_desc"],
        "reversed_ir": ["reversed_exam_result"],
        "lesion_stack": ["lesion"],
        "ll_stack": ["lesion_desc"],
        "medical_events_stack": ["medical_events"],
        "time_stack": ["time"],
        "entity_neg_stack": ["entity_neg"],
        "treatment_stack": ["treatment"],
        "tt_stack": ["treatment_desc"]
    }

    tmp1 = []
    for i in list(args):
        if len(i) > 0:
            tmp1.append(i)
    tmp1.sort(key=_get_sort_key)
    # print("排序后tmp1:\n%s\n" % tmp1)

    tmp2 = []
    c = 0
    for j in tmp1:
        tmp2.append({c: j[0][2]})
        c += 1
    # print("tmp2:\n%s\n" % tmp2)

    tmp3 = []
    for t in tmp2:
        for k, v in stack_map.items():
            if list(t.values())[0] in v:
                tmp3.append({int(list(t.keys())[0]): k})
    # print("tmp3:\n%s\n" % tmp3)

    res = []
    for each_stack in tmp3:
        for stack_name, stack_value in stacks.items():
            if stack_name == list(each_stack.values())[0]:
                res.append({int(list(each_stack.keys())[0]): stack_value})
    # print("res:\n%s\n" % res)

    # 2019_09_20 注释: 观察发现, 以下结构中 irA 和 irB 基本都要和 lesion 拼, 所以暂时注释掉以下这部分处理
    # 如果x是 irA + lesion + irB 结构, 那么irA 单独输出, irB 才需要和 lesion 拼接
    # tmp_lesion_idx, tmp_ir_idx = None, None
    # ir_tags = ["exam_item", "exam_result", "symptom_deco",
    #            "symptom_desc", "reversed_exam_result", "reversed_exam_item"]
    #
    # for idx in range(len(res)):
    #     rv = list(res[idx].values())[0][0]
    #     rv_tag = rv[rv.index("$")+1:rv.index("&")]
    #     if rv_tag == "lesion":
    #         tmp_lesion_idx = idx
    #     elif rv_tag in ir_tags:
    #         tmp_ir_idx = idx
    #
    # if tmp_ir_idx is not None and tmp_lesion_idx is not None:
    #     if tmp_ir_idx < tmp_lesion_idx:
    #         res.pop(tmp_lesion_idx)

    res.sort(key=_get_sort_key)
    sorted_product_params = [list(r.values())[0] for r in res]
    # print("最终:\n%s\n" % sorted_product_params)

    return sorted_product_params


# # 该函数暂时不用
# def _build_product_param(*stacks):
#     """
#     该函数用来构造 itertools.product 所需的参数 (注: 参数中不可存在空列表)
#     正确参数举例: [["$obj&肾", "%obj&肝脏"], ["$item&大小$exam_result&正常"]]
#     错误参数举例: [["$obj&肾", "%obj&肝脏"], [], [], ["$item&大小$exam_result&正常"]]
#     """
#     product_param = []
#     for stackOne in stacks:
#         if len(stackOne) > 0:
#             product_param.append(stackOne)
#     return product_param


def _connect_tag_and_value(t):
    """
    输入: [53, 55, 'symptom_obj', '副鼻窦']
    输出: "$symptom_obj&副鼻窦"
    """
    return "$" + t[2] + "&" + t[3]


def _get_sort_key(elem):
    """
    用途: some_list.sort(key=_get_sort_key)
    参数: elem: 列表中的元素
    """
    # [[55, 57, 'exam', 'DWI']] -> 55
    # 样本28 obj + neg + part + desc, 用obj还是part的索引?

    # 样本35, 看起来用 part 作为索引会好一点
    # [35, 35, 'symptom_obj', '肾']
    # .....
    # [68, 70, 'exam', '增强后'],
    # [71, 74, 'object_part', '囊性成分']

    # 目前用 obj, 也就是ppos末尾项的索引 (符合样本35)
    if isinstance(elem, list):
        return elem[-1][0]

    # {0: ['$symptom_pos&双侧$symptom_obj&额']} -> 0
    elif isinstance(elem, dict):
        return int(list(elem.keys())[0])


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


def _build_ppo_stack_by_ppo_situation(ppos, ppo_stack, sit):
    """
    该函数基于_check_ppo_situation 返回的结果, 来分析具体情况
    sit: 在函数 _check_ppo_situation 中返回的情况
    :param ppos: [[96, 97, 'symptom_obj', '中脑'], [105, 106, 'symptom_obj', '小脑']]
    :return: ppo_stack
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

            elif [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "object_part"]:
                obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])

                # 样本100 颅骨内外板o + 板障o + 骨质p
                # part 和 每一个object 都拼
                if obj_rel == 1:
                    tmp_1 = [_connect_tag_and_value(k) for k in ppos[:-1]]
                    tmp_2 = [_connect_tag_and_value(ppos[-1])]

                    for tmp in list(product(*[tmp_1, tmp_2])):
                        ppo_stack.append("".join(tmp))

                # 样本24 室间隔o + 左室o + 后壁p
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
            # 样本45 盲肠o + 下方pos + 周围pos + 腹膜part 建议先拼成"盲肠+下方+周围+腹膜"
            # 样本91 (鼻咽腔o + 顶部pos) + (后上壁pos + 软组织part)
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
        # 先来的obj是other_obj, 后来的是self_obj
        if ppos[0][2] == "symptom_obj" and ppos[1][2] == "symptom_obj":
            obj_rel = _check_obj_relationship(self_obj=ppos[1][3], other_obj=ppos[0][3])
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

        # medical
        medical_events, medical_events_stack = [], []

        # treatment 用来存储进来的 treatment, 如 [[54, 57, 'treatment', '静脉注射']]
        # treatment_stack 是在没有treatment_desc时, 用来放置单独的 treatment, 如 ["$treatment&静脉注射"]
        # tt_stack 是遇到 treatment_desc时，将其和 treatment拼接后放进这个列表, 如样本55:
        # [0, 9, 'treatment', '插管后经肛管注入气体'],
        # [11, 17, 'treatment_desc', '压力约9KPa'],
        # [18, 18, 'vector_seg', '，'],

        # 那么 treatment = [[0, 9, 'treatment', '插管后经肛管注入气体']]
        # 遇到 treatment_desc "压力约9KPa"时候, 将其和 treatment内拼接，得到:
        # tt_stack = ["$treatment&插管后经肛管注入气体$treatment_desc&压力约9KPa"]
        treatment, treatment_stack, tt_stack = [], [], []  # 样本12中出现过 [54, 57, 'treatment', '静脉注射']

        # exam = [[28, 31, 'exam', 'CDFI']], exam_stack = ["$exam&CDFI"]
        exam, exam_stack = [], []

        # time
        time, time_stack = [], []

        # entity_neg
        entity_neg, entity_neg_stack = [], []

        # res_x: 存储一个seg (seg也就是x) 内所有拼接好的结果
        res_x = []

        # lesion: 病灶; lesion_desc_list: 存储病灶描述的列表
        lesion = []
        lesion_stack = []
        for j in x:
            if j[2] == "lesion":
                lesion.append(j)
                lesion_stack.append(_connect_tag_and_value(j))
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
                obj_special_sit = 0
                # 这个特殊情况是为了 "腹腔obj" + "扫查exam"这种结构, 因为在exam处会讲腹腔和扫查拼到一起，所以这里obj就pass即可
                if i == 0:
                    if i < len(x) - 1:
                        if x[i+1][2] == "exam":
                            obj_special_sit = 2

                elif i != 0:
                    # [] + obj + xxx
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        if len(ppos) > 0:
                            # 2019_09_17修改逻辑，当前是只看ppos数组尾巴项是否为obj
                            # 修改后, 只要ppos中有obj，就判断obj只看的关系
                            # 样本31 左pos + 髋关节obj + 各骨part + [] + 关节obj(自己) + part + []
                            # 遇到关节（自己）时，和ppos中的 髋关节比较关系

                            # if ppos[-1][2] == "symptom_obj":
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
                exam = [x[i]]
                exam_special_sit = 0

                # [62, 63, 'symptom_obj', '肝胆'],
                # [64, 65, 'exam', '显像'],
                # [68, 78, 'medical_events', '静脉注射示踪剂 1分钟'],
                # [81, 81, 'symptom_obj', '心'],
                # [83, 83, 'symptom_obj', '肝'],
                # [85, 85, 'symptom_pos', '双'],
                # [86, 86, 'symptom_obj', '肾'],
                # [87, 88, 'reversed_exam_result', '隐约'],
                # [89, 90, 'reversed_exam_item', '显影'],
                # [91, 91, 'vector_seg', '，']

                # 遇到以上"肝胆+显像"这种结构时，会讲肝胆和显像拼到一起，作为 exam_stack
                if i == 1:
                    if x[i-1][2] == "symptom_obj":
                        exam_special_sit = 1

                # 72标签 [24, 27, 'exam', '前位显像']
                if value == "前位显像":
                    exam_special_sit = 1

                if exam_special_sit == 1:
                    exam_stack = [_connect_tag_and_value(x[i-1]) +
                                  _connect_tag_and_value(x[i])]

                else:
                    exam_stack = [_connect_tag_and_value(x[i])]

            elif tag == "time":
                time = [x[i]]
                time_stack = [_connect_tag_and_value(x[i])]

            elif tag == "entity_neg":
                entity_neg = [x[i]]
                entity_neg_stack = [_connect_tag_and_value(x[i])]

            elif tag == "medical_events":
                medical_events = [x[i]]
                medical_events_stack = [_connect_tag_and_value(x[i])]

            elif tag == "treatment":
                treatment = [x[i]]
                treatment_stack = [_connect_tag_and_value(x[i])]

            elif tag == "treatment_desc":
                # 样本55 中出现过
                # [0, 9, 'treatment', '插管后经肛管注入气体'],
                # [11, 17, 'treatment_desc', '压力约9KPa'],
                # [18, 18, 'vector_seg', '，']

                # 样本72 (处理方式待定, 目前是treatment+treatment_desc拼接结构化结果)
                # [0, 3, 'treatment', '静脉注射'],
                # [4, 6, 'treatment_desc', '显像剂'],
                # [8, 13, 'time', '1-30分钟'],
                # [15, 18, 'time', '60分钟'],
                # [22, 23, 'symptom_obj', '腹部'],
                # [24, 27, 'exam', '前位显像'],
                # [28, 28, 'vector_seg', '，']

                # 与 treatment 拼接
                if len(treatment) > 0:
                    tt_stack = [_connect_tag_and_value(treatment[0]) +
                                _connect_tag_and_value(x[i])]

                # 构造 product_param
                product_params = _build_sorted_product_params([x[i]],
                                                              tt_stack=tt_stack)

                # 构造结构化结果
                prod_res = list(product(*product_params))

                # 结果存入 res_x
                res_x.extend(["".join(j) for j in prod_res])

                # 清空 tt_stack 和 treatment
                tt_stack = []
                treatment = []

            elif tag == "exam_item":
                items.append(x[i])

            elif tag == "symptom_deco":
                deco_special_sit = 0
                # [0, 1, 'symptom_obj', '腹部'],
                # [2, 5, 'exam', '立位平片'],
                # [7, 7, 'vector_seg', '：'],
                # [8, 12, 'symptom_obj', '腹部肠管内'],
                # [13, 14, 'symptom_deco', '少量'],
                # [15, 16, 'symptom_desc', '积气'],
                # [18, 27, 'symptom_deco', '以左上腹部结肠内稍多'],
                # [29, 30, 'entity_neg', '未见'],
                # [31, 32, 'symptom_deco', '明显'],
                # [33, 34, 'symptom_desc', '扩张'],
                # [36, 39, 'symptom_desc', '液气平面'],
                # [40, 40, 'vector_seg', '，'],
                # 样本7, 若遇到 "以左上腹部结肠内稍多", 不写入decorations

                # 若从当前deco开始, 到该seg结束，都没有desc的话，就不把这种deco 放入decoration
                if "symptom_desc" not in [k[2] for k in x[i:]]:
                    deco_special_sit = 1
                else:
                    if i < len(x) -1:

                        # 样本33 局部deco + 气道obj + 变狭窄desc
                        # 样本34 局部deco + 骨质part + 缺损desc
                        # 以上33，34两个样本中的 deco局部，都是需要放入 decorations 中的
                        if x[i+1][2] not in ["symptom_pos", "symptom_obj", "object_part"]:

                            # 暂时用这个逻辑来处理样本7中的 "以左上腹部结肠内稍多"
                            if x[i+1][2] not in ["symptom_deco", "symptom_desc"]:
                                deco_special_sit = 2

                if deco_special_sit != 1 and deco_special_sit != 2:
                    decorations.append(x[i])

            elif tag == "reversed_exam_result":
                results.append(x[i])

            elif tag == "lesion":
                # 特殊情况, 样本70中, 同一个seg下有2个lesion
                # [87, 87, 'symptom_pos', '左'],
                # [88, 89, 'symptom_obj', '顶叶'],
                # [90, 92, 'object_part', '侧脑室'],
                # [93, 95, 'object_part', '后角旁'],
                # [97, 106, 'lesion', '片状长T1长T2信号'],
                # [108, 109, 'exam_item', '边界'],
                # [110, 111, 'exam_result', '清晰'],
                # [113, 122, 'lesion', 'T2FLAIR低信号'],
                # [123, 123, 'vector_seg', '，'],
                if x[i] != lesion[0]:
                    lesion.pop()
                    lesion.append(x[i])

            elif tag == "lesion_desc":
                # 特殊情况: 以下列表中的暂不拼接:
                # 1. "其中一个";
                # 2. 样本56中的 "其一";
                # 3. 样本83 "较大的"
                # 4. 样本51 "测一"
                if value in ["其中一个", "其一", "较大的", "测一"]:
                    continue

                if len(lesion) > 0:
                    # 按lesion 和 lesion_desc 出现先后顺序排序，构造 ll_stack
                    # 样本2
                    # [7, 9, 'symptom_obj', '脑沟内'],
                    # [12, 14, 'lesion_desc', '许多条'],
                    # [15, 16, 'lesion_desc', '索状'],
                    # [17, 21, 'lesion', '异常信号影'],
                    # [24, 27, 'lesion_desc', '额叶明显'],
                    tmp_ll_stack = [lesion, [x[i]]]
                    tmp_ll_stack.sort(key=_get_sort_key)
                    # tmp_ll_stack:
                    # [[[12, 14, 'lesion_desc', '许多条']], [[17, 21, 'lesion', '异常信号影']]]

                    ll_stack = ["".join([_connect_tag_and_value(tmp[0]) for tmp in tmp_ll_stack])]
                    # ll_stack = ['$lesion_desc&许多条$lesion&异常信号影']

                    # 构造ppo_stack
                    ppo_stack = _build_ppo_stack(ppos=ppos, ppo_stack=ppo_stack)

                    # 构造结构化结果
                    # TODO 由于文本70的特殊情况,暂时把 entity_neg加入lesion_desc拼接中
                    # TODO 看下效果, 如果会错误拼接其他的entity_neg,则需要将其移除，另想办法
                    # 70样本如下(其中 deco"异常"需要先人为修改成 lesion_desc)
                    # [130, 131, 'exam', '增强'],
                    # [133, 134, 'symptom_obj', '颅内'],
                    # [135, 136, 'entity_neg', '未见'],
                    # [137, 138, 'symptom_deco', '异常'],
                    # [139, 141, 'lesion', '强化灶'],
                    # [142, 142, 'vector_seg', '。'],
                    product_params = _build_sorted_product_params(exam, ppos, [x[i]], entity_neg, time,
                                                                  exam_stack=exam_stack,
                                                                  ppo_stack=ppo_stack,
                                                                  ll_stack=ll_stack,
                                                                  entity_neg_stack=entity_neg_stack,
                                                                  time_stack=time_stack)
                    # product_params = _build_product_param(exam_stack, ppo_stack, ll_stack)
                    prod_res = list(product(*product_params))

                    # 结果存入res_x
                    res_x.extend(["".join(j) for j in prod_res])

                    # 清空 ppo_stack
                    ppo_stack = []

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
                    # 将各个stack放入 itertools.product 函数所需的参数中
                    # 考虑到有可能items为空(样本8), 使用自己的索引作为排序依据，而不再用items:
                    # [33, 33, 'vector_seg', '，'],
                    # [40, 41, 'exam', '骨龄'],
                    # [42, 47, 'exam_result', '约为6.5岁'],
                    # [48, 48, 'vector_seg', '。'],
                    product_params = _build_sorted_product_params(exam, ppos, [x[i]], lesion,
                                                                  medical_events, time, treatment,
                                                                  exam_stack=exam_stack,
                                                                  ppo_stack=ppo_stack,
                                                                  ir=ir,
                                                                  lesion_stack=lesion_stack,
                                                                  medical_events_stack=medical_events_stack,
                                                                  time_stack=time_stack,
                                                                  treatment_stack=treatment_stack)
                    # product_params = _build_product_param(exam_stack, ppo_stack, ir)

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
                        # 由于items可能为空, 所以排序依据不用items, 而是用当前exam_result的索引, 即x[i][0]
                        # 例子: 样本64, 遇到"7个时", 因为items是空的, 所以排序后不会输出"7个", 所以用x[i][3]= 8 来做索引:
                        # [0, 0, 'symptom_pos', '左'],
                        # [1, 4, 'symptom_obj', '手腕关节'],
                        # [8, 9, 'exam_result', '7个'],
                        # [10, 15, 'exam_item', '骨化中心发育']
                        product_params = _build_sorted_product_params(exam, ppos, [x[i]], lesion,
                                                                      medical_events, time, treatment,
                                                                      exam_stack=exam_stack,
                                                                      ppo_stack=ppo_stack,
                                                                      ir=ir,
                                                                      lesion_stack=lesion_stack,
                                                                      medical_events_stack=medical_events_stack,
                                                                      time_stack=time_stack,
                                                                      treatment_stack=treatment_stack)
                        # 以下旧版本函数已不再用
                        # product_params = _build_product_param(ppo_stack, ir)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])
                        # 清空 items, ir, ppo_stack
                        items, ir = [], []
                    ppo_stack = []

            elif tag == "symptom_desc":
                # 注意: symptom_desc用来描述symptom, 和lesion可以看作平行，故遇此标签, 可以不用考虑 lesion.

                # step 1 把自己和 decorations 中的项拼接, 然后放入deco_desc列表中
                if len(decorations) > 0:
                    deco_desc.extend([_connect_tag_and_value(j) +
                                      _connect_tag_and_value(x[i]) for j in decorations])
                else:
                    deco_desc.append(_connect_tag_and_value(x[i]))

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
                    # 注意, 由于较多时候,decorations都可能是空的，所以排序不用decOrations,而使用[x[i]]
                    # desc 中需要考虑 entity_neg
                    product_params = _build_sorted_product_params(exam, ppos, [x[i]], entity_neg, time,
                                                                  exam_stack=exam_stack,
                                                                  ppo_stack=ppo_stack,
                                                                  deco_desc=deco_desc,
                                                                  entity_neg_stack=entity_neg_stack,
                                                                  time_stack=time_stack)
                    # 旧函数不再用
                    # product_params = _build_product_param(ppo_stack, deco_desc)

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
                        # 特殊情况，样本70
                        # [50, 53, 'symptom_obj', '第四脑室'],
                        # [54, 55, 'symptom_desc', '扩大'],
                        # [57, 63, 'symptom_deco', '与前片大致相仿'],
                        # [64, 64, 'vector_seg', '；']
                        if x[i+1][2] == "symptom_deco":
                            if i == len(x) - 2:
                                # 将倒序的deco"与前片大致相仿"也拼进来
                                tmp_1 = deco_desc[0]
                                tmp_2 = _connect_tag_and_value(x[i+1])
                                deco_desc = [tmp_1 + tmp_2]

                        # 以下为正常情况下的处理流程:

                        # 将各个stack放入 itertools.product 函数所需的参数中
                        # 注意, 由于较多时候,decorations都可能是空的，所以排序不用decOrations,而使用[x[i]]
                        # desc 中需要考虑 entity_neg
                        product_params = _build_sorted_product_params(exam, ppos, [x[i]], entity_neg, time,
                                                                      exam_stack=exam_stack,
                                                                      ppo_stack=ppo_stack,
                                                                      deco_desc=deco_desc,
                                                                      entity_neg_stack=entity_neg_stack,
                                                                      time_stack=time_stack)
                        # 旧函数不再用
                        # product_params = _build_product_param(ppo_stack, deco_desc)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack 和 entity_neg
                        decorations, deco_desc, ppo_stack = [], [], []

                        # [20, 21, 'symptom_obj', '椎体'],
                        # [22, 23, 'exam_item', '形态'],
                        # [24, 25, 'exam_result', '正常'],
                        # [27, 28, 'entity_neg', '未见'],
                        # [29, 32, 'symptom_desc', '骨质破坏'],
                        # [34, 35, 'symptom_deco', '明显'],
                        # [36, 39, 'symptom_desc', '骨质增生'],
                        # [40, 40, 'vector_seg', '。'],
                        # 样本4. 以上示例中，遇到"骨质破坏"时不清除entity_neg,因为瞎 main的"骨质增生"也需要拼接"未见".
                        if x[i + 1][2] != "symptom_deco":
                            entity_neg = []

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
                    # product_params = _build_product_param(medical_events_stack, ppo_stack, reversed_ir)
                    product_params = _build_sorted_product_params(exam, ppos, results, lesion, medical_events, time,
                                                                  ppo_stack=ppo_stack,
                                                                  exam_stack=exam_stack,
                                                                  reversed_ir=reversed_ir,
                                                                  lesion_stack=lesion_stack,
                                                                  medical_events_stack=medical_events_stack,
                                                                  time_stack=time_stack)

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
                        product_params = _build_sorted_product_params(exam, ppos, results, lesion, medical_events, time,
                                                                      exam_stack=exam_stack,
                                                                      ppo_stack=ppo_stack,
                                                                      reversed_ir=reversed_ir,
                                                                      lesion_stack=lesion_stack,
                                                                      medical_events_stack=medical_events_stack,
                                                                      time_stack=time_stack)
                        # 以下旧版本函数已不再适用
                        # product_params = _build_product_param(ppo_stack, reversed_ir)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack
                        results, reversed_ir, ppo_stack = [], [], []
        print(" ")
        for aaa in res_x:
            print(aaa)

        # 统计所有结果
        output_list.extend(res_x)

    return output_list


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
