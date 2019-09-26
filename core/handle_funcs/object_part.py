# 功能函数 1
def slice_sub_seg_between_current_object_part_and_next_comma(seg, text, i):
    """
    该函数用来从seg中，截取一段sub_seg，这段sub_seg开始是当前seg[i], 结束是从text找到离当前seg[i]最近的一个标点符号
    作用: 看一下如果这段sub_seg中有 symptom_obj, 那么说明腔内要和这个obj绑定，所以stack["ppos"]中的obj就要出栈

    示例:
    原文text = "膀胱壁无异常增厚，腔内未见异常密度，大小正常。"
    当前seg[i] 是 [9, 10, "object_part", "腔内"]

    :return: sub_seg = [[object_part, 腔内], [reversed_result, 未见异常], [reversed_item, 密度]]
    """

    # current_text_idx = 10, text_stop_idx = 10
    # seg_stop_idx = 22
    current_text_idx = seg[i][1]
    text_stop_idx = seg[i][1]
    seg_stop_idx = len(seg) - 1

    for text_idx in range(current_text_idx, len(text)):
        # 遇到了"异常密度"后面的逗号
        # text_stop_idx = 17
        if text[text_idx] in ["，", "。", "；"]:
            text_stop_idx = text_idx
            break
    for tag_one_idx in range(i, len(seg)):
        # [18, 19, "exam_item", "大小"] 中 18 > 17
        # seg_stop_idx = 18
        if seg[tag_one_idx][0] > text_stop_idx:
            seg_stop_idx = tag_one_idx
            break

    return seg[i+1:seg_stop_idx+1]


# 功能函数 2
def check_comma_existence_between_a_and_b(ppos, text, current_pos_index_from_ppos):
    """
    :param ppos: 即 stack["ppos"]
    :param current_pos_index_from_ppos: 当前在stack["ppos"] 中遇到的symptom_pos项, 在 stack["ppos"] 中的索引
    a 和 b 是 stack["ppos"] 中的 2 项
    该函数用来判断: a 和 b 之间在原文中是否有逗号

    示例数据:
    当前seg[i] == [37, 40, "object_part", "囊形成分"]
    stack["ppos"] = [[0, 0, 'symptom_pos', '左'], [1, 1, 'symptom_obj', '肾'], [2, 4, 'symptom_pos', '周外侧']]
    text = "左肾周外侧可见多房囊性病变，边界尚清，最大截面约3.7x1.7cm，增强后囊性成分未见明显强化。"

    该函数会查看"肾"和"周外侧"之间是否有逗号，句号或者分号.
    从结果中看出: "左肾周外侧" 是连续的，没有逗号，所以返回 False

    :return: True, 说明有逗号; False 说明没有逗号
    """

    # stack["ppos"] = [[34,35,obj,左肾], [36,38,pos,周外侧]]
    # 查看 "肾" 和 "周" 之间，是否有逗号，分号或者句号
    has_comma_between_a_and_b = False

    punctuations = ["，", "。", "；"]
    j = current_pos_index_from_ppos

    for comma in punctuations:
        if comma in text[ppos[j - 1][1] + 1:ppos[j][0]]:
            has_comma_between_a_and_b = True
            break

    return has_comma_between_a_and_b


# 主函数
def handle_obj_part(seg, text, res_seg, i, stack):
    """
    pop_up_count_from_ppos: 需要从 stack["ppos"] 中出栈的项的数量

    示例结构:
    part_x...., obj_A ....., obj_B part_y ...., part_z ....

    判断流程
    1 i 是否为 0
        1.1 i==0 --> 入栈 (即 part_x)
        1.2 i>0:

            2 前一项是否为 pos/obj/part
                2.1 是 --> 入栈 (part_y)
                2.2 若不是:

                    3 倒序查看stack["ppos"], 统计 pop_up_count_from_ppos 的值
                        3.a 遇到part --> line 44-46
                        3.b 遇到obj --> line 48-76
                        3.c 遇到pos --> line 78-91
    """

    # step 1 定义初始变量 pop_up_count_from_ppos

    # 举例: 比如 stack["ppos"] = [obj肾脏, part皮质],
    # pop_up_count_from_ppos = 1, 那么最后切片之后的 stack["ppos"]就是:
    # [obj肾脏]
    # 等于是让 part"皮质" 出栈
    pop_up_count_from_ppos = 0

    # step 2 倒序遍历stack[ppos], 统计 pop_up_count_from_ppos 值
    if i > 0:
        # A ...， B(当前seg[i])...。结构
        # 骨盆诸构成骨骨皮质连续，骨质(当前seg[i]) 信号均匀，...
        # seg[i-1] = [9, 10, 'symptom_desc', '连续']
        if seg[i - 1][2] not in ["symptom_obj", "symptom_pos", "object_part"]:

            # 遍历开始，分3种情况，即：在ppos中遇到pos, obj, part 分别如何处理
            # 如果判断完毕后 pop_up_count = 0, 说明不需要从 stack[ppos]移除任何项，直接将自己入栈即可
            if len(stack["ppos"]) > 0:
                for j in range(len(stack["ppos"]) - 1, -1, -1):
                    tag = stack["ppos"][j][2]

                    if tag == "object_part":
                        pop_up_count_from_ppos += 1
                        continue

                    # 举例: 当前seg[i] = [9, 10, "object_part", "腔内"]
                    # 原文: "膀胱壁无异常增厚，腔内未见异常密度，大小正常。"
                    elif tag == "symptom_obj":
                        # 调用功能函数 1
                        sub_seg = slice_sub_seg_between_current_object_part_and_next_comma(seg, text, i)

                        # sub_seg = [revesed_result未见异常, reversed_item密度]
                        # 也就是说, 从"腔内"到下一个逗号这一段文字中，没有任何obj，也就是说：
                        # 当前的part腔内, 无法和后面的obj绑定(因为没有)，只能和前面ppos中的obj绑定
                        # 所以 现在遇到的这个 obj"膀胱" 不用出栈，因为它还要继续和当前 part"腔内" 绑定.
                        if "symptom_obj" not in [check_item[2] for check_item in sub_seg]:
                            break

                    elif tag == "symptom_pos":
                        if j > 0:
                            # 调用功能函数 2
                            has_comma_between_a_and_b = check_comma_existence_between_a_and_b(stack["ppos"], text, j)

                            if has_comma_between_a_and_b:
                                pop_up_count_from_ppos += 1

    # step 3 使用 pop_up_count_from_ppos， 将需要出栈的部分, 从 stack[ppos] 中切掉
    if pop_up_count_from_ppos > 0:
        stack["ppos"] = stack["ppos"][:len(stack["ppos"]) - pop_up_count_from_ppos]

    # step 4 最后，将自己入栈
    stack["ppos"].append(seg[i])

    return res_seg, stack
