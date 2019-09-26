from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.utils import connect


def build_ppo_stack_by_obj(ppos, ppo_stack, text):
    """
    :param ppos: [[68, 69, 'symptom_obj', '小脑'], [71, 72, 'symptom_obj', '脑干'], [74, 75, 'symptom_obj', '垂体']]
    :param text: "小脑、脑干及垂体未见明显异常。"
    :param ppo_stack
    :return: ppo_stack = ['#68$69&symptom_obj*小脑^', '#71$72&symptom_obj*脑干^', '#74$75&symptom_obj*垂体^']

    tmp_list: 临时放置拼好的项, 将ppos遍历完之后，对tmp_list中的项，做connect处理后，即为最终返回的ppo_stack.
    slice_start_idx 和 slice_end_idx: 2个指针。根据并列或者从属关系，从ppos中截取相应的项, 放入 tmp_list.
    has_flag: 标志位, 如果是 True, 则 2个obj之间有顿号，及等连接词, 认为是并列关系;
                     如果是 False，则没有这些连词，认为是包含关系.

    ppos_idx: ppos的索引
    text_start_idx 和 text_end_idx: 从text原文本中切出一段字符串，判断这段字符串中是否有"、"，"及"，"和"等等连接词.
    """

    slice_start_idx = 0
    slice_end_idx = 1

    flags = ["、", "和", "及"]
    tmp_list = []

    for ppos_idx in range(len(ppos) - 1):
        has_flag = False

        text_start_idx = ppos[ppos_idx][1] + 1
        text_end_idx = ppos[ppos_idx + 1][0]

        for flag in flags:
            # 如果2个obj之间有顿号，那么has_flag置为True，结束 flags 的小循环
            if flag in text[text_start_idx:text_end_idx]:
                has_flag = True
                break

        # 这一组if else 是因为如果遇到最后一个ppos中的项， 那么不能再往后数，和后面的obj判断关系了（因为自己是最后一项）
        if ppos_idx < len(ppos) - 2:
            if has_flag:
                tmp_list.append(ppos[slice_start_idx:slice_end_idx])
                slice_start_idx = slice_end_idx

            slice_end_idx += 1

        # 如果自己是ppos中的倒数第二项, 那么不论是并列还是包含，这里都要最后一项ppos[-1]一同给处理了
        else:
            if has_flag:
                tmp_list.append(ppos[slice_start_idx:slice_end_idx])
                # 如果是并列，那么把最后一项也放入
                tmp_list.append([ppos[ppos_idx + 1]])

            else:
                # 如果是包含，那把2个obj拼一起，放入
                slice_end_idx += 1
                tmp_list.append(ppos[slice_start_idx:slice_end_idx])

    # tmp_list = [
    #               [[167, 171, 'symptom_obj', '肝内外胆管']],
    #               [[173, 174, 'symptom_obj', '胆囊']],
    #               [[176, 177, 'symptom_obj', '肠道']]
    #            ]
    for tmp in tmp_list:
        ppo_stack.append("".join([connect(t) for t in tmp]))

    # ppo_stack = ['#167$171&symptom_obj*肝内外胆管^', '#173$174&symptom_obj*胆囊^', '#176$177&symptom_obj*肠道^']
    
    return ppo_stack
