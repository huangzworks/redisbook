同步 —— replication
=====================


SYNC 命令
--------------

步骤：

1. 主节点执行 BGSAVE ，创建一个代表当前数据库状态的 .rdb 文件，并且在此期间，将新进入的命令请求缓存起来。

2. 将 .rdb 文件发送给附属节点，附属节点根据 .rdb 还原主节点的数据库

3. 主节点将从创建 .rdb 开始，到现在为止所缓存的所有命令请求传送给附属节点（到这一步，主节点和附属节点的数据已经一样了）

4. 每次当主节点接到一个新的写请求命令时，将命令转发给附属节点（保持同步）


updateSlaveWaitingBgsave
------------------------------

BGSAVE 每次执行完之后都会检查是否有附属节点在等待 BGSAVE 完成，如果有的话，就会调用 ``updateSlaveWaitingBgsave`` 函数。


附属节点的状态
--------------------

``redis.h/redisClient.replstate`` 属性的值指示了同步进行的状态：

- ``REDIS_REPL_WAIT_BGSAVE_START`` ：等待 BGSAVE 开始

- ``REDIS_REPL_WAIT_BGSAVE_END`` ：BGSAVE 已完成

- ``REDIS_REPL_SEND_BULK`` ：将 .rdb 文件发送到附属节点

- ``REDIS_REPL_ONLINE`` ： .rdb 文件发送完成，同步开始


命令的同步
------------

``redis.c/call`` 执行之后会调用 ``redis.c/propagate`` ，
``propagate`` 会调用 ``replication.c/replicationFeedSlaves`` ，
并将命令、命令参数、参数数量、数据库 ID 和包含所有附属节点的链表发送给它。

``replicationFeedSlaves`` 
