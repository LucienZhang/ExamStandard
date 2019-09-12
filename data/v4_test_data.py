"""
测试数据分4种情况 (不分前后顺序)
1 = obj
2 = obj + part
3 = pos + obj
4 = pos+ obj + part

v4_test_data = {
    "obj": {
        "1": [],
        "2": []
    },

    "obj_part": {
        "1": [],
        "2": []
    },

    "pos_obj": {
        "1": [],
        "2": []
    },

    "pos_obj_part": {
        "1": [],
        "2": []
    }
}
"""

type_map = ["obj", "obj_part", "pos_obj", "pos_obj_part"]

v4_test_data = {
    "obj": {
        # 单个obj
        "1": [
            [46, 47, 'symptom_obj', '纵隔'],
            [48, 49, 'exam_item', '结构'],
            [50, 52, 'exam_result', '无偏移'],
            [99, 99, 'vector_seg', '，']
        ],
        # 多个连续obj
        "2": [
            [54, 55, 'symptom_obj', '脑池'],
            [57, 58, 'symptom_obj', '脑沟'],
            [59, 59, 'entity_neg', '无'],
            [60, 61, 'symptom_desc', '增宽']
        ]
    }

}
