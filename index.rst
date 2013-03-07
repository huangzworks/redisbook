.. Redis 设计与实现 documentation master file, created by
   sphinx-quickstart on Fri Dec  7 13:54:33 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Redis 设计与实现
=================================================================


第 0 部分：内部数据结构
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   internal-datastruct/sds
   internal-datastruct/adlist
   internal-datastruct/dict
   internal-datastruct/skiplist


第 1 部分：内存映射数据结构
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   compress-datastruct/intset
   compress-datastruct/ziplist


第 2 部分：Redis 数据类型
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   datatype/object
   datatype/string
   datatype/hash
   datatype/list
   datatype/set
   datatype/sorted_set


第 3 部分：功能的实现
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   feature/transaction
   feature/pubsub
   feature/scripting
   feature/slowlog

..   feature/bitop
..   feature/sort


第 4 部分：内部运作机制
-----------------------------------------------------------------

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
