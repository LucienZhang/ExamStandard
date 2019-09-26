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
                        3.a 遇到part
                        3.b 遇到obj
                        3.c 遇到pos
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

                    elif tag == "symptom_obj":
                        break

                    elif tag == "symptom_pos":
                        if j > 0:
                            # stack["ppos"] = [[34,35,obj,左肾], [36,38,pos,周外侧]]
                            # 查看 "肾" 和 "周" 之间，是否有逗号，分号或者句号
                            has_comma_between_A_and_B = False
                            punctuations = ["，", "。", "；"]

                            for comma in punctuations:
                                if comma in text[stack["ppos"][j - 1][1] + 1:stack["ppos"][j][0]]:
                                    has_comma_between_A_and_B = True
                                    break

                            if has_comma_between_A_and_B:
                                pop_up_count_from_ppos += 1

    # step 3 使用 pop_up_count_from_ppos， 将需要出栈的部分, 从 stack[ppos] 中切掉
    if pop_up_count_from_ppos > 0:
        stack["ppos"] = stack["ppos"][:len(stack["ppos"]) - pop_up_count_from_ppos]

    # step 4 最后，将自己入栈
    stack["ppos"].append(seg[i])

    return res_seg, stack
