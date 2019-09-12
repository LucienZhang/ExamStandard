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
            [99, 99, 'vector_seg', '，'],

            [46, 47, 'symptom_obj', '肾脏'],
            [48, 49, 'exam_item', '大小'],
            [50, 52, 'exam_result', '正常'],
            [99, 99, 'vector_seg', '，']
        ],
        # 多个连续并列obj
        "2": [
            [54, 55, 'symptom_obj', '脑池'],
            [57, 58, 'symptom_obj', '脑沟'],
            [48, 49, 'exam_item', '结构'],
            [50, 52, 'exam_result', '正常'],
            [99, 99, 'vector_seg', '，']
        ],
        # 并列obj
        "3": [
            [46, 47, 'symptom_obj', '纵隔'],
            [57, 58, 'symptom_obj', '气管'],
            [48, 49, 'exam_item', '结构'],
            [50, 52, 'exam_result', '无偏移'],
            [99, 99, 'vector_seg', '，']
        ],
        # 这种也可以正常输出
        "4": [
            [165, 166, 'exam_item', '大小'],
            [167, 171, 'symptom_obj', '肝内外胆管'],
            [173, 174, 'symptom_obj', '胆囊'],
            [176, 177, 'symptom_obj', '肠道'],
            [178, 179, 'exam_result', '正常'],
            [180, 180, 'vector_seg', '，']
        ]
    },
    "obj_part": {},
    "pos_obj": {
        # pos + obj
        "1": [
            [85, 85, 'symptom_pos', '双'],
            [86, 86, 'symptom_obj', '肾'],
            [87, 88, 'exam_item', '大小'],
            [89, 90, 'exam_result', '正常'],
            [99, 99, 'vector_seg', '，']
        ],
        # obj + pos
        "2": [
            [86, 86, 'symptom_obj', '肾'],
            [85, 85, 'symptom_pos', '右侧'],
            [87, 88, 'exam_item', '大小'],
            [89, 90, 'exam_result', '正常'],
            [99, 99, 'vector_seg', '，']
        ],
        "3": [
            [81, 81, 'symptom_obj', '心'],
            [83, 83, 'symptom_obj', '肝'],
            [85, 85, 'symptom_pos', '双'],
            [86, 86, 'symptom_obj', '肾'],
            [87, 88, 'exam_item', '大小'],
            [89, 90, 'exam_result', '正常'],
        ]
    }

}
