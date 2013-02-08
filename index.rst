.. Redis 设计与实现 documentation master file, created by
   sphinx-quickstart on Fri Dec  7 13:54:33 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Redis 设计与实现
=================================================================


第零部分：阅读须知
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   convention
   

第一部分：内部数据结构
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   internal-datastruct/sds
   internal-datastruct/adlist
   internal-datastruct/dict
   internal-datastruct/skiplist


第二部分：内存映射数据结构
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   compress-datastruct/intset
   compress-datastruct/ziplist


第三部分：Redis 数据类型
-----------------------------------------------------------------

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

.. toctree::
   :maxdepth: 2

   feature/bitop
   feature/transaction
   feature/pubsub
   feature/scripting
   feature/slowlog
   feature/sort


第五步分：内部运作机制
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   internal/redis
   internal/ae
   internal/networking
   internal/db
   internal/rdb
   internal/aof

第六部分：高可用性、容错与集群
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   part-six/replication
   part-six/sentinel
   part-six/cluster


附录
-----------------------------------------------------------------

.. toctree::
   :maxdepth: 1

   internal-module
   reference
