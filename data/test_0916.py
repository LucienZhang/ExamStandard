samples = {
    0: [
        [148, 148, 'symptom_obj', '血'],
        [150, 152, 'symptom_obj', '软组织'],
        [153, 154, 'exam_item', '本底'],
        [155, 156, 'exam_result', '增高'],
        [25, 26, 'vector_seg', '.']
    ],
    1: [
        # [9, 11, 'symptom_obj', '肾部'],
        [9, 11, 'object_part', '左侧'],
        [9, 11, 'symptom_obj', '头部'],
        [17, 19, 'exam_item', '骨密度'],
        [20, 21, 'exam_result', '均匀'],
        [23, 24, 'exam_item', '颅缝'],
        [25, 26, 'exam_result', '不宽'],
        [25, 26, 'vector_seg', '.']
    ],
    2: [
        [167, 171, 'symptom_obj', '肝内外胆管'],
        [173, 174, 'symptom_obj', '胆囊'],
        [176, 177, 'symptom_obj', '肠道'],
        [165, 166, 'exam_item', '未见'],
        [178, 179, 'exam_result', '显影'],
        [25, 26, 'vector_seg', '.']
    ],
    3: [
        [78, 79, 'symptom_obj', '小脑'],
        [81, 82, 'symptom_obj', '脑干'],
        [83, 84, 'entity_neg', '未见'],
        [85, 86, 'exam_item', '明显'],
        [87, 88, 'exam_result', '异常'],
        [89, 89, 'vector_seg', '，']
    ],
    4: [
        [88, 88, 'symptom_obj', '脾'],
        [89, 90, 'exam_item', '形态'],
        [91, 92, 'exam_item', '大小'],
        [93, 94, 'exam_result', '正常'],
        [96, 97, 'object_part', '包膜'],
        [98, 99, 'entity_neg', '不'],
        [98, 99, 'symptom_desc', '光滑'],
        [128, 128, 'vector_seg', '。']
    ],
    5: [
        [96, 97, 'symptom_obj', '中脑'],
        [99, 100, 'symptom_obj', '桥脑'],
        [102, 103, 'symptom_obj', '延髓'],
        [105, 106, 'symptom_obj', '小脑'],
        [107, 108, 'exam_item', '形态'],
        [110, 111, 'exam_item', '信号'],
        [113, 118, 'exam_result', '未见明显异常'],
        [128, 128, 'vector_seg', '。']
    ],
    6: [
        [30, 31, 'symptom_obj', '气管'],
        [33, 36, 'object_part', '1－3级'],
        [37, 39, 'symptom_obj', '支气管'],
        [40, 41, 'symptom_desc', '通畅'],
        [128, 128, 'vector_seg', '。']
    ],
    7: [
        [64, 65, 'symptom_obj', '胸廓'],
        [66, 67, 'object_part', '骨骼'],
        [69, 70, 'symptom_obj', '胸壁'],
        [71, 73, 'object_part', '软组织'],
        [74, 75, 'entity_neg', '未见'],
        [76, 77, 'symptom_desc', '异常'],
        [78, 78, 'vector_seg', '。'],
    ],
    8: [
        [72, 72, 'object_part', '余'],
        [73, 75, 'symptom_obj', '副鼻窦'],
        [76, 77, 'symptom_desc', '清晰'],
        [79, 80, 'object_part', '窦壁'],
        [81, 82, 'entity_neg', '未见'],
        [83, 86, 'symptom_desc', '骨质破坏'],
        [87, 87, 'vector_seg', '。'],
    ],
    9: [
        [25, 26, 'object_part', '邻近'],
        [27, 27, 'object_part', '诸'],
        [28, 28, 'symptom_obj', '骨'],
        [29, 30, 'entity_neg', '未见'],
        [31, 32, 'symptom_deco', '明显'],
        [33, 36, 'symptom_desc', '骨质异常'],
        [87, 87, 'vector_seg', '。'],
    ],
    10: [
        [43, 43, 'object_part', '余'],
        [44, 45, 'symptom_obj', '脑池'],
        [47, 48, 'symptom_obj', '脑室'],
        [49, 50, 'entity_neg', '未见'],
        [51, 52, 'symptom_desc', '扩大'],
        [54, 55, 'symptom_desc', '闭塞'],
        [56, 56, 'vector_seg', '，'],
    ],
    11: [
        [127, 129, 'symptom_obj', '室间隔'],
        [131, 132, 'symptom_obj', '左室'],
        [133, 134, 'object_part', '后壁'],
        [135, 136, 'exam_item', '厚度'],
        [137, 138, 'exam_result', '正常'],
        [139, 139, 'vector_seg', '，']
    ],
    12: [
        [134, 137, 'symptom_obj', '十二指肠'],
        [139, 140, 'object_part', '球部'],
        [142, 143, 'object_part', '降部'],
        [144, 145, 'entity_neg', '未见'],
        [146, 147, 'symptom_desc', '异常'],
        [148, 148, 'vector_seg', '。'],
    ],
    13: [
        [42, 43, 'symptom_obj', '肝脏'],
        [44, 45, 'exam_item', '大小'],
        [47, 48, 'exam_item', '形态'],
        [49, 50, 'exam_result', '正常'],
        [52, 53, 'exam_item', '表面'],
        [54, 57, 'exam_result', '平整光滑'],
        [59, 60, 'object_part', '实质'],
        [61, 62, 'exam_item', '回声'],
        [63, 65, 'exam_result', '尚均匀'],
        [148, 148, 'vector_seg', '。'],
    ],
    14: [
        [0, 5, 'symptom_obj', '骨盆诸构成骨'],
        [6, 8, 'object_part', '骨皮质'],
        [9, 10, 'symptom_desc', '连续'],
        [12, 13, 'object_part', '骨质'],
        [14, 15, 'exam_item', '信号'],
        [16, 17, 'exam_result', '均匀'],
        [19, 21, 'object_part', '骨髓内'],
        [22, 27, 'reversed_exam_result', '未见明显异常'],
        [28, 30, 'reversed_exam_item', '信号影'],
        [148, 148, 'vector_seg', '。'],
    ],
    15: [
        [52, 53, 'symptom_obj', '椎旁'],
        [54, 56, 'object_part', '软组织'],
        [57, 58, 'entity_neg', '未见'],
        [59, 60, 'symptom_desc', '异常'],
        [62, 63, 'object_part', '韧带'],
        [64, 65, 'entity_neg', '未见'],
        [66, 67, 'symptom_desc', '钙化'],
        [148, 148, 'vector_seg', '。'],
    ],
    16: [
        [26, 27, 'symptom_obj', '肝脏'],
        [28, 29, 'exam_item', '形态'],
        [30, 32, 'exam_result', '无异常'],
        [34, 35, 'exam_item', '轮廓'],
        [36, 37, 'exam_result', '光整'],
        [39, 39, 'symptom_obj', '肝'],
        [40, 42, 'object_part', '实质内'],
        [43, 48, 'reversed_exam_result', '未见明显异常'],
        [49, 50, 'reversed_exam_item', '密度'],
        [148, 148, 'vector_seg', '。'],
    ],
    17: [
        [0, 1, 'symptom_obj', '头颅'],
        [2, 3, 'exam_item', '形态'],
        [4, 5, 'exam_result', '正常'],
        [7, 8, 'symptom_obj', '颅骨'],
        [9, 11, 'object_part', '内外板'],
        [12, 15, 'symptom_desc', '光整连续'],
        [17, 19, 'exam_item', '骨密度'],
        [20, 21, 'exam_result', '均匀'],
        [23, 24, 'exam_item', '颅缝'],
        [25, 26, 'exam_result', '不宽'],
        [28, 29, 'object_part', '蝶鞍'],
        [30, 31, 'exam_item', '形态'],
        [32, 33, 'exam_result', '正常'],
        [35, 36, 'entity_neg', '未见'],
        [37, 40, 'symptom_desc', '骨质破坏'],
        [148, 148, 'vector_seg', '。'],
    ],
    # 以下开始 obj+pos
    18: [
        [64, 74, 'medical_events', '静脉注射示踪剂 1分钟'],
        [77, 77, 'symptom_obj', '心'],
        [79, 79, 'symptom_obj', '肝'],
        [81, 81, 'symptom_pos', '双'],
        [82, 82, 'symptom_obj', '肾'],
        [83, 84, 'reversed_exam_result', '隐约'],
        [85, 86, 'reversed_exam_item', '显影'],
        [87, 87, 'vector_seg', '，'],
    ],
    19: [
        [0, 1, 'symptom_obj', '胸廓'],
        [2, 3, 'symptom_pos', '两侧'],
        [4, 5, 'symptom_deco', '大致'],
        [6, 7, 'symptom_desc', '对称'],
        [87, 87, 'vector_seg', '，'],
    ],
    20: [
        [53, 53, 'symptom_pos', '左'],
        [54, 55, 'symptom_obj', '肱骨'],
        [56, 57, 'symptom_pos', '中段'],
        [58, 59, 'symptom_deco', '骨折'],
        [60, 61, 'symptom_desc', '错位'],
        [63, 64, 'symptom_desc', '分离'],
        [87, 87, 'vector_seg', '，'],
    ],
    21: [
        [69, 75, 'symptom_pos', 'L4、5、S1'],
        [76, 77, 'symptom_obj', '棘突'],
        [78, 79, 'symptom_deco', '可疑'],
        [80, 81, 'symptom_deco', '线状'],
        [82, 84, 'symptom_desc', '透亮影'],
        [87, 87, 'vector_seg', '，'],
    ],
    22: [
        [192, 192, 'symptom_pos', '双'],
        [193, 194, 'symptom_obj', '肾内'],
        [195, 200, 'reversed_exam_result', '未见明显异常'],
        [201, 202, 'reversed_exam_item', '声像'],
        [204, 207, 'exam', 'CDFI'],
        [210, 210, 'symptom_pos', '双'],
        [211, 211, 'symptom_obj', '肾'],
        [212, 215, 'exam_item', '彩色血流'],
        [216, 219, 'exam_result', '分布正常'],
        # [221, 222, 'exam', '频谱'],
        [223, 228, 'exam_result', '未见明显异常'],
        [87, 87, 'vector_seg', '，'],
    ],
    23: [
        [13, 13, 'symptom_pos', '右'],
        [14, 14, 'symptom_obj', '叶'],
        [15, 16, 'exam_item', '体积'],
        [17, 18, 'exam_result', '增大'],
        [21, 21, 'symptom_pos', '内'],
        [22, 26, 'exam_item', '放射性分布'],
        [27, 29, 'exam_result', '不均匀'],
        [87, 87, 'vector_seg', '，'],
    ],
    24: [
[46, 47, 'symptom_obj', '纵隔'],
[48, 49, 'exam_item', '结构'],
[50, 52, 'exam_result', '无偏移'],
[54, 54, 'symptom_pos', '内'],
[55, 56, 'entity_neg', '未见'],
[57, 58, 'symptom_deco', '明显'],
[59, 63, 'symptom_desc', '肿大淋巴结'],
        [87, 87, 'vector_seg', '，'],

    ]
}
