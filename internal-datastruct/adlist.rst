双端链表 —— Adlist
========================

链表作为数组之外的一种有序序列抽象，是大多数高级语言的基本数据类型，但是，因为 C 语言本身并不支持链表类型，因此，大部分 C 程序都会实现自己版本的链表，Redis 也不例外。

双端链表作为一种通用的数据结构，在 Redis 的实现中使用得非常多：它既是 Redis 列表结构的底层实现，还被大量 Redis 模块所使用，用于构建 Redis 的其他功能。

**实现 Redis 的列表类型**

Redis 的列表类型在底层操作的就是双端列表：所有处理列表的操作，比如 ``LPUSH`` 、 ``LPOP`` 、 ``LLEN`` ，等等，在底层操作的都是双端链表。

::

    redis 127.0.0.1:6379> LPUSH company apple microsoft google  // 将给定的三个元素保存到链表
    (integer) 3

    redis 127.0.0.1:6379> LPOP company                          // 移除链表的表尾元素
    "google"

    redis 127.0.0.1:6379> LLEN company                          // 计算链表的元素数量
    (integer) 2

**Redis 自身功能的构建**

除了实现列表类型以外，双端链表用在很多其他模块中：

* 事务模块使用双端链表来按顺序保存输入的命令

* 服务器模块使用双端链表来保存多个客户端

* 订阅/发送模块使用双端链表来保存订阅模式的多个客户端

* 事件模块使用双端链表来保存时间事件(time event)

类似的应用还有很多，在后续的内容中，我们会多次见到双端链表是如何在  Redis 模块的实现中发挥作用的。


关于双端链表
----------------------

链表/双端链表作为一种常见的数据结构，在大部分的数据结构或者算法书里都有讲解，因此，这一章的内容关注的是 Redis 的双端链表的具体实现，以及它的 API ，而对于双端链表本身，以及双端链表所对应的算法，就不做太多的解释。

读者如果有需要的话，可以参考维基百科的\ `双端链表 <http://en.wikipedia.org/wiki/Doubly_linked_list>`_\ 词条，里面提供了关于双端链表的一些基本信息。

另外，一些书籍，比如\ `《算法：C 语言实现》 <http://book.douban.com/subject/4065258/>`_\ 和\ `《数据结构与算法分析》 <http://book.douban.com/subject/1139426/>`_\ 则提供了关于双端链表的更详细的信息。

双端链表的实现
-----------------

双端链表的实现由 ``listNode`` 和 ``list`` 两个数据结构构成。

其中， ``listNode`` 是双端链表的节点：

::

    /*
     * 链表节点
     */
    typedef struct listNode {
        struct listNode *prev;  // 前驱节点
        struct listNode *next;  // 后继节点
        void *value;            // 值
    } listNode;


而 ``list`` 则是双端链表本身：

::

    /*
     * 链表
     */
    typedef struct list {
        listNode *head;                         // 表头指针
        listNode *tail;                         // 表尾指针
        void *(*dup)(void *ptr);                // 复制函数
        void (*free)(void *ptr);                // 释放函数
        int (*match)(void *ptr, void *key);     // 比对函数
        unsigned long len;                      // 节点数量
    } list;

注意， ``listNode`` 的 ``value`` 属性的类型是 ``void *`` ，说明这个双端链表对节点所保存的值的类型不做限制。

对于不同类型的值，有时候需要不同的函数来处理这些值，因此， ``list`` 类型保留了三个函数指针 —— ``dup`` 、 ``free`` 和 ``match`` ，分别用于处理值的复制、释放和对比匹配。在对节点的值进行处理时，如果有给定这些函数，那么它们就会被调用。

举个例子：当删除一个 ``listNode`` 时，如果包含这个节点的 ``list`` 的 ``list->free`` 函数不为空，那么删除函数就会先调用 ``list->free(listNode->value)`` 清空节点的值，再执行余下的删除操作（比如说，释放节点）。

另外，从这两个数据结构的定义上，也可以看出一些 Redis 列表的属性：

- ``listNode`` 带有 ``prev`` 和 ``next`` ，因此对列表的遍历可以在两个方向上进行：从表头到表尾，或者从表尾到表头。

- ``list`` 保存了 ``head`` 和 ``tail`` 两个指针，因此，对列表的表头和表尾进行插入的复杂度都为 :math:`\theta(1)` ，这是高效实现 ``LPUSH/RPUSH`` 、 ``LPOP/RPOP`` 、 ``RPOPLPUSH`` 等命令的关键。

- ``list`` 带有保存节点数量的 ``len`` 属性，所以计算链表长度的复杂度仅为 :math:`\theta(1)` ，这也保证了 ``LLEN`` 命令不会成为性能瓶颈。


双端链表 API
----------------

TODO


迭代器
---------

TODO


迭代器 API
--------------

TODO
