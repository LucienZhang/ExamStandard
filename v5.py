from itertools import product
import sys
from utils import split_target
from data.obj_rel_map import obj_rel_map
from data.test_0916 import samples


# 该函数用来构造 itertools.product 所需的参数
# 正确参数举例: [["$obj&肾", "%obj&肝脏"], ["$item&大小$exam_result&正常"]]
# 错误参数举例: [["$obj&肾", "%obj&肝脏"], [], [], ["$item&大小$exam_result&正常"]]
def _build_product_param(*stacks):
    ans = []
    for stackOne in stacks:
        if len(stackOne) > 0:
            ans.append(stackOne)
    return ans


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
    print(self_obj, other_obj)
    for obj in object_relation_map:
        if obj["name"] == self_obj:
            # "气管" 与 "纵隔"
            if other_obj in obj["rel"]["1"]:
                rel = 1

            # "气管" 与 "支气管"
            elif other_obj in obj["rel"]["2"]:
                rel = 2
            break

    return rel


# 该函数用来判断当前ppo属于哪种情况
def _check_ppo_situation(ppo_list):
    """
    分情况时不分先后, 只看有哪些标签
    obj: 1
    obj + part: 2
    obj + pos: 3
    obj + pos + part: 4
    如果没有obj: 5 (理论上不可能出现该情况)
    :param ppo_list:
    :return: situation
    """

    ppo_sit = None
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
    第二季端分情况, 要考虑顺序
    sit_stage_1: 第一阶段分出的情况
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
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_obj", "symptom_pos", "symptom_obj"]:
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

            # 样本2 双侧p + 额o + 颞o + 顶枕叶o + 脑沟内o
            if "symptom_pos" not in [j[2] for j in ppos[1:]]:
                tmp_list = list(product(*[[ppos[0]], ppos[1:]]))
                for tmp in tmp_list:
                    ppo_stack.append("".join([_connect_tag_and_value(k) for k in tmp]))

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
            # TODO 若要系统分辨，可能后续标注时, 需要将这种"和"，"及"等关键词都标出
            if [j[2] for j in ppos] == ["symptom_obj", "symptom_pos", "symptom_pos", "object_part"]:
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
                                        # 没有遇到
                                        pass

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
                if i != 0:
                    # xxx + obj + xxx
                    # 除了这种情况需要清空ppos外，其他情况一律将自己放入ppos即可
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        ppos = list()
                ppos.append(x[i])

            elif tag == "object_part":
                if i != 0:
                    # [ir] + part + xxx
                    if x[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:
                        # 样本3 中的 "皮肤"
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
                        if ppos[-1][2] == "object_part":
                            # 原 ppos = [['pos', '左侧'], ['obj', '臀大肌'], ["pos", "外侧缘"],
                            #           ["part"], "皮下脂肪"], ["part", "间隙内"]]
                            # 按照以下方式截断后, ppos = [['pos', '左侧'], ['obj', '臀大肌']]
                            # 然后将自己，即["part", "皮肤"] 放入ppos
                            for j in range(len(ppos) - 1, -1, -1):
                                if ppos[j][2] == "symptom_obj":
                                    tmp_obj_idx = j
                                    ppos = ppos[:tmp_obj_idx + 1]
                                    break
                ppos.append(x[i])

            elif tag == "exam":
                exam_stack = [_connect_tag_and_value(x[i])]

            elif tag == "entity_neg":
                entity_neg = x[i]

            elif tag == "medical_events":
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
                    print("ppos: ", ppos)
                    print("ppo_stack: ", ppo_stack)
                    print("\n")
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
                    print("ppos: ", ppos)
                    print("ppo_stack: ", ppo_stack)
                    print("\n")
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

                        # 清空 items, ir, ppo_stack
                        decorations, deco_desc, ppo_stack = [], [], []
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
                    print("ppos: ", ppos)
                    print("ppo_stack: ", ppo_stack)
                    print("\n")
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
    print("最终结果:\n")
    for r in ans:
        print(r)
