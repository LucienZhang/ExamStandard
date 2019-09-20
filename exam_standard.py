class ExamStandardProcessor(object):
    """
    结构化拼接类.
    输入 text: 一段原文本
    输出 output_list: 结构化拼接出的结果
    """

    def __init__(self, text, targets):
        self.text = text
        self.targets = targets

    # 分割初始文本
    def slice_targets(self, display=False):
        idx = [0]
        for i in range(len(self.targets)):
            if self.targets[i][2] == "vector_seg":

                # case1 , 当遇到 obj"腹部" + exam"立位平片" + ": " 时，这种冒号不分割
                # "腹部立位平片示：腹部肠管内少量积气"

                # case2 (sample[1])
                # 遇到 "餐后扫查" + ", "时, 这种逗号不分割
                # "餐后扫查, 肠气干扰明显."

                # case3 (sample[97])
                # 这种连着2个vector_seg, 那么2个都不分割
                # [0, 1, 'symptom_obj', '腹部'],
                # [2, 5, 'exam', '急诊扫描'],
                # [6, 6, 'vector_seg', '，'],
                # [18, 18, 'vector_seg', '。']

                if i >= 1:
                    if self.targets[i - 1][2] == "exam":
                        if i >= 2:
                            # case1. case2
                            if self.targets[i - 2][2] in ["symptom_obj", "vector_seg"]:
                                continue
                        else:
                            continue

                    # case3
                    elif self.targets[i - 1][2] == "vector_seg":
                        continue

                # 其他情况正常分割
                if i != 0:
                    idx.append(i)

        sliced_targets = []
        for j in range(len(idx) - 1):
            sliced_targets.append(self.targets[idx[j]:idx[j + 1]])
        for k in sliced_targets:
            for m in k:
                if m[2] == "vector_seg":
                    k.pop(k.index(m))

        if display:
            for seg in sliced_targets:
                for s in seg:
                    print(s)
                print("")

        return sliced_targets

