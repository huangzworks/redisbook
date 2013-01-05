哈希表 —— Hash
=================

``REDIS_HASH`` （哈希表）是 ``HSET`` 、 ``HLEN`` 等命令的操作对象，
它使用 ``REDIS_ENCODING_ZIPLIST`` 和 ``REDIS_ENCODING_HT`` 两种编码方式：

.. image:: image/redis_hash.png

当使用 ``REDIS_ENCODING_ZIPLIST`` 编码时，
哈希表通过将键和值一同推入 ziplist ，
从而形成保存哈希表所需的键-值对结构：

::

    +--------------------+------+------+------+------+------+------+------+------+-------------------+
    | ZIPLIST_ENTRY_HEAD | key1 | val1 | key2 | val2 | ...  | ...  | keyN | valN | ZIPLIST_ENTRY_END |
    +--------------------+------+------+------+------+------+------+------+------+-------------------+

新添加的 key-value 对会被添加到 ziplist 的表尾，
而对 ziplist 中的 key 进行查找/删除的复杂度则为 :math:`O(N)` 。

创建空白哈希表时，
默认使用 ``REDIS_ENCODING_ZIPLIST`` 编码，
当以下任何一个条件被满足时，
哈希表被转换为 ``REDIS_ENCODING_HT`` 编码：

- 键或者值的长度大于 ``server.hash_max_ziplist_value`` （默认值为 ``64`` ）

- ``ziplist`` 中的节点数量大于 ``server.hash_max_ziplist_value`` （默认值为 ``512`` ）

哈希类型命令的实现全都是对字典和 ziplist 操作函数的包装，
以及几个在两种编码之间进行转换的函数，
除此以外，没有其他特别要讲解的地方。
