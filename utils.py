import json
import sys
import getopt
import pandas as pd


def load_file(file_name="goldset.json"):
    result = []
    line_count = 0
    count = 0
    print('Source file: {}'.format(file_name))
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            line_count = line_count + 1
            if line_count % 1000 == 0:
                print('line --- {}'.format(line_count))
            try:
                dic = json.loads(line)
                result.append(dic)
                count = count + 1
            except Exception as e:
                print(e)
                print('error line: {}'.format(line))
    print('Read source file finished: total={}, valid={}\n'.format(line_count, count))
    return result


# 分割初始文本
def split_target(origin_target):
    idx = [0]
    for i in range(len(origin_target)):
        if origin_target[i][2] == "vector_seg":
            idx.append(i)
    res = []
    for j in range(len(idx) - 1):
        res.append(origin_target[idx[j]:idx[j+1]])
    for k in res:
        for m in k:
            if m[2] == "vector_seg":
                k.pop(k.index(m))
    return res


def add_optional_parameters(data, rst, total_counter):
    # 函数所需的参数: data 是加载的初始数据; rst 是处理后的结果; total_counter 是统计的每个标签数量
    # -h --help
    # --json= 存储为 json
    # --csv= 存储为 csv
    # --text= 输出第x个初始文本
    # --target= 输出第x个标签
    # --counter 输出每个标签的出现总数量
    opts, args = getopt.getopt(sys.argv[1:], "-h-c-o:", ["help", "count", "json=", "csv=",
                                                         "text=", "target=", "output="])
    for opt_name, opt_value in opts:
        if opt_name in ("-h", "--help"):
            print(r'''Optional parameters:
            python main.py --output <n> / python main.py -o <n>  // Print n-th output
            python main.py --text <n>  // Print n-th text
            python main.py --target <n>  // Print n-th target
            python main.py --csv <fileName>  // Save as csv
            python main.py --json <fileName>  // Save as json
            python main.py --count / python main.py -c  // Print count number for each label.
            ''')
            exit()
        elif opt_name in ("--json",):
            json_file_name = opt_value
            with open(json_file_name, 'a') as f:
                f.write(json.dumps(rst, ensure_ascii=False))
            print("Save as json [%s] successfully." % json_file_name)
        elif opt_name in ("--csv",):
            csv_file_name = opt_value
            output_all_df = pd.DataFrame(columns=["text", "output"])
            output_all_df["text"] = [i["text"] for i in rst]
            output_all_df["output"] = [i["output_list"] for i in rst]
            output_all_df.to_csv(csv_file_name, sep=",", encoding="gbk")
            print("Save as csv [%s] successfully." % csv_file_name)
        elif opt_name in ("--text",):
            n = int(opt_value)
            print("\n第%d个文本\n" % n)
            print(data[n]["input"]["text"])
        elif opt_name in ("--target",):
            n = int(opt_value)
            print("\n第%d个标签\n" % n)
            for tag in data[n]["target"]:
                print(str(tag) + ",")
        elif opt_name in ("--output",):
            n = int(opt_value)
            print("\n第%d个结果\n" % n)
            for output in rst[n]["output_list"]:
                print(output)
        elif opt_name in ("-c", "--count"):
            for k, v in total_counter.items():
                print("[%s]: %d" % (k, v))


def print_segment(segment):
    print("\n")
    for i in segment:
        print(i)
