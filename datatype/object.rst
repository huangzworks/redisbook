对象处理机制 —— Redis Object
================================


实现
---------

类型

::

    /*
     * 对象类型
     */
    #define REDIS_STRING 0
    #define REDIS_LIST 1
    #define REDIS_SET 2
    #define REDIS_ZSET 3
    #define REDIS_HASH 4

编码

::

    /*
     * 对象编码
     *
     * 像 String 和 Hash 这样的对象，可以有多种内部表示。
     * 对象的 encoding 属性可以设置为以下域的任意一种。
     */
    #define REDIS_ENCODING_RAW 0     /* Raw representation */
    #define REDIS_ENCODING_INT 1     /* Encoded as integer */
    #define REDIS_ENCODING_HT 2      /* Encoded as hash table */
    #define REDIS_ENCODING_ZIPMAP 3  /* Encoded as zipmap */
    #define REDIS_ENCODING_LINKEDLIST 4 /* Encoded as regular linked list */
    #define REDIS_ENCODING_ZIPLIST 5 /* Encoded as ziplist */
    #define REDIS_ENCODING_INTSET 6  /* Encoded as intset */
    #define REDIS_ENCODING_SKIPLIST 7  /* Encoded as skiplist */

对象结构

::

    /*
     * Redis 对象
     */
    typedef struct redisObject {
        unsigned type:4;        // 类型
        unsigned notused:2;     // 不使用(对齐位)
        unsigned encoding:4;    // 编码方式
        unsigned lru:22;        // LRU 时间(相对于 server.lruclock)
        int refcount;           // 引用计数
        void *ptr;              // 对象的实际值
    } robj;

     

note
-------

long 保存为数字
long long 的数字值都保存为字符串

shared 对象用于保存共享对象

类型

REDIS_STRING => sds / long / long long / long double

REDIS_LIST => adlist / ziplist

REDIS_SET => dict(setDictType => dictType) / intset

REDIS_HASH => ziplist

REDIS_ZSET => zset / ziplist

编码

REDIS_ENCODING_INT ==> long 

REDIS_ENCODING_RAW ==> sds / long long / long double

REDIS_ENCODING_LINKEDLIST => adlist

REDIS_ENCODING_ZIPLIST => ziplist

REDIS_ENCODING_HT => dict

REDIS_ENCODING_INTSET => intset

REDIS_ENCODING_ZIPLIST => ziplist

REDIS_ENCODING_SKIPLIST => zset



topic
-----------

对象系统的来源

对象系统的层次结构和实现

对象创建和释放

节约内存的共享对象


question
------------

为什么要有 Redis Object ？它解决了什么问题？


共享对象
---------------

``tryObjectEncoding`` 尝试将一个字符出对象编码为 ``REDIS_ENCODING_INT`` ，如果条件合适的话，就将它加入到 ``shared`` 。
