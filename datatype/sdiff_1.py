# coding: utf-8

def sdiff_1(*multi_set):

    result = multi_set[0].copy()

    sorted_multi_set = sorted(multi_set[1:], lambda x, y: len(x) - len(y))

    # 当 elem 存在于除 multi_set[0] 之外的集合时
    # 将 elem 从 result 中删除
    for elem in multi_set[0]:

        for s in sorted_multi_set:

            if elem in s:
                result.remove(elem)
                break

    return result
