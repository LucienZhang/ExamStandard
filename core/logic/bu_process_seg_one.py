from core.utils import connect_tag_and_value
from core.logic.handle_obj import handle_obj
from core.logic.handle_exam_result import handle_exam_result
from core.logic.handle_lesion_desc import handle_lesion_desc


# def process_seg_one(seg, text, res_seg):
#     obj_stack = ObjStack()
#     exam_item_stack = ExamItemStack()
#     exam_result_stack = ExamResultStack()
#
#     for i in range(len(seg)):
#         tag = seg[i][2]
#         value = seg[i]
#         if tag == "symptom_obj":
#             obj_stack.push(value)
#
#         elif tag == "exam_item":
#             exam_item_stack.push(value)
#
#         elif tag == "exam_result":
#             exam_result_stack.push(value)
#
#             if check_print_timing(value, text):
#                 prod_res = list(product(*[obj_stack.stack, exam_item_stack.stack, exam_result_stack.stack]))
#                 res_seg.append(prod_res)
#
#     return res_seg


def process_seg_one(seg, text, res_seg):
    ppos, ppo_stack = [], []
    items, decorations = [], []
    results, reversed_ir = [], []
    ir, deco_desc = [], []
    medical_events, medical_events_stack = [], []
    treatment, treatment_stack, tt_stack = [], [], []
    exam, exam_stack = [], []
    time, time_stack = [], []
    entity_neg, entity_neg_stack = [], []
    lesion = []
    lesion_stack = []

    for j in seg:
        if j[2] == "lesion":
            lesion.append(j)
            lesion_stack.append(connect_tag_and_value(j))
            break

    for i in range(len(seg)):
        tag = seg[i][2]

        if tag == "symptom_obj":
            ppos = handle_obj(seg, ppos, i)

        elif tag == "exam_item":
            items.append(seg[i])

        elif tag == "exam_result":
            res_seg, items, ir, ppo_stack, exam_stack = handle_exam_result(seg, res_seg, items, ir, i, ppos, exam,
                                                                           lesion, medical_events, time, treatment,
                                                                           ppo_stack, exam_stack, lesion_stack,
                                                                           medical_events_stack, time_stack,
                                                                           treatment_stack)
        elif tag == "lesion":
            if seg[i] != lesion[0]:
                lesion.pop()
                lesion.append(seg[i])

        elif tag == "lesion_desc":
            if seg[i][3] in ["其中一个", "其一", "较大的", "测一"]:
                continue

            res_seg, ppo_stack = handle_lesion_desc(seg, res_seg, i, ppos, lesion, exam, entity_neg, time,
                                                    exam_stack, ppo_stack, entity_neg_stack, time_stack)

    return res_seg
