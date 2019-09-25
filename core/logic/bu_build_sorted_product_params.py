from core.utils import get_sort_key


def build_sorted_product_params(*unsorted_stacks):
    """
    该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
    :param 排序前的 unsorted_stacks = [ppo_stack, exam_item_stack, exam_result_stack]
    :return: 排序后的 sorted_stacks
    """

    sorted_stacks = []
    for stackOne in unsorted_stacks:
        if len(stackOne) > 0:
            sorted_stacks.append(stackOne)

    sorted_stacks.sort(key=get_sort_key)

    return sorted_stacks
