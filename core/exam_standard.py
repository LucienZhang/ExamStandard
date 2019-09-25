import core.utils as Utils
from core.logic.bu_process_seg_one import process_seg_one
from core.init_stack import init_stack


class ExamStandardProcessor(object):
    """
    结构化拼接类.
    输入 source_json_file_path/name: 输入源json文件, 包含原检查报告text 和标注结果targets.

    res_all: 100个样本结果的总和, 即所有 res_segments 之和
    res_segments: 1个样本中所有seg的结果总和, 即所有 res_seg 之和
    res_seg: 1个seg中所有结果之和
    source_json_data: load_source_json获得的初始数据
    """

    def __init__(self, config):
        self.config = config

    def _slice_origin_target(self, source_data_one):
        """
        :param source_data_one: 即 source_json_data 每一个样本
        source_data_one = {"input":{"text":"双肾大小正常，形态清晰...", "target": [[0,1,obj,双肾],[..],[..]]}
        :return: 切分好的 sliced_targets = [seg1, seg2, seg3]
        """

        sliced_targets = Utils.slice_target(source_data_one["target"])

        return sliced_targets

    def _process_seg_one(self, seg, text):
        """
        该函数用来处理 segment 中的每一个子 seg
        :param seg: slice_targets 中的 每一个子seg
        :param text: 检查报告的 原文本: "双肾大小正常，形态清晰..."
        :return: res_seg: 用来存储该seg中所有拼接好的结果
        """

        stack = init_stack()
        res_seg = process_seg_one(seg, text, stack)

        return res_seg

    def run(self, source_data_one):
        """
        主函数, 处理 source_data 中的每一个样本(即每一个segments)
        :param source_data_one: 即一个 source_data 中的样本
        :return: res_segments
        """

        segments = self._slice_origin_target(source_data_one)
        text = source_data_one["input"]["text"]

        res_segments = []
        for seg in segments:
            res_seg = self._process_seg_one(seg, text)
            res_segments.extend(res_seg)
            res_seg = []

        return res_segments
