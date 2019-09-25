from core.utils import connect


def handle_symptom_deco(seg, text, res_seg, i, stack):
    # 倒序特殊情况, desc"积气" 拼不到 deco"以左上腹部结肠内稍多"
    # 原文: "腹部立位平片示：腹部肠管内少量积气，以左上腹部结肠内稍多，未见明显扩张及液气平面，双膈下未见游离气体。"

    if seg[i] != [18, 27, 'symptom_deco', '以左上腹部结肠内稍多']:
        stack[seg[i][2]].append(connect(seg[i]))

    return res_seg, stack
