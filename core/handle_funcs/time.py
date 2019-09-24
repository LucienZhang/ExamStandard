from core.utils import connect


def handle_time(seg, text, res_seg, i, stack):
    # 找到time之前最近的一个标点符号, 将标点到当前time之间所有的tag拼一起，再和自己拼接
    punctuation_idx = 0
    for char_idx in range(seg[i][0], -1, -1):
        if text[char_idx] in ["，", "。", "；", ".", "："]:
            punctuation_idx = char_idx
            break

    all_tags_between_punctuation_and_time = []
    for tagOne in seg[:i]:
        if tagOne[0] in range(punctuation_idx, seg[i][0]):
            all_tags_between_punctuation_and_time.append(tagOne)

    # 将自己也放进去
    all_tags_between_punctuation_and_time.append(seg[i])

    # 按序拼接
    tmp = [connect(each_tag) for each_tag in all_tags_between_punctuation_and_time]
    stack[seg[i][2]] = ["".join(tmp)]

    return res_seg, stack
