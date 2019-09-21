from core.handle_funcs.handle_obj import handle_obj
from core.handle_funcs.handle_exam_result import handle_exam_result
from core.handle_funcs.handle_lesion_desc import handle_lesion_desc
from core.handle_funcs.handle_pos import handle_pos
from core.handle_funcs.handle_exam_item import handle_exam_item
from core.handle_funcs.handle_object_part import handle_obj_part
from core.handle_funcs.handle_lesion import handle_lesion


handle_func_map = {
    "symptom_pos": handle_pos,
    "symptom_obj": handle_obj,
    "object_part": handle_obj_part,
    "exam_item": handle_exam_item,
    "exam_result": handle_exam_result,
    "lesion": handle_lesion,
    "lesion_desc": handle_lesion_desc
}
