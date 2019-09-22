from core.handle_funcs.symptom_obj import handle_obj
from core.handle_funcs.object_part import handle_obj_part
from core.handle_funcs.symptom_pos import handle_pos

from core.handle_funcs.exam_item import handle_exam_item
from core.handle_funcs.exam_result import handle_exam_result

from core.handle_funcs.lesion import handle_lesion
from core.handle_funcs.lesion_desc import handle_lesion_desc

from core.handle_funcs.symptom_deco import handle_symptom_deco
from core.handle_funcs.symptom_desc import handle_symptom_desc

from core.handle_funcs.reversed_exam_result import handle_reversed_exam_result
from core.handle_funcs.reversed_exam_item import handle_reversed_exam_item

from core.handle_funcs.treatment import handle_treatment
from core.handle_funcs.treatment_desc import handle_treatment_desc

from core.handle_funcs.exam import handle_exam
from core.handle_funcs.medical_events import handle_medical_events
from core.handle_funcs.time import handle_time
from core.handle_funcs.entity_neg import handle_entity_neg
from core.handle_funcs.vector_seg import handle_vector_seg
from core.handle_funcs.pathogen import handle_pathogen


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

    "reversed_exam_result": handle_reversed_exam_result,
    "reversed_exam_item": handle_reversed_exam_item,

    "treatment": handle_treatment,
    "treatment_desc": handle_treatment_desc,

    "exam": handle_exam,
    "medical_events": handle_medical_events,
    "time": handle_time,
    "entity_neg": handle_entity_neg,
    "vector_seg": handle_vector_seg,
    "pathogen": handle_pathogen
}
