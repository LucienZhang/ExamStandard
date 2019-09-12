from utils import load_file
import sys
import getopt


data = load_file("/users/hk/dev/ExamStandard/data/goldset_93.json")

opts, args = getopt.getopt(sys.argv[1:], "-h", ["text=", "target="])

for opt_name, opt_value in opts:
    if opt_name == "--text":
        print("\n第%s个文本:\n" % opt_value)
        print(data[int(opt_value)]["input"]["text"])
    elif opt_name == "--target":
        print("\n第%s个标签:\n" % opt_value)
        for i in data[int(opt_value)]["target"]:
            print(str(i) + ",")
