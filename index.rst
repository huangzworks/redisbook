.. Redis 设计与实现 documentation master file, created by
   sphinx-quickstart on Fri Dec  7 13:54:33 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Redis 设计与实现
====================


**第一部分：内部数据结构**

.. toctree::
   :maxdepth: 2

   internal-datastruct/sds
   internal-datastruct/adlist
   internal-datastruct/dict
   internal-datastruct/skiplist
   internal-datastruct/compress-datastruct


**第二部分：内存映射数据结构**

intset

ziplist

zipmap


**第三部分：Redis 数据类型**

.. toctree::
   :maxdepth: 2

   datatype/object

字符串 —— t_string

哈希表 —— t_hash

列表 —— t_list

集合 —— t_set

有序集合 —— t_zset


**第四部分：功能的实现**

二进制操作 —— bitop

事务 —— multi

发送与订阅 —— pubsub

Lua 脚本 —— scripting

慢查询报告 —— slowlog

SORT 命令 —— sort


**第五步分：运作机制**

启动与初始化 —— redis

事务处理与多路复用 —— ae

服务端的连接和处理 —— networking

数据库 —— db

持久化 —— rdb & rio

Append Only File 模式 —— aof

同步 —— replication

监视器 —— Sentinel

集群 —— cluster


**附录**

.. toctree::
   :maxdepth: 1

   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
