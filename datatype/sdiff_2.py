# coding: utf-8

def sdiff_2(*multi_set):
    # 用第一个集合作为结果集的起始值
    result = multi_set[0].copy()

    for s in multi_set[1:]:
        for elem in s:
            # 从结果集中删去其他集合中包含的元素
            if elem in result:
                result.remove(elem)

    return result
