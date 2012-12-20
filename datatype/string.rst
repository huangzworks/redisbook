字符串 —— String
====================

字符串的操作都是对 sds 数据结构操作的包装，没有什么需要讲的。

两种编码方式：

- ``REDIS_ENCODING_RAW`` ，将 ``sds`` （\ ``char*``\ ）、 ``long long`` 和 ``long double`` （Redis 字符串输入的浮点数都以这种类型表示）类型的值全部以 ``sds`` 类型保存。

- ``REDIS_ENCODING_INT`` ，将 ``long`` 类型的值以 ``long`` 类型来保存。
