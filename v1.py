from itertools import product
import sys
from utils import split_target
from copy import deepcopy
from data.samples import samples


# 将target列表, 按照vector_seg分成一段一段的seg
# 对每段seg进行处理


def build_res_x(stack, res_x, print_info=True):
    # 复制一个stack
    tmp_stack = deepcopy(stack)
    print("原始stack: ", tmp_stack)
    # 先将 tmp_stack 中的空列表剔除掉, 防止笛卡尔积product时失败(因为0乘以任何数都为0)
    while [] in tmp_stack:
        for each in tmp_stack:
            if len(each) == 0:
                tmp_stack.pop(tmp_stack.index(each))
        if [] not in tmp_stack:
            print("复制的剔除[]后的stack: ", tmp_stack)
            break
    # 剔除空列表后的 stack = [['关节'], ['囊', '周围软组织'], ['无'], ['明显肿胀']]
    tmp_list = product(*tmp_stack)
    for tmp_tuple in tmp_list:
        tmp = "".join(tmp_tuple)
        res_x.append(tmp)
    if print_info:
        print("res_x:")
        for a in res_x:
            print(a)


def func(result):
    # check_list 用途:
    # 在每次最后一个 exam_result/reversed_exam_item 或者 symptom_desc 输出后，判断是否需要清空 object_part 变量
    check_list = ["exam_result", "exam_item", "symptom_deco", "exam",
                  "entity_neg", "symptom_desc", "reversed_exam_item", "reversed_exam_result"]
    # 将初始一整段 target 分成多个小段
    target_list = split_target(result)
    # 初始化最终返回的响应
    output_list = []
    for x in target_list:
        print("\n")
        for aaa in x:
            print(aaa)

        # 如果x 长度为1，比如只有一个 symptom_obj, 其他什么都没，那不用判断了，直接过到下一个
        if len(x) == 1:
            continue

        # 初始化变量
        res_x = []
        stack = []

        items = []
        ir = []

        decorations = []
        deco_desc = []

        results = []
        reversed_ir = []

        pos_part = []
        pos_obj = []
        index_pos_part = None
        index_entity_neg = None
        index_pos_obj = None

        # 这个 index_pos 是专门为"既不和obj,又不和 obj_part拼接"的独立 pos 使用的索引
        # 当一个seg中多次出现独立pos时，需要根据该索引，将上一个pos从stack中清除掉
        # 示例: sample_36 "右叶内....中下部...", 其中"内"和"中下部"都是独立pos，但是到中下部时，需要将内清除掉
        # 该操作在 tag == "symptom_pos" 中完成
        index_pos = None

        # 初始化 lesion
        for a in x:
            lesion = ""
            if a[2] == "lesion":
                lesion = a[3]
                break

        # 开始每个 seg 的处理
        for i in range(len(x)):
            tag = x[i][2]
            value = x[i][3]
            if tag == "symptom_obj":
                if i == 0:
                    if x[i+1][2] != tag:
                        pos_obj.append(value)
                    else:
                        pos_obj.append(value + x[i+1][3])
                else:
                    if x[i-1][2] == "symptom_pos":
                        pos_obj.append(x[i-1][3] + value)
                    elif x[i-1][2] == tag:
                        # 如果前一个是obj, 那么还需要再往前看一项
                        # 如果上上一项不是 pos, 那么说明自己已经被添加过了，直接pass即可
                        # 如果上上一项是 pos, 那么说明自己没有被添加, 需要把自己放入 pos_obj 中
                        if i >= 2:
                            if x[i-2][2] != "symptom_pos":
                                pass
                            else:
                                # 这里有一个问题, "双肾盂肾盏"，这个双是只拼肾盂，还是2个都拼, 不好判断
                                # 目前处理是只拼前一个"肾盂"
                                pos_obj.append(value)
                    else:
                        if x[i+1][2] != tag:
                            pos_obj.append(value)
                        elif x[i+1][2] == tag:
                            pos_obj.append(value + x[i+1][3])
                        # 若同一seg内有多个obj，需要按以下逻辑判断
                        for j in range(i, 0, -1):
                            if x[j][2] == "symptom_obj":
                                for k in range(i, j, -1):
                                    if x[k][2] in ["exam", "symptom_pos,", "symptom_object", "object_part"]:
                                        if index_pos_obj is not None:
                                            stack[index_pos_obj] = []
                                        if index_pos_part is not None:
                                            stack[index_pos_part] = []
                        # 如果同一个seg有多个obj, 那么: 如果当前obj的前一项不在以下列表中，则清空前面的pos_obj和pos_part
                        # ["exam", "symptom_pos,", "symptom_object", "object_part"]
                        # if x[i-1][2] not in ["exam", "symptom_pos,", "symptom_object", "object_part"]:
                        #     if index_pos_obj is not None:
                        #         stack[index_pos_obj] = []
                        #     if index_pos_part is not None:
                        #         stack[index_pos_part] = []
                # 将 pos_obj 放入 stack:
                if x[i+1][2] != tag:
                    if x[i+1][2] == "symptom_pos":
                        if x[i+2][2] != tag:
                            stack.append(pos_obj)
                            index_pos_obj = len(stack) - 1
                            pos_obj = []
                    else:
                        stack.append(pos_obj)
                        index_pos_obj = len(stack) - 1
                        pos_obj = []
            elif tag == "object_part":
                if x[i-1][2] == "symptom_pos":
                    pos_part.append(x[i-1][3] + value)
                # obj + obj + obj_part, 这种part不能直接放到pos_part, 而是要和前面的obj拼在一起
                elif x[i-1][2] == "symptom_obj":
                    print("当前pos_obj: ", stack[index_pos_obj])
                    pos_part.append(value)
                else:
                    pos_part.append(value)
                if x[i+1][2] != "object_part" and x[i+1][2] != "symptom_pos":
                    stack.append(pos_part)
                    # 用完 pos_part 后清空
                    pos_part = []
                    # 记录 pos_part 在 stack 中的索引, 后面输出完之后要从stack中删掉该pos_part列表
                    index_pos_part = len(stack) - 1
            elif tag == "symptom_pos":
                # 情况1 如果在obj后面,而且要倒回去和 obj拼接, 那直接在这里将这种特殊 pos 放入stack中
                # 示例见 sample_22:  "胸廓" + "两侧"; sample_35: "肾"+"周外侧"
                # 情况2 如果前后都不是 obj或者obj_part, 是一个独立的pos，那直接放入 stack
                # 示例 sample_29: "内"
                if i != 0:
                    if x[i-1][2] == "symptom_obj":
                        if x[i+1][2] != "symptom_obj" and x[i+1][2] != "object_part":
                            # 情况1
                            if index_pos is not None:
                                stack[index_pos] = []
                            stack.append([value])
                            index_pos = len(stack) - 1
                    elif x[i-1][2] != "symptom_obj":
                        if x[i+1][2] != "symptom_obj" and x[i+1][2] != "object_part":
                            # 情况2
                            if index_pos is not None:
                                stack[index_pos] = []
                            stack.append([value])
                            index_pos = len(stack) - 1
            elif tag == "entity_neg":
                stack.append([value])
                index_entity_neg = len(stack) - 1
                # if index_neg is None:
                #     stack.append([value])
                #     index_neg = len(stack) - 1
                # else:
                #     # 清除stack中的上一个neg值
                #     stack[index_neg] = []
                #     stack.append([value])
            elif tag == "exam_item":
                items.append(value)
            elif tag == "exam":
                stack.append([value])
            elif tag == "time":
                stack.append([value])
            elif tag == "treatment":
                stack.append([value])
            elif tag == "medical_events":
                stack.append([value])
            elif tag == "exam_result":
                # 防止没有exam_item, 只有 obj + exam_result情况，这里判断 items 是否为空列表
                # 例: sample_8
                if len(items) > 0:
                    ir.extend([j + value for j in items])
                else:
                    ir.append(value)
                if "time" not in [j[2] for j in x[i+1:]]:
                    # 判断是否为最后一个
                    if i != len(x) - 1:
                        # 判断下一个是否为 exam_result(如果不是, 则输出)
                        if x[i+1][2] != tag:
                            # 清空items
                            items = []
                            stack.append(ir)
                            # 记录一个索引, result全部输出完之后要清空stack中的 ir
                            index_ir = len(stack) - 1
                            # 用完 ir 后清空
                            # 输出存在res_x中
                            build_res_x(stack, res_x, print_info=True)
                            # 清空 stack 中的 ir
                            stack[index_ir] = []
                            ir = []

                            # 判断下一项:
                            # 1 如果不在check_list中,那么说明当前obj已经列举完了,清空 stack[pos_part];
                            # 2 如果不在 ["exam_item", "exam_result"], 那么清空 stack[entity_neg]
                            if x[i + 1][2] not in check_list:
                                if index_pos_part is not None:
                                    print("index_pos_part ", stack[index_pos_part])
                                    stack[index_pos_part] = []
                            if x[i + 1][2] not in ["exam_item", "exam_result"]:
                                if index_entity_neg is not None:
                                    stack[index_entity_neg] = []
                    else:
                        stack.append(ir)
                        # 如果当前 exam_result 是整个seg的最后一个, 则: 1 输出; 2 清空 stack 中的 pos_part
                        # 输出
                        build_res_x(stack, res_x, print_info=True)
                else:
                    stack.append(ir)
                    ir = []
            elif tag == "symptom_deco":
                decorations.append(value)
            elif tag == "symptom_desc":
                if len(decorations) > 0:
                    deco_desc.extend([j + value for j in decorations])
                else:
                    deco_desc.append(value)
                if "time" not in [j[2] for j in x[i+1:]]:
                    if i != len(x) - 1:
                        if x[i+1][2] != tag:
                            # 清空 decorations
                            decorations = []
                            stack.append(deco_desc)
                            index_deco_desc = len(stack) - 1
                            # 输出存在 res_x 中
                            build_res_x(stack, res_x, print_info=True)
                            # 清空 stack 中的 deco_desc
                            print("stack中的ir: ", stack[index_deco_desc])
                            stack[index_deco_desc] = []
                            deco_desc = []

                            # 判断下一项:
                            # 1 如果不在check_list中,那么说明当前obj已经列举完了,清空 stack[pos_part];
                            # 2 如果不在 ["symptom_deco", "symptom_desc"], 那么清空 stack[entity_neg]
                            if x[i+1][2] not in check_list:
                                if index_pos_part is not None:
                                    print("index_pos_part ", stack[index_pos_part])
                                    stack[index_pos_part] = []
                            if x[i+1][2] not in ["symptom_deco", "symptom_desc"]:
                                if index_entity_neg is not None:
                                    stack[index_entity_neg] = []
                    else:
                        stack.append(deco_desc)
                        build_res_x(stack, res_x, print_info=True)
                else:
                    stack.append(deco_desc)
                    deco_desc = []
            elif tag == "reversed_exam_result":
                results.append(value)
            elif tag == "reversed_exam_item":
                # 如果seg[当前:最后] 之间没有time，才可以输出, 否则只是将自己放在stack中，但是不输出
                reversed_ir.extend([j + value for j in results])
                if "time" not in [j[2] for j in x[i+1:]]:
                    if i != len(x) - 1:
                        if x[i+1][2] != tag:
                            results = []
                            stack.append(reversed_ir)
                            index_reversed_ir = len(stack) - 1
                            build_res_x(stack, res_x, print_info=True)
                            print("stack中的reversed_ir: ", stack[index_reversed_ir])
                            stack[index_reversed_ir] = []
                            reversed_ir = []

                            # 判断下一项:
                            # 1 如果不在check_list中,那么说明当前obj已经列举完了,清空 stack[pos_part];
                            # 2 如果不在 ["symptom_deco", "symptom_desc"], 那么清空 stack[entity_neg]
                            if x[i + 1][2] not in check_list:
                                if index_pos_part is not None:
                                    print("index_pos_part ", stack[index_pos_part])
                                    stack[index_pos_part] = []
                            if x[i + 1][2] not in ["reversed_exam_item", "reversed_exam_result"]:
                                if index_entity_neg is not None:
                                    stack[index_entity_neg] = []
                    else:
                        stack.append(reversed_ir)
                        build_res_x(stack, res_x, print_info=True)
                else:
                    # 如果后面有time, 那么不输出，只把自己放进stack即可
                    stack.append(reversed_ir)
                    reversed_ir = []
            elif tag == "lesion_desc":
                # 目前规则, 只允许 lesion_desc 出现在 lesion 前面
                # 若出现, 则1 desc + lesion 拼接; 2 放入stack输出; 3从stack删掉
                stack.append([value + lesion])
                build_res_x(stack, res_x, print_info=True)
                print("stack中的ldesc_lesion: ", stack[-1])
                stack[-1] = []
            elif tag == "lesion":
                # 将自己单独放在 stack 中即可
                stack.append([lesion])
        output_list.extend(res_x)
    return output_list


def main():
    # data = load_file("/users/hk/test/normalization/data/goldset_93.json")
    # targets = [i["target"] for i in data]
    # n = sys.argv[1]
    # res = func_v8(targets[int(n)])
    idx = "sample_" + sys.argv[1]
    res = func(samples[idx])
    print("\n最终结果:\n")
    for z in res:
        print(z)


if __name__ == "__main__":
    main()
