列表 —— List
=================

``REDIS_LIST`` （列表）是 ``LPUSH`` 、 ``LRANGE`` 等命令的操作对象，
它使用 ``REDIS_ENCODING_ZIPLIST`` 和 ``REDIS_ENCODING_LINKEDLIST`` 这两种方式编码：

.. image:: image/redis_list.png

创建新列表时默认使用 ``REDIS_ENCODING_ZIPLIST`` 编码，
当以下任一个条件被满足时，
列表会被转换成 ``REDIS_ENCODING_LINKEDLIST`` 编码：

- 试图往列表新添加一个字符串值，且这个字符串的长度超过 ``server.list_max_ziplist_value`` （默认值为 ``64`` ）。

- ``ziplist`` 本身的长度超过 ``server.list_max_ziplist_entries`` （默认值为 ``512`` ）。

Redis 列表类型命令的实现，
主要是对 ``adlist.c/list`` 和 ``ziplist`` 两种数据结构的操作函数的包装，
以及一些在两种编码之间进行转换的函数，
具体细节可以参考 ``t_list.c`` 模块。

唯一需要谈一下的是列表的阻塞原语（比如 ``BLPOP`` 和 ``BRPOPLPUSH`` ）的实现，
后面会专门有一章讨论这个主题。

.. todo: 添加链接



两种编码
--------------

- ``ziplist`` 

- ``linkedlist``


编码转换
--------------

ZIPLIST -> LINKEDLIST ：

- 字符串值 ``value`` 的长度超过 ``server.list_max_ziplist_value`` 。

- ``ziplist`` 的长度超过 ``server.list_max_ziplist_entries`` 。


阻塞
-------

调用 B[RL]POP/BRPOPLPUSH 命令时，如果列表为空，进行阻塞：

1. 将 key 保存到客户端 c->bpop.keys 字典里

2. 按 key 保存到 c->db->blocking_keys 字典的一个链表里，key 作为字典的键，链表里保存的是所有被这个 key 阻塞的客户端

server.bpop_blocked_clients 记录了当前被阻塞的客户端数量


取消阻塞
----------

在执行 push 时，检查被 push 的 key 是否有客户端因为它而 block 住，
如果有的话，将客户端释放出来，并将 push 进去的值返回给它。

server.readyList 保存一个列表，
以 readyList 结构保存了所有就绪的 key 及 key 的 db 的信息。

client->db->readyList 这个字典也保存了这个 db 所有已经就绪的 key ，
使用字典可以在 O（1） 时间内检查。

Redis 在执行完  call 之后就会调用 handleClienBlockedOnList 
将所有就绪的客户端都处理完。
