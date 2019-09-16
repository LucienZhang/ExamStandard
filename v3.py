from itertools import product
from copy import deepcopy


# v3 根据100个样本统计结果, 定义多种情况

# ppos定义:
# 是指一段连续的(长度可能1，也可能大于1)，全部是 pos, obj, 或者obj_part 的一段列表， 从seg中提取获得
# 如:
# [44, 45, 'symptom_obj', '关节']
# [46, 46, 'object_part', '囊']
# [48, 49, 'symptom_pos', '周围']
# [50, 52, 'object_part', '软组织']
# [53, 53, 'entity_neg', '无']
# [54, 55, 'symptom_deco', '明显']
# [56, 57, 'symptom_desc', '肿胀'],
# [58, 58, "object_part", "硬组织"],
# [59, 60, 'symptom_deco', '异常']
# [61, 63, 'symptom_desc', '密度影']

# 这段seg中, 有2个ppos, 分别是:
# ppos_1 = [
# [44, 45, 'symptom_obj', '关节']
# [46, 46, 'object_part', '囊']
# [48, 49, 'symptom_pos', '周围']
# [50, 52, 'object_part', '软组织']
# ]

# ppos_2 = [
# [58, 58, "object_part", "硬组织"]
# ]


# 该函数用来判断当前ppo属于哪种情况
def check_ppo_situation(ppo_list):
    """
    pos: 1
    obj: 2
    part: 3
    pos + obj: 4
    pos + part: 5
    obj + part: 6
    pos + obj + part: 7
    :param ppo_list:
    :return: situation
    """

    sit = None
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

    if pos in check_list and obj not in check_list and part not in check_list:
        sit = 1
    elif pos not in check_list and obj in check_list and part not in check_list:
        sit = 2
    elif pos not in check_list and obj not in check_list and part in check_list:
        sit = 3
    elif pos in check_list and obj in check_list and part not in check_list:
        sit = 4
    elif pos in check_list and obj not in check_list and part in check_list:
        sit = 5
    elif pos not in check_list and obj in check_list and part in check_list:
        sit = 6
    elif pos in check_list and obj in check_list and part in check_list:
        sit = 7

    return sit


# 根据ppos情况, 在以下函数中定义具体每种子情况的处理方式
def handle_ppos(segment, ppos, situation):
    """

    :param segment:
    :param ppos:
    :param situation: 这个参数就是check_ppo_situation函数返回的 sit 值
    :return: 拼好的ppo组合, 如:
    res = [(['symptom_pos', '右'], ['symptom_obj', '肾']), (['symptom_pos', '右'], ['symptom_obj', '肝脏'])]
    """

    ppos_tag = [j[2] for j in ppos]
    ppos_value = [j[3] for j in ppos]
    current_sit = None
    res = []

    # 1 只有pos
    if situation == 1:
        # 样本36
        for ppo in ppos:
            res.append(ppo)

    # 2 只有 obj (1个 / 多个)
    elif situation == 2:
        # 先判断属于哪种子情况
        sit_2_dict = {
            1: [
                ["symptom_obj"]
            ],
            2: [
                ["symptom_obj", "symptom_obj"],
                ["symptom_obj", "symptom_obj", "symptom_obj"],
                ["symptom_obj", "symptom_obj", "symptom_obj", "symptom_obj"]
            ]
        }
        for k, v in sit_2_dict.items():
            if ppos_tag in v:
                current_sit = k

        # 根据子情况处理
        if current_sit == 1:
            res = ppos[2:]
        elif current_sit == 2:
            # TODO 判断obj之间关系
            res = [j[2:] for j in ppos]

    # 3 只有 obj_part
    elif situation == 3:
        print("情况%d" % situation)
    elif situation == 4:
        sit_4_dict = {
            1: [
                ["symptom_pos", "symptom_obj"],
                ["symptom_pos", "symptom_obj", "symptom_obj"],
                ["symptom_pos", "symptom_obj", "symptom_obj", "symptom_obj"],
                ["symptom_pos", "symptom_obj", "symptom_obj", "symptom_obj", "symptom_obj"]
            ]
        }
        for k, v in sit_4_dict.items():
            if ppos_tag in v:
                current_sit = k
        if current_sit == 1:
            a = [ppos[0][2:]]  # a =[['symptom_pos', '右']]
            b = [j[2:] for j in ppos[1:]]  # b = [['symptom_obj', '肾'], ['symptom_obj', '肝脏']]
            res = list(product(*[a, b]))
            # res = [(['symptom_pos', '右'], ['symptom_obj', '肾']), (['symptom_pos', '右'], ['symptom_obj', '肝脏'])]
        elif current_sit == 2:
            pass
    elif situation == 5:
        print("情况%d" % situation)
        pass
    elif situation == 4:
        print("情况%d" % situation)
        pass
    elif situation == 4:
        print("情况%d" % situation)
        pass
    return res


# 将结果存入res_x
def build_res_x(x, res_x, stack, current_ppo_count, ppos_idx, print_info=True):
    # cs: copied_stack 简写
    cs = deepcopy(stack)
    #print("原stack: ", cs)
    #print("ppo_index: ", ppos_idx)
    #print("当前ppo_count: ", current_ppo_count)
    # 1 看看有几个 ppos
    if len(ppos_idx) == 1:  # obj + [] 直接拼, 不用考虑隔开的情况
        # 先去空列表
        while [] in cs:
            for each in cs:
                if len(each) == 0:
                    cs.pop(cs.index(each))
            if [] not in cs:
                #print("复制的剔除[]后的stack: ", cs)
                break
        # 再将 cs 中的唯一一个 ppos 排列组合
        new_ppos = []
        for j in cs[ppos_idx[1]]:
            tmp = ["$"+k[0]+k[1] for k in list(j)]
            new_ppos.append("".join(tmp))
        cs[ppos_idx[1]] = new_ppos
        #print("合并ppos后的cs: ", cs)
        #print("没动的原始stack: ", stack)

        # 最后对cs排列组合
        tmp_list = product(*cs)
        for tmp_tuple in tmp_list:
            tmp = "".join(tmp_tuple)
            res_x.append(tmp)
        if print_info:
            print("res_x:")
            for a in res_x:
                print(a)
    elif len(ppos_idx) > 1: # obj + [] + obj + []的情况，是否需要隔着ir去前一个ppos拼 ppo,在这里判断
        pass


if __name__ == "__main__":
    x = [
        # [17, 18, 'symptom_desc', '增大'],
        [13, 13, 'symptom_pos', '右'],
        [14, 14, 'symptom_obj', '肾'],
        [14, 14, 'symptom_obj', '肝脏'],
        [15, 16, 'exam_item', '体积'],
        [17, 18, 'exam_result', '增大'],
        #[13, 13, 'symptom_pos', '双侧'],
        #[14, 14, 'symptom_obj', '大脑'],
        [14, 14, 'object_part', '某部分'],
        [15, 16, 'exam_item', '大小'],
        # [15, 16, 'exam_item', '形态'],
        [17, 18, 'exam_result', '正常']
    ]

    ppo_tags = ["symptom_pos", "symptom_obj", "object_part"]
    stack = []
    res_x = []
    items = []
    ir = []
    idx_ir = None
    ppos_count = 0
    ppos_idx = {}  # 记录每个ppos在stack中的索引位置

    for i in range(len(x)):
        tag = x[i][2]
        value = x[i][3]
        if tag == "symptom_pos":
            # 在 ppos 头部获取 start索引
            if i == 0:
                ppo_start_idx = 0
            else:
                if x[i - 1][2] not in ppo_tags:
                    ppo_start_idx = i

            # 在 ppos 尾部做两件事: 1 获取end索引; 2 处理ppos
            if x[i + 1][2] not in ppo_tags:
                ppo_end_idx = i
                # 2 ppos
                ppos = x[ppo_start_idx:ppo_end_idx + 1]
                # 3 根据ppos判断是哪种结构(7种)
                situation = check_ppo_situation(ppos)
                # 根据某种具体结构, 再细化处理每种不同子情况
                processed_ppos = handle_ppos(x, ppos, situation)
                # 处理完成的ppos放入 stack
                stack.append(processed_ppos)
                # 记录当前放入的 ppos在stack中的索引位
                ppos_count += 1
                ppos_idx[ppos_count] = len(stack) - 1

                # 清理变量值
                ppo_start_idx, ppo_end_idx = None, None
                ppos = []
        elif tag == "symptom_obj":
            if i == 0:
                ppo_start_idx = 0
            else:
                if x[i - 1][2] not in ppo_tags:
                    ppo_start_idx = i
            if x[i + 1][2] not in ppo_tags:
                ppo_end_idx = i
                ppos = x[ppo_start_idx:ppo_end_idx + 1]
                situation = check_ppo_situation(ppos)
                processed_ppos = handle_ppos(x, ppos, situation)
                stack.append(processed_ppos)
                ppos_count += 1
                ppos_idx[ppos_count] = len(stack) - 1

                ppo_start_idx, ppo_end_idx = None, None
                ppos = []
        elif tag == "exam_item":
            items.append("$" + x[i][2] + x[i][3])
        elif tag == "exam_result":
            #print("当前ppos_count: ", ppos_count)
            if len(items) > 0:
                ir.extend([j + "$" + x[i][2] + x[i][3] for j in items])
            elif len(items) == 0:
                ir.append("$" + x[i][2] + x[i][3])

            if i == len(x) - 1:
                items = []
                stack.append(ir)
                idx_ir = len(stack) - 1
                # 输出
                build_res_x(x, res_x, stack, ppos_count, ppos_idx)
                stack[idx_ir] = []
                ir = []
            else:
                if x[i+1][2] != tag:
                    items = []
                    stack.append(ir)
                    idx_ir = len(stack) - 1
                    build_res_x(x, res_x, stack, ppos_count, ppos_idx)
                    stack[idx_ir] = []
                    ir = []
