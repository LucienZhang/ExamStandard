from itertools import product


def get_sort_key_for_build_prod_param(elem):
    if isinstance(elem[0], str):
        # elem = "#0$1&symptom_obj*肾"
        return int(elem[0][elem[0].index("$")+1:elem[0].index("&")])


def _build_sorted_product_params(*unsorted_stacks):
    """
    该函数用来将传入的所有stack, 按照索引，进行先后顺序的排序
    :param 排序前的 unsorted_stacks = [ppo_stack, exam_item_stack, exam_result_stack]
    :return: 排序后的 sorted_stacks
    """

    sorted_stacks = []
    for stackOne in unsorted_stacks:
        if len(stackOne) > 0:
            sorted_stacks.append(stackOne)

    # print(sorted_stacks)
    sorted_stacks.sort(key=get_sort_key_for_build_prod_param)
    # print(list(unsorted_stacks).sort(key=get_sort_key))

    return sorted_stacks


if __name__ == "__main__":
    ppo_stack = ["#0$1&symptom_obj*胸廓"]
    exam_item_stack = ["#25$26&exam_item*边界"]

    exam_result_stack = ["#27$28&exam_result*不清"]

    args = [exam_result_stack, exam_item_stack, ppo_stack]

    product_params = _build_sorted_product_params(*args)
    print("函数外: ", product_params)

    prod_res = list(product(*product_params))
    print("组合后：\n", prod_res)

