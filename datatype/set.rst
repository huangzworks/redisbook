集合 —— Set
=================

两种编码方式：

- ``REDIS_ENCODING_HT`` ：用字典表示集合，元素保存为字典的 ``key`` ，值为 ``NULL`` 。

- ``REDIS_ENCODING_INTSET`` ：用 intset 表示集合。

创建规则
-----------

创建 set 对象是，默认使用 intset 。

调用 SADD 等命令时，根据输入值，选择是使用 intset （值可以保存为 ``long`` ？）
或者字典（sds/double/long...）

转换规则
---------------

intset -> dict 转换的规则： 

- intset 的实体数量超过 ``server.set_max_intset_entries`` 。

- 新添加的元素不能表示为 ``long long`` 类型。


看点
------

SINTER 、 SUNION 等命令的实现算法蛮有趣的。
