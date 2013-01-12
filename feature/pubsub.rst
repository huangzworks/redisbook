订阅与发送 —— pubsub
==========================

订阅
--------

调用 ``SUBSCRIBE`` 命令时，
将客户端订阅的所有 channel 添加到 ``c->pubsub_channels`` 字典里，
字典的键为 ``channel`` ，
值为 ``NULL`` 。

并将客户端添加到服务器的订阅链表里，
其中 ``server.pubsub_channels`` 为字典，
键为 ``channel`` ，
值为链表，
链表里保存着所有订阅这个 ``channel`` 的客户端。


退订
-----

退订执行的是订阅的反操作。


订阅模式
-----------

1) 将订阅的模式 ``pattern`` 添加到客户端的 ``c->pubsub_patterns`` 链表中。

2) 将包含模式 ``pattern`` 以及客户端 ``client`` 的 ``redis.h/pubsubPattern`` 结构保存到 ``server.pubsub_patterns`` 链表中。


退订模式
----------

退订执行的是订阅的反操作。


发送信息
------------

分为两部分：

1） 根据 ``server.pubsub_channels`` ，将所有信息发送给订阅指定频道的订阅者

2） 根据 ``server.pubsub_patterns`` ，如果给定频道匹配给定模式，那么将信息也发送给这些频道的订阅者。
