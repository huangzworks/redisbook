集合 —— Set
=================

``REDIS_SET`` （集合）是 ``SADD`` 、 ``SRANDMEMBER`` 等命令的操作对象，
它使用 ``REDIS_ENCODING_INTSET`` 和 ``REDIS_ENCODING_HT`` 两种方式编码：

.. image:: image/redis_set.png

第一个添加到集合的元素，决定了集合所使用的编码，
如果该元素可以表示为 ``long long`` 类型值（也即是，它是一个整数），
那么元素的编码为 ``REDIS_ENCODING_INTSET`` ，
否则为 ``REDIS_ENCODING_HT`` 。

如果一个集合使用 ``REDIS_ENCODING_INTSET`` 编码，
那么当以下任何一个条件被满足时，
这个集合会被转换成 ``REDIS_ENCODING_HT`` 编码：

- ``intset`` 保存的整数值个数超过 ``server.set_max_intset_entries`` （默认值为 ``512`` ）

- 试图往集合里添加一个新元素，并且这个元素不能被表示为 ``long long`` 类型（也即是，它不是一个整数）

Redis 集合类型命令的实现，
主要是对 ``intset`` 和 ``dict`` 两个数据结构的操作函数的包装，
以及一些在两种编码之间进行转换的函数，
大部分都没有什么需要解释的地方，
唯一比较有趣的是 ``SINTER`` 、 ``SUNION`` 等命令之下的算法实现，
后面会专门有一章讨论这个主题。

.. todo: 添加链接


----

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
