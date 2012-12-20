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


**第二部分：内存映射数据结构**

主要思想：想办法用使用更少的空间来保存数据。

没有免费午餐 —— 用时间换空间 —— 操作复杂，容易出错。

通过更复杂的操作(更多 CPU)，让保存数据所需的内存尽可能地减少(更少的内存)。

.. note::

    使用图示来说明 memory layout !!!!!!!!!!!!!!!!!!!

.. toctree::
   :maxdepth: 2

   compress-datastruct/intset
   compress-datastruct/ziplist
   compress-datastruct/zipmap


**第三部分：Redis 数据类型**

.. toctree::
   :maxdepth: 2

   datatype/object
   datatype/string
   datatype/hash
   datatype/list
   datatype/set
   datatype/sorted_set


**第四部分：功能的实现**

.. toctree::
   :maxdepth: 2

   feature/bitop
   feature/transaction
   feature/pubsub
   feature/scripting
   feature/slowlog
   feature/sort


**第五步分：运作机制**

.. toctree::
   :maxdepth: 2

   internal/redis
   internal/ae
   internal/networking
   internal/db
   internal/persistent
   internal/aof
   internal/replication
   internal/sentinel
   internal/cluster


**附录**

.. toctree::
   :maxdepth: 1

   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
