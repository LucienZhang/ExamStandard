from core.handle_func_map import handle_func_map


def process_seg_one(seg, text, stack):
    """
    :param seg: 示例:
    seg = [
        [26, 26, 'symptom_pos', '左'],
        [27, 27, 'symptom_obj', '肾'],
        [28, 29, 'exam_item', '轮廓'],
        [30, 32, 'exam_result', '欠清晰']
    ]
    :param text: 示例:
    text = "腹主动脉清晰显影后2″右肾清晰显影，左肾轮廓欠清晰。肾血流灌注曲线示双肾灌注峰同时到达，左肾峰值较右肾略低。"
    :param stack: 示例:
    stack = {
        "exam_item": [..],
        "exam_result": [..],
        "ppo_stack": [..],
        ...
    }
    :return: res_seg: 示例:
    res_seg = [
                [
                    "#19$19&symptom_pos*右^#20$20&symptom_obj*肾^",
                    "#21$22&reversed_exam_result*清晰^",
                    "#14$15&reversed_exam_item*显影^"
                ],
                [
                    "#52$52&symptom_pos*左^#53$53&symptom_obj*肾^",
                    "#54$55&exam_item*峰值^",
                    "#56$60&exam_result*较右肾略低^"
                ]
    ]
    """
    res_seg = []

    for i in range(len(seg)):
        tag_type = seg[i][2]

        res_seg, stack = handle_func_map[tag_type](seg, text, res_seg, i, stack)

    return res_seg
