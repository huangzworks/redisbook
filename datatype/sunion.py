# coding: utf-8

def sunion(*multi_set):

    result = set()

    for s in multi_set:
        for elem in s:
            # 重复的元素会被自动忽略
            result.add(elem)

    return result
