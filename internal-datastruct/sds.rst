简单动态字符串
===========================================

Sds （Simple Dynamic String，简单动态字符串）是 Redis 底层所使用的字符串表示，
几乎所有的 Redis 模块中都用了 sds。

本章将对 sds 的实现、性能和功能等方面进行介绍，
并说明 Redis 使用 sds 而不是传统 C 字符串的原因。

sds 的用途
-----------------

Sds 在 Redis 中的主要作用有以下两个：

1. 实现字符串对象（StringObject）；

2. 在 Redis 程序内部用作 ``char*`` 类型的替代品；

以下两个小节分别对这两种用途进行介绍。

实现字符串对象
^^^^^^^^^^^^^^^^^^^

Redis 是一个键值对数据库（key-value DB），
数据库的值可以是字符串、集合、列表等多种类型的对象，
而数据库的键则总是字符串对象。

对于那些包含字符串值的字符串对象来说，
每个字符串对象都包含一个 sds 值。

.. note::

    “包含字符串值的字符串对象”，这种说法初听上去可能会有点奇怪，
    但是在 Redis 中，
    一个字符串对象除了可以保存字符串值之外，
    还可以保存 ``long`` 类型的值，
    所以为了严谨起见，
    这里需要强调一下：
    当字符串对象保存的是字符串时，
    它包含的才是 sds 值，
    否则的话，
    它就是一个 ``long`` 类型的值。

举个例子，
以下命令创建了一个新的数据库键值对，
这个键值对的键和值都是字符串对象，
它们都包含一个 sds 值：

::

    redis> SET book "Mastering C++ in 21 days"
    OK

    redis> GET book
    "Mastering C++ in 21 days"

以下命令创建了另一个键值对，
它的键是字符串对象，
而值则是一个集合对象：

::

    redis> SADD nosql "Redis" "MongoDB" "Neo4j"
    (integer) 3

    redis> SMEMBERS nosql
    1) "Neo4j"
    2) "Redis"
    3) "MongoDB"

用 sds 取代 C 默认的 char* 类型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

因为 ``char*`` 类型的功能单一，
抽象层次低，
并且不能高效地支持一些 Redis 常用的操作（比如追加操作和长度计算操作），
所以在 Redis 程序内部，
绝大部分情况下都会使用 sds 而不是 ``char*`` 来表示字符串。

性能问题在稍后介绍 sds 定义的时候就会说到，
因为我们还没有了解过 Redis 的其他功能模块，
所以也没办法详细地举例说那里用到了 sds ，
不过在后面的章节中，
我们会经常看到其他模块（几乎每一个）都用到了 sds 类型值。

目前来说，
只要记住这个事实即可：
在 Redis 中，
客户端传入服务器的协议内容、
aof 缓存、
返回给客户端的回复，
等等，
这些重要的内容都是由 sds 类型来保存的。

Redis 中的字符串
----------------------

在 C 语言中，字符串可以用一个 ``\0`` 结尾的 ``char`` 数组来表示。

比如说， ``hello world`` 在 C 语言中就可以表示为 ``"hello world\0"`` 。

这种简单的字符串表示，在大多数情况下都能满足要求，但是，它并不能高效地支持长度计算和追加（append）这两种操作：

- 每次计算字符串长度（\ ``strlen(s)``\ ）的复杂度为 :math:`\theta(N)` 。

- 对字符串进行 N 次追加，必定需要对字符串进行 N 次内存重分配（\ ``realloc``\ ）。

在 Redis 内部，
字符串的追加和长度计算很常见，
而 :ref:`APPEND` 和 :ref:`STRLEN` 更是这两种操作，在 Redis 命令中的直接映射，
这两个简单的操作不应该成为性能的瓶颈。

另外，
Redis 除了处理 C 字符串之外，
还需要处理单纯的字节数组，
以及服务器协议等内容，
所以为了方便起见，
Redis 的字符串表示还应该是\ `二进制安全的 <http://en.wikipedia.org/wiki/Binary-safe>`_\ ：
程序不应对字符串里面保存的数据做任何假设，
数据可以是以 ``\0`` 结尾的 C 字符串，
也可以是单纯的字节数组，
或者其他格式的数据。

考虑到这两个原因，
Redis 使用 sds 类型替换了 C 语言的默认字符串表示：
sds 既可高效地实现追加和长度计算，
同时是二进制安全的。

sds 的实现
^^^^^^^^^^^^^^

在前面的内容中，
我们一直将 sds 作为一种抽象数据结构来说明，
实际上，
它的实现由以下两部分组成：

::

    typedef char *sds;


    struct sdshdr {

        // buf 已占用长度
        int len;

        // buf 剩余可用长度
        int free;

        // 实际保存字符串数据的地方
        char buf[];
    };

其中，类型 ``sds`` 是 ``char *`` 的别名（alias），而结构 ``sdshdr`` 则保存了 ``len`` 、 ``free`` 和 ``buf`` 三个属性。

作为例子，以下是新创建的，同样保存 ``hello world`` 字符串的 ``sdshdr`` 结构：

::

    struct sdshdr {
        len = 11;
        free = 0;
        buf = "hello world\0";  // buf 的实际长度为 len + 1
    };

通过 ``len`` 属性， ``sdshdr`` 可以实现复杂度为 :math:`\theta(1)` 的长度计算操作。

另一方面，
通过对 ``buf`` 分配一些额外的空间，
并使用 ``free`` 记录未使用空间的大小，
``sdshdr`` 可以让执行追加操作所需的内存重分配次数大大减少，
下一节我们就会来详细讨论这一点。

当然，
sds 也对操作的正确实现提出了要求 —— 所有处理 ``sdshdr`` 的函数，都必须正确地更新 ``len`` 和 ``free`` 属性，否则就会造成 bug 。


优化追加操作
-------------------------

在前面说到过，利用 ``sdshdr`` 结构，除了可以用 :math:`\theta(1)` 复杂度获取字符串的长度之外，还可以减少追加（append）操作所需的内存重分配次数，以下就来详细解释这个优化的原理。

为了易于理解，我们用一个 Redis 执行实例作为例子，解释一下，当执行以下代码时， Redis 内部发生了什么：

::

    redis> SET msg "hello world"
    OK

    redis> APPEND msg " again!"
    (integer) 18

    redis> GET msg
    "hello world again!"

首先， ``SET`` 命令创建并保存 ``hello world`` 到一个 ``sdshdr`` 中，这个 ``sdshdr`` 的值如下：

::

    struct sdshdr {
        len = 11;
        free = 0;
        buf = "hello world\0";
    }

当执行 :ref:`APPEND` 命令时，相应的 ``sdshdr`` 被更新，字符串 ``" again!"`` 会被追加到原来的 ``"hello world"`` 之后：

::

    struct sdshdr {
        len = 18;
        free = 18;
        buf = "hello world again!\0                  ";     // 空白的地方为预分配空间，共 18 + 18 + 1 个字节
    }

注意，
当调用 ``SET`` 命令创建 ``sdshdr`` 时，
``sdshdr`` 的 ``free`` 属性为 ``0`` ，
Redis 也没有为 ``buf`` 创建额外的空间 ——
而在执行 :ref:`APPEND` 之后，
Redis 为 ``buf`` 创建了多于所需空间一倍的大小。

在这个例子中，
保存 ``"hello world again!"`` 共需要 ``18 + 1`` 个字节，
但程序却为我们分配了 ``18 + 18 + 1 = 37`` 个字节 ——
这样一来，
如果将来再次对同一个 ``sdshdr`` 进行追加操作，
只要追加内容的长度不超过 ``free`` 属性的值，
那么就不需要对 ``buf`` 进行内存重分配。

比如说，
执行以下命令并不会引起 ``buf`` 的内存重分配，
因为新追加的字符串长度小于 ``18`` ：

::

    redis> APPEND msg " again!"
    (integer) 25

再次执行 :ref:`APPEND` 命令之后，
``msg`` 的值所对应的 ``sdshdr`` 结构可以表示如下：

::

    struct sdshdr {
        len = 25;
        free = 11;
        buf = "hello world again! again!\0           ";     // 空白的地方为预分配空间，共 18 + 18 + 1 个字节
    }

``sds.c/sdsMakeRoomFor`` 函数描述了 ``sdshdr`` 的这种内存预分配优化策略，
以下是这个函数的伪代码版本：

.. code-block:: python

    def sdsMakeRoomFor(sdshdr, required_len):

        # 预分配空间足够，无须再进行空间分配
        if (sdshdr.free >= required_len):
            return sdshdr

        # 计算新字符串的总长度
        newlen = sdshdr.len + required_len

        # 如果新字符串的总长度小于 SDS_MAX_PREALLOC
        # 那么为字符串分配 2 倍于所需长度的空间
        # 否则就分配所需长度加上 SDS_MAX_PREALLOC 数量的空间
        if newlen < SDS_MAX_PREALLOC:
            newlen *= 2
        else:
            newlen += SDS_MAX_PREALLOC

        # 分配内存
        newsh = zrelloc(sdshdr, sizeof(struct sdshdr)+newlen+1)

        # 更新 free 属性
        newsh.free = newlen - sdshdr.len

        # 返回
        return newsh

在目前版本的 Redis 中，
``SDS_MAX_PREALLOC`` 的值为 ``1024 * 1024`` ，
也就是说，
当大小小于 ``1MB`` 的字符串执行追加操作时，
``sdsMakeRoomFor`` 就为它们分配多于所需大小一倍的空间；
当字符串的大小大于 ``1MB`` ，
那么 ``sdsMakeRoomFor`` 就为它们额外多分配 ``1MB`` 的空间。

.. note:: 这种分配策略会浪费内存吗？

    执行过 :ref:`APPEND` 命令的字符串会带有额外的预分配空间，
    这些预分配空间不会被释放，
    除非该字符串所对应的键被删除，
    或者等到关闭 Redis 之后，
    再次启动时重新载入的字符串对象将不会有预分配空间。

    因为执行 :ref:`APPEND` 命令的字符串键数量通常并不多，
    占用内存的体积通常也不大，
    所以这一般并不算什么问题。

    另一方面，
    如果执行 :ref:`APPEND` 操作的键很多，
    而字符串的体积又很大的话，
    那可能就需要修改 Redis 服务器，
    让它定时释放一些字符串键的预分配空间，
    从而更有效地使用内存。

sds 模块的 API
-----------------------

sds 模块基于 ``sds`` 类型和 ``sdshdr`` 结构提供了以下 API ：

======================= ============================================================================= =================
函数                    作用                                                                            算法复杂度
======================= ============================================================================= =================
``sdsnewlen``           创建一个指定长度的 ``sds`` ，接受一个 C 字符串作为初始化值                      :math:`O(N)`
``sdsempty``            创建一个只包含空白字符串 ``""`` 的 ``sds``                                      :math:`O(N)`
``sdsnew``              根据给定 C 字符串，创建一个相应的 ``sds``                                       :math:`O(N)`
``sdsdup``              复制给定 ``sds``                                                                :math:`O(N)`
``sdsfree``             释放给定 ``sds``                                                                :math:`O(N)`
``sdsupdatelen``        更新给定 ``sds`` 所对应 ``sdshdr`` 结构的 ``free`` 和 ``len``                   :math:`O(N)`
``sdsclear``            清除给定 ``sds`` 的内容，将它初始化为 ``""``                                    :math:`O(1)`
``sdsMakeRoomFor``      对 ``sds`` 所对应 ``sdshdr`` 结构的 ``buf`` 进行扩展                            :math:`O(N)`
``sdsRemoveFreeSpace``  在不改动 ``buf`` 的情况下，将 ``buf`` 内多余的空间释放出去                      :math:`O(N)`
``sdsAllocSize``        计算给定 ``sds`` 的 ``buf`` 所占用的内存总数                                    :math:`O(1)`
``sdsIncrLen``          对 ``sds`` 的 ``buf`` 的右端进行扩展（expand）或修剪（trim）                    :math:`O(1)`
``sdsgrowzero``         将给定 ``sds`` 的 ``buf`` 扩展至指定长度，无内容的部分用 ``\0`` 来填充          :math:`O(N)`
``sdscatlen``           按给定长度对 ``sds`` 进行扩展，并将一个 C 字符串追加到 ``sds`` 的末尾           :math:`O(N)`
``sdscat``              将一个 C 字符串追加到 ``sds`` 末尾                                              :math:`O(N)`
``sdscatsds``           将一个 ``sds`` 追加到另一个 ``sds`` 末尾                                        :math:`O(N)`
``sdscpylen``           将一个 C 字符串的部分内容复制到另一个 ``sds`` 中，需要时对 ``sds`` 进行扩展     :math:`O(N)`
``sdscpy``              将一个 C 字符串复制到 ``sds``                                                   :math:`O(N)`
======================= ============================================================================= =================

``sds`` 还有另一部分功能性函数，
比如 ``sdstolower`` 、 ``sdstrim``  、 ``sdscmp`` ，
等等，
基本都是标准 C 字符串库函数的 ``sds`` 版本，
这里不一一列举了。

小结
----------

- Redis 的字符串表示为 ``sds`` ，而不是 C 字符串（以 ``\0`` 结尾的 ``char*``\ ）。

- 对比 C 字符串， ``sds`` 有以下特性：

  - 可以高效地执行长度计算（\ ``strlen``\ ）；

  - 可以高效地执行追加操作（\ ``append``\ ）；

  - 二进制安全；

- ``sds`` 会为追加操作进行优化：加快追加操作的速度，并降低内存分配的次数，代价是多占用了一些内存，而且这些内存不会被主动释放。
