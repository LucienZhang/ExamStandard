from itertools import product
import sys
import getopt
from utils import split_target
from data.v4_test_data import v4_test_data, type_map


# 之前将所有标签放入一个统一 stack
# v4.py 分成多个 stack (ppo_stack, ir_stack, exam_stack等)


# 该函数用来构造 itertools.product 所需的参数
# 正确参数举例: [["$obj&肾", "%obj&肝脏"], ["$item&大小$exam_result&正常"]]
# 错误参数举例: [["$obj&肾", "%obj&肝脏"], [], [], ["$item&大小$exam_result&正常"]]
def _build_product_param(*stacks):
    ans = []
    for stackOne in stacks:
        if len(stackOne) > 0:
            ans.append(stackOne)
    return ans


# 该函数用来判断2个obj之间关系
def _check_obj_relationship(self_obj, other_objs):
    """
    :param self_obj: 自己 = "心脏"
    :param other_objs: ppo中已经存在的所有objs  = ['额', "肾", "肝脏"]
    :return: 1并列, 2从属
    """

    rel = 1
    # TODO 判断关系
    return rel


# 主函数
def exam_standard(origin_targets):

    # 分割为多个segments
    segments = split_target(origin_targets)

    # 定义最终返回的响应
    output_list = []

    for x in segments:

        # 初始化变量
        pos_or_obj_or_part = ["symptom_pos", "symptom_obj", "object_part"]

        # ppos解释: ppo是指 pos_part_obj的简写, s是指复数
        # ppos = [['$symptom_pos&双侧'], ['symptom_obj', '额']]
        ppos, ppo_stack = [], []

        # items存放遇到的 exam_item, ir是 exam_item_exam_result简写, 存放拼好的ir,比如"大小+正常"
        items, ir = [], []

        # 用来其他标签
        exam_stack, treatment_stack, medical_events = [], [], []

        # res_x: 存储一个seg (seg也就是x) 内所有拼接好的结果
        res_x = []

        # 每个seg中处理结构化拼接
        for i in range(len(x)):
            tag = x[i][2]
            value = "$" + x[i][2] + "&" + x[i][3]

            if tag == "symptom_pos":
                ppos.append([value])

            elif tag == "symptom_obj":
                # 遇到obj,做2件事
                # 1 根据一些规则, 将自己放入ppos
                # 2 如果自己后面不再是ppo, 则考虑将ppos中的项，按照一定的规则拼接, 并放入ppo_stack

                # 若ppos列表为空, 则直接放入
                if len(ppos) == 0:
                    ppos.append([value])

                # 若ppos不为空, 则:
                # 1 如果ppos中目前没有 obj, 那么直接放入(因为不需要和其他obj进行比较关系（并列，从属，等）)
                # 2 如果ppos中已经有 obj, 那么在这里调用 处理2个obj之间关系的函数,或者逻辑(TODO)
                else:
                    if tag not in [j[0][j[0].index("$") + 1:j[0].index("&")] for j in ppos]:
                        ppos.append([value])

                    # _check_obj_relationship 判断关系, 1并列 2从属
                    # 例子: ppo_stack = ["$obj&肾"], 有一个新的obj准备进入: "$obj&肝脏"
                    # 若并列: ppos =["$obj&肾", "$obj&肝脏"], 若从属, ppos = [["$obj&肾"], ["$obj&肝脏"]]
                    # objs_in_ppos 是当前ppos中已经有的所有obj
                    else:
                        objs_in_ppos = []
                        for ppo in ppos:
                            if ppo[0][ppo[0].index("$")+1:ppo[0].index("&")] == "symptom_obj":
                                tmp_obj = ppo
                                objs_in_ppos.extend([k[k.index("&")+1:] for k in ppo])
                        if _check_obj_relationship(self_obj=x[i][3], other_objs=objs_in_ppos) == 1:
                            tmp_obj.append(value)

                # TODO 制定具体的拼接规则

                # 情况1 遇到脑沟内, 后面没有part/pos/obj, 这种情况开始拼ppo_stack
                # [0, 1, 'symptom_pos', '双侧'],
                # [2, 2, 'symptom_obj', '额'],
                # [3, 3, 'symptom_obj', '颞'],
                # [4, 6, 'symptom_obj', '顶枕叶'],
                # [7, 9, 'symptom_obj', '脑沟内'],
                # [29, 32, 'exam_item', 'T1WI'],
                # [33, 36, 'exam_result', '略低信号']
                if x[i+1][2] not in pos_or_obj_or_part:
                    ppo_stack.extend(["".join(m) for m in list(product(*ppos))])

                else:
                    pass

            elif tag == "object_part":
                ppos.append([value])

            elif tag == "exam_item":
                items.append(value)

            elif tag == "exam_result":
                # 遇到 exam_result, 一般做3件事:
                # a 把自己和items中的项拼接, 然后放入ir列表中
                # 剩下的2件事是: b 把拼好的输出写入 res_x; c 并且在适当时候清空有关变量值
                # 但是b和c在处理时, 分为情况1和情况2, 下面有具体解释

                # step_a: 和 item 拼接, 并放入ir (ir 是 item_result简写)
                if len(items) > 0:
                    ir.extend([j + value for j in items])
                else:
                    ir.append(value)

                # 情况1举例 (i == len(x) - 1)
                # 遇到"正常"时，不会输出到 res_x中;
                # 遇到"清楚"时, 会做2件事: 输出到res_x + 清空items, ir, ppo_stack
                # [0, 1, 'symptom_obj', '头颅'],
                # [2, 3, 'exam_item', '形态'],
                # [4, 5, 'exam_result', '正常'],
                # [4, 5, 'exam_result', '清楚']
                if i == len(x) - 1:
                    # 将各个stack放入 itertools.product 函数所需的参数中
                    product_params = _build_product_param(ppo_stack, ir, exam_stack, treatment_stack)

                    # itertools.product
                    prod_res = list(product(*product_params))

                    # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                    res_x.extend(["".join(j) for j in prod_res])

                    # 清空 items, ir, ppo_stack
                    items, ir, ppo_stack = [], [], []

                # 情况2举例 i < len(x) - 1)
                # 当遇到"均匀", "不宽"时，都会做2件事: 输出 + 清空变量
                # [9, 11, 'symptom_obj', '头部'],
                # [17, 19, 'exam_item', '骨密度'],
                # [20, 21, 'exam_result', '均匀'],
                # [23, 24, 'exam_item', '颅缝'],
                # [25, 26, 'exam_result', '不宽']
                # ...
                if i < len(x) - 1:
                    if x[i + 1][2] != tag:
                        # 将各个stack放入 itertools.product 函数所需的参数中
                        product_params = _build_product_param(ppo_stack, ir, exam_stack, treatment_stack)

                        # itertools.product
                        prod_res = list(product(*product_params))

                        # 将拼出的结构化数据, 写入当前seg的res_x结果列表中
                        res_x.extend(["".join(j) for j in prod_res])

                        # 清空 items, ir, ppo_stack
                        items, ir, ppo_stack = [], [], []

        # 统计所有结果
        output_list.extend(res_x)

    return output_list


def main():
    opts, args = getopt.getopt(sys.argv[1:], "-h-t:-d:", ["type=", "data="])
    for opt_name, opt_value in opts:
        if opt_name in ("-t", "--type"):
            datatype = int(opt_value)
        elif opt_name in ("-d", "--data"):
            idx = opt_value
        elif opt_name == "-h":
            print(r'''Optional parameters:
                        python v4.py -t 1 -d 1 
                        t/type=[1=obj, 2=obj+part, 3=pos+obj, 4=pos+obj+part]
                        ''')
            sys.exit()

    output_list = exam_standard(v4_test_data[type_map[datatype-1]][idx])
    print("最终结果:\n")
    for resOne in output_list:
        print(resOne)


if __name__ == "__main__":
    main()
