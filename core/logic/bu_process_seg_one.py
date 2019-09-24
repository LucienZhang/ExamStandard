from core.utils import connect
from core.handle_func_map import handle_func_map


def process_seg_one(seg, text, stack):
    res_seg = []

    # for j in seg:
    #     if j[2] == "lesion":
    #         stack["lesion_stack"].append(connect(j))
    #         break

    for i in range(len(seg)):
        res_seg, stack = handle_func_map[seg[i][2]](seg, text, res_seg, i, stack)

    return res_seg
