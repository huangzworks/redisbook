.. _string_chapter:

字符串
====================

``REDIS_STRING`` （字符串）是 Redis 使用得最为广泛的数据类型，
它除了是 ``SET`` 、 ``GET`` 等命令的操作对象之外，
数据库中的所有键，
以及执行命令时提供给 Redis 的参数，
都是用这种类型保存的。


字符串编码
-------------

字符串类型分别使用 ``REDIS_ENCODING_INT`` 和 ``REDIS_ENCODING_RAW`` 两种编码：

- ``REDIS_ENCODING_INT`` 使用 ``long`` 类型来保存 ``long`` 类型值。
- ``REDIS_ENCODING_RAW`` 则使用 ``sdshdr`` 结构来保存 ``sds`` （也即是 ``char*`` )、 ``long long`` 、 ``double`` 和 ``long double`` 类型值。

换句话来说，
在 Redis 中，
只有能表示为 ``long`` 类型的值，
才会以整数的形式保存，
其他类型的整数、小数和字符串，
都是用 ``sdshdr`` 结构来保存。

.. graphviz:: image/redis_string.dot


编码的选择
-----------------------

新创建的字符串默认使用 ``REDIS_ENCODING_RAW`` 编码，
在将字符串作为键或者值保存进数据库时，
程序会尝试将字符串转为 ``REDIS_ENCODING_INT`` 编码。


字符串命令的实现
----------------------

Redis 的字符串类型命令，
基本上是通过包装 ``sds`` 数据结构的操作函数来实现的，
没有什么需要说明的地方。
