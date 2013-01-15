持久化 —— rdb & rio
========================

预备知识：

http://redis.io/topics/persistence

文章的 RDB 部分。


TODO 要点
------------

1. 各个类型的编码方式

2. Save 和 Load 两个动作

3. save 和 bgsave 的实现，子进程进行的动作

.. image:: image/persistent.png


rio
---------

创建了一套既通用接口，
可以用于处理字节数组和文件。


写入 RDB 文件的过程
-------------------------

伪代码

::

    f = open(...)
    for db in all_db_in_server:
        write(f, db_number)
        for key-value-pair in db:
            if key has expire time:
                write(f, expire_time_of_key)
            write(key)
            write(value)


rdb 文件的结构
-------------------

::

    | REDIS | RDB_VERSION | DB_NUMBER | KEY-VALUE-PAIRS | EOF | CHECK_SUM |


**REDIS**

字符串 "REDIS"

**RDB_VERSION**

一个四字节长的字符串，
保存了 RDB 的版本号
（不同版本之间互不兼容）。

**DB_NUMBER**

记录被保存的数据库号码，可以分为以下两部分：

::

    | DB_IDENTITY | DB_NUMBER |

``DB_IDENTITY`` ：数据库号码标识符，标记后跟的数字为数据库号码。长度为 1 个字节，值为 ``rdb.h/REDIS_RDB_OPCODE_SELECTDB`` （\ ``254``\ ）

``DB_NUMBER`` ：数据库号码， rdbSaveLen 编码，因为数据库数量通常比较少，通常可以用一个字节来保存（包括长度标识和长度值）

**KEY-VALUE-PAIRS**

保存键-值对，以及可能有的过期时间。

**EOF**

标志着数据库内容的结尾（不是文件的结尾），值为 ``rdb.h/EDIS_RDB_OPCODE_EOF`` （\ ``255``\ ）。

**CHECK_SUM**

前文以上所有内容的校验和，
一个 ``uint_64t`` 类型值，
如果为 ``0`` ，
那么表示校验和已关闭，
如果不为 ``0`` ，
那么 REDIS 在写入时将校验和保存在 RDB 文件，
当读取时，根据它对正文内容进行校验。


KEY-VALUE-PAIRS 结构
---------------------------

::

    | OPTIONAL-EXPIRE-TIME | TYPE-OF-VALUE | KEY | VALUE |

1. 可选的过期时间

2. 值（对象）的类型

3. 键

4. 值


OPTIONAL-EXPIRE-TIME
----------------------

::

    | TYPE | TIME |

type
^^^^^^

1 字节长，

可以用毫秒或者秒计算，
分别用 ``rdb.h/REDIS_RDB_OPCODE_EXPIRETIME_MS`` （\ ``252``\ ）和
``rdb.h/REDIS_RDB_OPCODE_EXPIRETIME`` （\ ``253``\ ）标记。

time
^^^^^

一个 ``int64_t`` 类型值，过期时间以毫秒计算。

如果类型是秒，那么会根据这个值计算出秒。


TYPE-OF-VALUE
-----------------

1 字节长，标识了值的类型，可以是 ``rdb.h`` 中的以下任何一个常量

::

    /* Dup object types to RDB object types. Only reason is readability (are we
     * dealing with RDB types or with in-memory object types?).
     *
     * 对象类型在 RDB 文件中的类型
     */
    #define REDIS_RDB_TYPE_STRING 0
    #define REDIS_RDB_TYPE_LIST   1
    #define REDIS_RDB_TYPE_SET    2
    #define REDIS_RDB_TYPE_ZSET   3
    #define REDIS_RDB_TYPE_HASH   4

    /* Object types for encoded objects. */
    /*
     * 编码对象的方式
     */
    #define REDIS_RDB_TYPE_HASH_ZIPMAP    9
    #define REDIS_RDB_TYPE_LIST_ZIPLIST  10
    #define REDIS_RDB_TYPE_SET_INTSET    11
    #define REDIS_RDB_TYPE_ZSET_ZIPLIST  12
    #define REDIS_RDB_TYPE_HASH_ZIPLIST  13


KEY
------

一个字符串，
保存的可能是字符串，
也可能是整数，
长度根据值而不等。

如果是整数的话，
在保存时会尝试将它进行特殊编码。

如果是字符串的话，
尝试使用 LZF 算法对它进行压缩，
然后将它保存到 rdb 中（压缩成功就用压缩之后的值，不成功就用原值）。


VALUE
-------

根据值类型的不同，
保存的方式和长度也不同。

字符串
^^^^^^^^

保存的形式和 ``KEY`` 一样。

ziplist 编码的列表
^^^^^^^^^^^^^^^^^^^^^^^

整个 ziplist 保存为一个字符串。

双端链表编码的列表
^^^^^^^^^^^^^^^^^^^^

::

    for node in list:
        write(rdb, node.value, len(node.value))

其中节点的值（\ ``node.value``\ ）也是一个字符串，
保存的形式和 ``KEY`` 一样。

ziplist 编码的哈希
^^^^^^^^^^^^^^^^^^^^^^

整个 ziplist 保存为一个字符串。

字典编码的哈希
^^^^^^^^^^^^^^^^^

::

    for entry in dict:
        write(rdb, entry.key, len(entry.key))
        write(rdb, entry.value, len(entry.value))

其中的 ``key`` 和 ``value`` 都是字符串，
保存的形式和 ``KEY`` 一样。

intset 编码的集合
^^^^^^^^^^^^^^^^^^^^^^

整个 intset 保存为一个字符串。

字典编码的集合
^^^^^^^^^^^^^^^^^

::

    for entry in dict:
        write(rdb, entry.key, len(entry.key))

集合只使用字典的 ``key`` 来保存成员， ``value`` 都是 ``NULL`` ，因此只保存 ``key`` 就可以了。
``key`` 的保存形式和 ``KEY`` 一样。


ziplist 编码的有序集
^^^^^^^^^^^^^^^^^^^^^^^^

整个 ziplist 保存为一个字符串。

zset 编码的有序集
^^^^^^^^^^^^^^^^^^^

zset 同时使用了跳跃表和字典，
任意一个数据结构都可以取出所有元素，
这里 Redis 选择了使用字典。

::

    for entry in dict:
        write(db, entry.key)    // key as member
        write(db, entry.value)  // value as score

两种写入
-----------

- 阻塞写

- 后台写（fork 子进程）
