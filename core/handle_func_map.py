from core.logic.handle_obj import handle_obj
from core.logic.handle_exam_result import handle_exam_result
from core.logic.handle_lesion_desc import handle_lesion_desc
from core.logic.handle_pos import handle_pos
from core.logic.handle_exam_item import handle_exam_item


handle_func_map = {
    "symptom_pos": handle_pos,
    "symptom_obj": handle_obj,
    "exam_item": handle_exam_item,
    "exam_result": handle_exam_result,
    "lesion_desc": handle_lesion_desc
}
