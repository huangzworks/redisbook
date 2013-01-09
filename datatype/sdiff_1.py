# coding: utf-8

def sdiff_1(*multi_set):

    result = set()

    # 按基数排序集合
    sorted_multi_set = sorted(multi_set, lambda x, y: len(x) - len(y))

    for elem in sorted_multi_set[0]:
        exists = False
        for s in sorted_multi_set[1:]:
            if elem in s:
                exists = True
                break
        # 只有当元素 elem 不存在于其他集合时
        # 才将它加入到结果集
        if not exists: result.add(elem)

    return result
