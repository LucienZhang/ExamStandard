# from core.logic.bu_check_obj_relationship import check_obj_relationship
from core.utils import connect


def check_obj_relationship_v2(current_obj, next_obj, text):
    """
    text_start_idx 和 text_end_idx: 从text原文本中切出一段字符串，判断这段字符串中是否有"、"，"及"，"和"等等连接词.
    """

    is_parallel = False
    flags = ["、", "和", "及"]

    text_start_idx = current_obj[1] + 1
    text_end_idx = next_obj[0]

    for flag in flags:
        if flag in text[text_start_idx:text_end_idx]:
            is_parallel = True
            break

    return is_parallel


def build_ppo_stack_by_obj(ppos, ppo_stack, text):
    """
    :param ppos: [[68, 69, 'symptom_obj', '小脑'], [71, 72, 'symptom_obj', '脑干'], [74, 75, 'symptom_obj', '垂体']]
    :param text: "小脑、脑干及垂体未见明显异常。"
    :param ppo_stack
    :return: ppo_stack = ['#68$69&symptom_obj*小脑^', '#71$72&symptom_obj*脑干^', '#74$75&symptom_obj*垂体^']


    函数中使用的变量解释:
    1. tmp_ppo_stack: 临时放置拼好的项, 将ppos遍历完之后，对 tmp_ppo_stack 中的项，做connect处理后，即为最终返回的ppo_stack.
    示例:
    tmp_ppo_stack = [
                        [[167, 171, 'symptom_obj', '肝内外胆管']],
                        [[173, 174, 'symptom_obj', '胆囊']],
                        [[176, 177, 'symptom_obj', '肠道']]
                    ]

    和以上tmp_ppo_stack对应的 ppo_stack 示例:
    ppo_stack = [
                    '#167$171&symptom_obj*肝内外胆管^',
                    #173$174&symptom_obj*胆囊^',
                    '#176$177&symptom_obj*肠道^'
                ]

    2. slice_start_idx 和 slice_end_idx: 2个指针。根据并列或者从属关系，从ppos中截取相应的项, 放入 tmp_list.
    3. is_parallel: 标志位, 如果是 True, 则 2个obj之间有顿号，及等连接词, 认为是并列关系;
                        如果是 False，则没有这些连词，认为是包含关系.

    4. ppos_idx: ppos的索引
    """

    # step 1 定义初始变量
    slice_start_idx = 0
    slice_end_idx = 1

    tmp_ppo_stack = []

    # step 2 obj两两查看关系，根据不同的关系，按照规则放入 tmp_ppo_stack
    for ppos_idx in range(len(ppos) - 1):
        is_parallel = check_obj_relationship_v2(current_obj=ppos[ppos_idx],
                                                next_obj=ppos[ppos_idx + 1],
                                                text=text)

        if is_parallel:
            tmp_ppo_stack.append(ppos[slice_start_idx:slice_end_idx])

            slice_start_idx = slice_end_idx
            slice_end_idx += 1

            if ppos_idx == len(ppos) - 2:
                tmp_ppo_stack.append([ppos[ppos_idx + 1]])

        else:
            slice_end_idx += 1

            if ppos_idx == len(ppos) - 2:
                tmp_ppo_stack.append(ppos[slice_start_idx:slice_end_idx])

    # step 3 统一将 tmp_ppo_stack 中的结果，格式化放入到最终返回的 ppo_stack
    for tmp in tmp_ppo_stack:
        ppo_stack.append("".join([connect(t) for t in tmp]))

    return ppo_stack
