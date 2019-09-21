from core.utils import connect_tag_and_value
from core.init_stack import stack_dict
from core.handle_func_map import handle_func_map


def process_seg_one(seg, text, res_seg, stack):
    for j in seg:
        if j[2] == "lesion":
            stack["lesion"].append(j)
            stack["lesion_stack"].append(connect_tag_and_value(j))
            break

    for i in range(len(seg)):
        res_seg, stack = handle_func_map[seg[i][2]](seg, res_seg, i, stack_dict)

    return res_seg
