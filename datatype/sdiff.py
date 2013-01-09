# coding: utf-8

from sdiff_1 import sdiff_1
from sdiff_2 import sdiff_2

def sdiff(*multi_set):

    algo_one_advantage = 2 # 算法一的常数项较低，给它一点额外的优先级
    algo_one_weight = len(multi_set[0]) * len(multi_set[1:]) / algo_one_advantage

    algo_two_weight = sum(map(len, multi_set))

    if algo_one_weight <= algo_two_weight:
        return sdiff_1(*multi_set)
    else:
        return sdiff_2(*multi_set)
