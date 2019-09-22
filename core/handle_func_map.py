from core.handle_funcs.symptom_obj import handle_obj
from core.handle_funcs.object_part import handle_obj_part
from core.handle_funcs.symptom_pos import handle_pos

from core.handle_funcs.exam_item import handle_exam_item
from core.handle_funcs.exam_result import handle_exam_result

from core.handle_funcs.lesion import handle_lesion
from core.handle_funcs.lesion_desc import handle_lesion_desc

from core.handle_funcs.symptom_deco import handle_symptom_deco
from core.handle_funcs.symptom_desc import handle_symptom_desc

from core.handle_funcs.entity_neg import handle_entity_neg


handle_func_map = {
    "symptom_pos": handle_pos,
    "symptom_obj": handle_obj,
    "object_part": handle_obj_part,

    "exam_item": handle_exam_item,
    "exam_result": handle_exam_result,

    "lesion": handle_lesion,
    "lesion_desc": handle_lesion_desc,

    "symptom_deco": handle_symptom_deco,
    "symptom_desc": handle_symptom_desc,

    "entity_neg": handle_entity_neg
}
