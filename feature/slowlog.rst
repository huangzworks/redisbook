慢查询报告 —— slowlog
========================

.. warning:: TODO 慢查询的作用，用法，etc 。


慢查询日志
------------------

每条慢查询日志都以一个 ``slowlog.h/slowlogEntry`` 结构定义：

::

    typedef struct slowlogEntry {
        // 命令参数
        robj **argv;
        // 命令参数数量
        int argc;
        // 唯一标识符
        long long id;       /* Unique entry identifier. */
        // 执行命令消耗的时间，以纳秒（1 / 1,000,000,000 秒）为单位
        long long duration; /* Time spent by the query, in nanoseconds. */
        // 命令执行时的时间
        time_t time;        /* Unix time at which the query was executed. */
    } slowlogEntry;

代表服务器的 ``redis.h/redisServer`` 结构里保存了几个和慢查询有关的属性：

::

    struct redisServer {
        // ... other fields
        list *slowlog;                  /* SLOWLOG list of commands */
        long long slowlog_entry_id;     /* SLOWLOG current entry ID */
        long long slowlog_log_slower_than; /* SLOWLOG time limit (to get logged) */
        unsigned long slowlog_max_len;     /* SLOWLOG max number of items logged */
        // ... other fields
    };

``slowlog`` 属性是一个链表，
链表里的每个节点保存了一个慢查询日志结构，
所有日志按添加时间从新到旧排序，新的日志在链表的左端，旧的日志在链表的右端。

``slowlog_entry_id`` 在创建每条新的慢查询日志时增一，用于产生慢查询日志的 ID （这个 ID 在执行 ``SLOWLOG RESET`` 之后会被重置）。

``slowlog_log_slower_than`` 是用户指定的命令执行时间上限，执行时间大于等于这个值的命令会被慢查询日志记录。

``slowlog_max_len`` 慢查询日志的最大数量，当日志数量等于这个值时，添加一条新日志会造成最旧的一条日志被删除。


慢查询日志的记录
--------------------

在每次执行命令之前，
Redis 都会用一个参数记录命令执行前的时间，
在命令执行完之后，
再计算一次当前时间，
然后将两个时间值相减，
得出执行命令所耗费的时间值 ``duration`` ，
并将 ``duration`` 传给 ``slowlogPushEntryIfNeed`` 函数。

如果 ``duration`` 超过服务器设置的执行时间上限 ``server.slowlog_log_slower_than`` 的话，
``slowlogPushEntryIfNeed`` 就会创建一条新的慢查询日志，
并将它加入到慢查询日志链表里。

可以用一段伪代码来表示这个过程：

::

    start = ustime()
    execute_command(argv, argc)
    duration = ustime() - start
    if slowlog_is_enable:
        slowlogPushEntryIfNeed(argv, argc, duration)


慢查询日志的操作
---------------------

针对慢查询日志有三种操作，分别是查看、清空和获取日志数量。

查看分为查看全部和查看给定索引下的日志，
因为多条日志用链表保存，
所以查看操作实际上就是在链表中进行遍历，
这两种查看的复杂度都为 :math:`O(N)` 。

清空日志也即是清空保存日志的链表及其节点，
复杂度为 :math:`O(N)` 。

获取日志的长度也即是获取日志链表的长度，
复杂度为 :math:`O(1)` 。
