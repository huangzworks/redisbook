.. Redis 设计与实现 documentation master file, created by
   sphinx-quickstart on Fri Dec  7 13:54:33 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Redis 设计与实现（第一版）
=================================================================

.. warning::

    你正在阅读的是《Redis 设计与实现》第一版，
    查看新版《Redis 设计与实现》的相关信息请访问 `redisbook1e.rtfd.org <http://redisbook1e.rtfd.org/>`_ 。

本书的目标是以简明易懂的方式讲解 Redis 的内部运行机制，
通过阅读本书，
你可以了解到 Redis 从数据结构到服务器构造在内的几乎所有知识。

.. image:: redis-logo-small.png
   :align: left
   :width: 454px
   :height: 151px
   :scale: 55%

为了保证内容的简洁性，
本书会尽量以高抽象层次的角度来观察 Redis ，
并将代码的细节留给读者自己去考究。

如果读者只是对 Redis 的内部运作机制感兴趣，
但并不想深入代码，
那么只阅读本书就足够了。

另一方面，
对于需要深入研究 Redis 代码的读者，
本书附带了一份 `带有详细注释的 Redis 2.6 源代码 <https://github.com/huangz1990/annotated_redis_source>`_ ，
可以配合本书一并使用。


第一部分：内部数据结构
-----------------------------------------------------------------

Redis 和其他很多 key-value 数据库的不同之处在于，
Redis 不仅支持简单的字符串键值对，
它还提供了一系列数据结构类型值，
比如列表、哈希、集合和有序集，
并在这些数据结构类型上定义了一套强大的 API 。

通过对不同类型的值进行操作，
Redis 可以很轻易地完成其他只支持字符串键值对的 key-value 数据库很难（或者无法）完成的任务。

在 Redis 的内部，
数据结构类型值由高效的数据结构和算法进行支持，
并且在 Redis 自身的构建当中，
也大量用到了这些数据结构。

这一部分将对 Redis 内存所使用的数据结构和算法进行介绍。

.. toctree::
   :maxdepth: 2

   internal-datastruct/sds
   internal-datastruct/adlist
   internal-datastruct/dict
   internal-datastruct/skiplist


第二部分：内存映射数据结构
-----------------------------------------------------------------

虽然内部数据结构非常强大，
但是创建一系列完整的数据结构本身也是一件相当耗费内存的工作，
当一个对象包含的元素数量并不多，
或者元素本身的体积并不大时，
使用代价高昂的内部数据结构并不是最好的办法。

为了解决这一问题，
Redis 在条件允许的情况下，
会使用内存映射数据结构来代替内部数据结构。

内存映射数据结构是一系列经过特殊编码的字节序列，
创建它们所消耗的内存通常比作用类似的内部数据结构要少得多，
如果使用得当，
内存映射数据结构可以为用户节省大量的内存。

不过，
因为内存映射数据结构的编码和操作方式要比内部数据结构要复杂得多，
所以内存映射数据结构所占用的 CPU 时间会比作用类似的内部数据结构要多。

这一部分将对 Redis 目前正在使用的两种内存映射数据结构进行介绍。

.. toctree::
   :maxdepth: 2

   compress-datastruct/intset
   compress-datastruct/ziplist


第三部分：Redis 数据类型
-----------------------------------------------------------------

既然 Redis 的键值对可以保存不同类型的值，
那么很自然就需要对键值的类型进行检查以及多态处理。

为了让基于类型的操作更加方便地执行，
Redis 创建了自己的类型系统。

在这一部分，
我们将对 Redis 所使用的对象系统进行了解，
并分别观察字符串、哈希表、列表、集合和有序集类型的底层实现。

.. toctree::
   :maxdepth: 2

   datatype/object
   datatype/string
   datatype/hash
   datatype/list
   datatype/set
   datatype/sorted_set


第四部分：功能的实现
-----------------------------------------------------------------

除了针对单个键值对的操作外，
Redis 还提供了一些同时对多个键值对进行处理的功能，
比如事务和 Lua 脚本。

另外，
一些辅助性的功能，
比如慢查询，
以及一些和数据库无关的功能，
比如订阅与发布，
我们也会经常用到。

通过理解这些功能的底层实现，
我们可以更有效地使用它们。

这一部分将对这些功能进行介绍。

.. toctree::
   :maxdepth: 2

   feature/transaction
   feature/pubsub
   feature/scripting
   feature/slowlog

..   feature/bitop
..   feature/sort


第五部分：内部运作机制
-----------------------------------------------------------------

以下章节将对 Redis 最底层也最隐蔽的模块进行探讨：

- Redis 如何表示一个数据库？数据库操作是如何实现的？

- Redis 如何进行持久化？ RDB 模式和 AOF 模式有什么区别？

- Redis 如何处理输入命令？它又是如何将输出返回给客户端的？

- Redis 服务器如何初始化？传入服务器的命令又是以什么方法执行的？

以上的这些问题，都是这一部分要解答的。

.. toctree::
   :maxdepth: 2

   internal/db
   internal/rdb
   internal/aof
   internal/ae
   internal/redis

..   internal/networking

.. 第六部分：高可用性、容错与集群
   -----------------------------------------------------------------
   .. toctree::
      :maxdepth: 2
      part-six/replication
      part-six/sentinel
      part-six/cluster


关于
-------------------

本书由 `huangz <http://huangz.me/>`_ 编写。

我在研究 Redis 源码并创作本书的过程中获得了极大的快乐，希望你在阅读本书时也能有同感。

评论、问题、意见或建议都可以发表在本书自带的 disqus 论坛里，
也可以通过 `豆瓣 <http://www.douban.com/people/i_m_huangz/>`_ 、 `微博 <http://weibo.com/huangz1990>`_ 或 `Twitter <https://twitter.com/huangz1990>`_ 联系我，
我会尽可能地回复。

要获得本书的最新动态，请关注 `redisbook <https://github.com/huangz1990/redisbook>`_ 项目。

要了解编写本书时用到的工具（源码管理、文档的生成和托管、图片生成，等等），请阅读 `这篇文章 <http://blog.huangz.me/en/latest/diary/2013/tools-for-writing-redisbook.html>`_ 。

下载本书离线版本： `pdf 格式 <https://github.com/huangz1990/redisbook/raw/master/pdf/redisbook.pdf>`_ 或 `html 格式 <https://media.readthedocs.org/htmlzip/redisbook/latest/redisbook.zip>`_ 。


通过捐款支持本书
-------------------

如果你喜欢这本《Redis 设计与实现》的话，
可以通过捐款的方式，
支持作者继续更新本书：
比如为本书修补漏洞、添加更多有趣的章节，
或者发行有更多更棒内容的下一版，
等等。

捐款地址： https://me.alipay.com/huangz
