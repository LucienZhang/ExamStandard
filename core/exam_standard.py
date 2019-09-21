from itertools import product
import core.utils as Utils
from core.stacks import *
from core.logic.bu_process_seg_one import process_seg_one
from core.init_stack import stack_dict


class ExamStandardProcessor(object):
    """
    结构化拼接类.
    输入 text: 一个 json 文件
    输出 output_list: 结构化拼接出的结果
    self.data: 需要传递到 process_seg_one函数中
    """

    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.res_seg = []
        self.data = []
        self.output_list = []

    def load_json_file(self):
        abs_file_path = self.file_path + self.file_name
        data = Utils.load_json_file(abs_file_path)
        self.data = data

        return data

    def slice_origin_target(self, idx):
        sliced_targets = Utils.slice_target(self.data[idx]["target"])

        return sliced_targets

    def process_seg_one(self, seg, text):
        """
        该函数用来处理每一个子 seg
        :param seg: slice_targets 中的 每一个子seg
        :param text: 检查报告的 原文本
        :return: res_seg: 用来存储该seg中所有拼接好的结果
        """

        self.res_seg = process_seg_one(seg, text, res_seg=self.res_seg, stack=stack_dict)

        self.output_list.append(self.res_seg)
        self.res_seg = []
