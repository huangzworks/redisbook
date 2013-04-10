# coding: utf-8

def sinter(*multi_set):

    # 根据集合的基数进行排序
    sorted_multi_set = sorted(multi_set, lambda x, y: len(x) - len(y))

    # 使用基数最小的集合作为基础结果集，有助于降低常数项
    result = sorted_multi_set[0].copy()

    # 剔除所有在 sorted_multi_set[0] 中存在
    # 但在其他某个集合中不存在的元素
    for elem in sorted_multi_set[0]:

        for s in sorted_multi_set[1:]:

            if (not elem in s):
                result.remove(elem)
                break

    return result
