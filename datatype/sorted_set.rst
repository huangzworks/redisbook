有序集 —— SortedSet
========================

``REDIS_ZSET`` （有序集）是 ``ZADD`` 、 ``ZCOUNT`` 等命令的操作对象，
它使用 ``REDIS_ENCODING_ZIPLIST`` 和 ``REDIS_ENCODING_SKIPLIST`` 两种方式编码：

.. image:: image/redis_zset.png

TODO: 介绍有序集使用两个数据结构的原因，以及并集、交集的实现算法


---

两种编码：

- ``REDIS_ENCODING_ZIPLIST`` ： 用 ziplist 保存有序集合

- ``REDIS_ENCODING_SKIPLIST`` ：用 skiplist 保存有序集合

转码条件：

-  ``server.zset_max_ziplist_entries == 0`` 。

- 元素的 ``member`` 长度大于 ``server.zset_max_ziplist_value`` 。


