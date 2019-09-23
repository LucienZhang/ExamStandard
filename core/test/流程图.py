"""
test_v2.py使用该流程

1. data = load_source_json_file(source_json_path)

2. 切分
for n in range(len(data)):
    targets = data[n]["targets"]
    segments = slice_targets(targets)

    init_stacks()

    3. 开始循环+拼接
    for seg in segments:
        for i in range(len(seg)):
            tag == seg[i]

            # seg[i] = [0, 1, 'symptom_obj', '胸廓']
            if tag == "symptom_obj":
                ppos = build_ppos(seg, i, ppos)

            elif s[2] == "symptom_pos":
                ppos = build_ppos(seg, i, ppos)

            elif s[2] == "object_part":
                ppos = build_ppos(seg, i, ppos)

            elif s[2] == "exam_item":
                exam_item_stack.append(s)
                # exam_item_stack = [[25, 26, 'exam_item', '边界']]

            elif s[2] == "exam_result":
                exam_result_stack.append(s)
                timing = check_build_timing(seg, i)
                if timing:
                    ppo_stack = build_ppo_stack(ppos, ppo_stack)
                    # ppos = [[0, 1, 'symptom_obj', '胸廓'], [2, 3, 'symptom_pos', '两侧']]
                    # 这种情况下, ppo_stack = [ppos]

                    tag_args_map = {
                        "symptom_obj": "ppo_stack",
                        "object_part": "ppo_stack",
                        "symptom_pos": "ppo_stack",
                        "exam_item": "exam_item_stack",
                        "exam_result": "exam_result_stack"
                    }
                    product_params = build_sorted_product_params(*args)
                    # ppo_stack[-1], exam_item_stack[-1], exam_result_stack[-1] 排序
                    # ppo_stack[-1] = 3, exam_item_stack[-1] = 26, exam_result_stack = [28]
                    # 排序后的res = [ppo_stack, exam_item_stack, exam_result_stack]

                    prod_res = list(product(*[product_params]))

                    for pr in prod_res:
                        res_seg.append(pr)

"""