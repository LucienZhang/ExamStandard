from core.utils import get_sort_key


def build_sorted_product_params(*unsorted_stacks):
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


# def build_sorted_product_params(*args, **stacks):
#     """
#     该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
#     :param args: items, exam_stack, ppos 等, 用来排序
#             stacks: ppo_stack, exam_stack, ir, deco_desc等, 根据排序结果, 将stacks按顺序构造最终返回的响应.
#     :return: 根据索引排好先后顺序的列表, 直接作为 itertools.product 函数的参数
#     """
#
#     # stack_map中, key是每个stack名称, value是列表, 是该 stack 的排序依据标签
#     stack_map = {
#         "exam_stack": ["exam"],
#         "ppo_stack": ["symptom_pos", "symptom_obj", "object_part"],
#         "ir": ["exam_item", "exam_result"],
#         "deco_desc": ["symptom_desc"],
#         "reversed_ir": ["reversed_exam_result"],
#         "lesion_stack": ["lesion"],
#         "ll_stack": ["lesion_desc"],
#         "medical_events_stack": ["medical_events"],
#         "time_stack": ["time"],
#         "entity_neg_stack": ["entity_neg"],
#         "treatment_stack": ["treatment"],
#         "tt_stack": ["treatment_desc"]
#     }
#
#     tmp1 = []
#     for i in list(args):
#         if len(i) > 0:
#             tmp1.append(i)
#     tmp1.sort(key=get_sort_key)
#     # print("排序后tmp1:\n%s\n" % tmp1)
#
#     tmp2 = []
#     c = 0
#     for j in tmp1:
#         tmp2.append({c: j[0][2]})
#         c += 1
#     # print("tmp2:\n%s\n" % tmp2)
#
#     tmp3 = []
#     for t in tmp2:
#         for k, v in stack_map.items():
#             if list(t.values())[0] in v:
#                 tmp3.append({int(list(t.keys())[0]): k})
#     # print("tmp3:\n%s\n" % tmp3)
#
#     res = []
#     for each_stack in tmp3:
#         for stack_name, stack_value in stacks.items():
#             if stack_name == list(each_stack.values())[0]:
#                 res.append({int(list(each_stack.keys())[0]): stack_value})
#     # print("res:\n%s\n" % res)
#
#     res.sort(key=get_sort_key)
#     sorted_product_params = [list(r.values())[0] for r in res]
#     # print("最终:\n%s\n" % sorted_product_params)
#
#     return sorted_product_params
