哈希表 —— Hash
=================

两种编码方式：

- ``REDIS_ENCODING_ZIPLIST`` ：用 ziplist 保存映射

- ``REDIS_ENCODING_HT`` ：用字典保存映射

Ziplist -> dict 转换的规则：

- 键或者值的长度大于 ``server.hash_max_ziplist_value``

- ``ziplist`` 的映射数量大于 ``server.hash_max_ziplist_entries`` 
