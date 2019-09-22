import core.utils as Utils
from core.logic.bu_process_seg_one import process_seg_one
from core.init_stack import init_stack


class ExamStandardProcessor(object):
    """
    结构化拼接类.
    输入 source_json_file_path/name: 输入源json文件, 包含原检查报告和标注结果
    输出 all_result: 结构化拼接出的结果

    self.res_all: 100个样本结果的总和, 即所有 res_segments 之和
    self.res_segments: 1个样本中所有seg的结果总和, 即所有 res_seg 之和
    self.res_seg: 1个seg中所有结果之和
    self.data: load_source_json获得的初始数据, 需要传递到 process_seg_one函数中
    """

    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.data = []
        self.res_seg = []
        self.res_segments = []
        self.res_all = []

    def load_source_json_file(self):
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

        stack = init_stack()
        self.res_seg = process_seg_one(seg, text, res_seg=self.res_seg, stack=stack)

        self.res_segments.append(self.res_seg)
        self.res_seg = []

    def put_res_segments_to_res_all(self, data_idx):
        """
        该方法用来将100个样本中的每一个结果 res_segments，汇总到总结果 res_all 中
        :param data_idx: 该参数的取值范围, 就是 source_json_file 中的样本数量(100左右)
        """

        self.res_all.append(
            {data_idx: self.res_segments}
        )

        self.res_segments = []

    def save_res_all_to_json(self, result_save_path, result_save_name):
        Utils.save_all_result_to_json(self.data, self.res_all, result_save_path, result_save_name)