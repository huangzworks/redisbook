事件处理器
===========================

事件处理器是 Redis 服务器的核心，
它处理两项重要的任务：

1. 在多个客户端中实现多路复用，接受它们发来的命令请求，并将命令的执行结果返回给客户端。

2. 实现服务器中断器。

本章就来介绍事件处理器的实现，
以及它的详细工作行为。


事件处理器状态
------------------

和其他很多的事件处理器一样，
Redis 的事件处理器也是由一个循环（loop）驱动的：
通过在一个循环里不断对事件状态进行修改，
从而实现事件的处理、添加、修改和删除操作：

.. image:: image/event-loop.png

Redis 事件处理器的状态由 ``ae.h/aeEventLoop`` 结构表示：

::

    typedef struct aeEventLoop {
        // 目前已注册的最大描述符
        int maxfd;   /* highest file descriptor currently registered */
        // 目前已追踪的最大描述符
        int setsize; /* max number of file descriptors tracked */
        // 记录时间事件的下个 id
        long long timeEventNextId;
        // 最后一次执行时间事件的时间
        time_t lastTime;     /* Used to detect system clock skew */

        // 已注册的文件事件
        aeFileEvent *events; /* Registered events */

        // 已就绪的文件事件
        aeFiredEvent *fired; /* Fired events */

        // 时间事件
        aeTimeEvent *timeEventHead;

        // 事件处理器的开关
        int stop;
        // 多路复用库的私有数据
        void *apidata; /* This is used for polling API specific data */
        // 在处理事件前要执行的函数
        aeBeforeSleepProc *beforesleep;
    } aeEventLoop;

在这个结构中，
最重要的是 ``events`` 、 ``fired`` 和 ``timeEventHead`` 三个属性：

- ``events`` 属性：保存所有正在等待的文件事件。

- ``fired`` 属性：记录所有已就绪文件事件的信息。“已就绪”指的是，事件无须再等待，已经可以被执行了。

- ``timeEventHead`` 属性：保存所有正在等待的时间事件。因为所有时间事件都串连在一个链表里，所以这个属性被称为 ``Head`` 。

在本章接下来的内容中，
我们将详细地分析这三个属性，
以及它们所对应的事件。


文件事件
------------------------

Redis 服务器通过在多个客户端之间进行多路复用，
从而实现高效的命令请求处理：
多个客户端通过套接字连接到 Redis 服务器中，
但只有在套接字可以无阻塞地进行读或者写时，
服务器才会和这些客户端进行交互。

Redis 将这类因为对套接字进行多路复用而产生的事件称为文件事件（file event），
这种事件的信息分别由 ``aeEventLoop`` 结构中的 ``events`` 属性和 ``fired`` 属性保存。

以下两个小节将对这两个属性进行介绍。

events 属性
^^^^^^^^^^^^^^^^

``events`` 属性是一个 ``aeFileEvent`` 类型的数组，
每个 ``aeFileEvent`` 结构都记录了一个和文件描述符相关联的事件的信息，
其中 ``events[i]`` 记录的就是文件描述符 ``i`` 的事件信息。

``aeFileEvent`` 类型的定义如下：

::

    typedef struct aeFileEvent {
        // 事件类型掩码
        int mask; 
        // 写事件函数
        aeFileProc *rfileProc;
        // 读事件函数
        aeFileProc *wfileProc;
        // 多路复用库的私有数据
        void *clientData;
    } aeFileEvent;

``aeFileEvent`` 最重要的是 ``mask`` 、 ``rfileProc`` 和 ``wfileProc`` 三个属性，
它们的作用分别如下：

- ``mask`` ：记录了描述符正在等待的文件事件，它的值可以是 ``AE_READABLE`` 或者 ``AE_WRITABLE`` ，或者两者的或。

- ``rfileProc`` ：指向读事件处理函数的指针。

- ``wfileProc`` ：指向写事件处理函数的指针。

注意，
虽然文件描述符可以同时关联两种事件的处理函数，
但同一时间内，
只有一种事件会被处理，
这也就是说，
连接要么写，
要么读，
但不能又读又写。

如果文件描述符同时关联了两种事件，
并且两种事件都已就绪，
那么程序优先执行读事件。

fired 属性
^^^^^^^^^^^^^^

除了记录了所有事件信息的 ``events`` 数组之外，
多路复用程序还使用 ``fired`` 数组记录所有已就绪文件的事件信息。

``fired`` 属性是一个 ``aeFiredEvent`` 类型的数组，
每个 ``aeFiredEvent`` 结构都记录了一个已就绪的文件事件。

``aeFiredEvent`` 类型的定义如下：

::

    typedef struct aeFiredEvent {
        // 已就绪文件描述符
        int fd;
        // 事件类型掩码，可以是 AE_READABLE 或 AE_WRITABLE
        int mask;
    } aeFiredEvent;

``fd`` 记录了已就绪文件的描述符。

``mask`` 则记录了已就绪的事件类型，它的值可以是 ``AE_READABLE`` 、 ``AE_WRITABLE`` 或这两者的或：

- ``AE_READABLE`` 表示文件可以无阻塞地读。

- ``AE_WRITABLE`` 表示文件可以无阻塞地写。

执行文件事件
^^^^^^^^^^^^^^^^^^

文件事件使用 ``aeApiPoll`` 函数等待文件事件发生，
这个函数是底层多路复用库的类 ``poll`` 函数的一个包装，
它返回已就绪事件的数量，
然后程序处理所有已就绪事件。

整个过程可以描述为以下伪代码：

.. code-block:: python

    # 在最多 timeout 秒的阻塞之内，获取已就绪事件
    # 并返回已就绪事件的数量
    numevents = aeApiPoll(eventLoop, timeout)

    # 遍历所有已就绪事件
    for i in numevents:
   
        # 已就绪事件的文件描述符
        fd = eventLoop.fired[i].fd

        # 已就绪事件的类型掩码
        mask = eventLoop.fired[i].mask
    
        # 该文件所关联的事件信息
        event = eventLoop.events[ready_fd]

        # 执行已就绪事件
        # 如果两种事件都已就绪，那么优先执行读事件
        if (event.mask & mask & AE_READABLE):
            # 执行读事件
            fe->rfileProc(eventLoop, fd, fd->clientData, mask)
        elif (event.mask & mask & AE_WRITABLE):
            # 执行写事件
            fe->wfileProc(eventLoop, fd, fd->clientData, mask)

Redis 处理事件的方式是典型的 `reactor 模式 <http://en.wikipedia.org/wiki/Reactor_pattern>`_ ：
事件处理器和事件源（套接字描述符）相关联，
当事件就绪时，
将套接字描述符、事件状态等数据作为参数，
调用相应的事件处理器。

文件事件的应用：接收命令请求和返回命令结果
-----------------------------------------------

文件事件实现了 Redis 的命令请求和结果返回机制。

每个连接到服务器的客户端，
服务器都会为其绑定读事件，
当客户端向服务器发送命令请求时，
相应的读事件就会就绪。

另一方面，
当命令执行完之后，
服务器会将命令的执行结果保存到缓存中，
并为之前发送命令的客户端绑定写事件，
当写事件就绪时，
就可以将命令的返回值传回给客户端。

作为例子，
下图展示了三个连接到服务器的客户端。
图片显示，
事件处理器正在等待客户端套接字的读事件就绪，
这就是说，
服务器正在等待客户端发来命令请求：

.. image:: image/event-pending.png

当客户端向服务器发来命令请求时，
相应客户端套接字的读事件会变为就绪状态。

在下图展示的例子中，
客户端 X 和 Z 都给服务器送来命令请求：

.. image:: image/event-readable.png

当事件处理器发现读事件就绪之后，
它会调用相关的读入程序，
读取客户端送来的命令的详细内容，
并通知命令执行器，
让它执行客户端送入的命令。

在下图展示的例子中，
程序读取客户端 X 和 Z 发送的命令，
并让命令执行器执行它们：

.. image:: image/event-accept-command.png
            
命令执行器在执行完命令之后，
会将结果保存在服务器缓存，
并通知文件事件处理器，
命令已经处理完毕，
请等待相关客户端的写事件。

在下图展示的例子中，
命令执行完毕之后，
事件处理器会等待客户端 X 和 Z 的写事件就绪：

.. image:: image/event-return-result-to-handler.png

当相应客户端的写事件就绪时，
就可以将命令的执行结果传回客户端。

在下图展示的例子中，
服务器将命令分别传回给客户端 X 和 Z ：

.. image:: image/event-return-result-to-client.png

以上就是 Redis 服务器使用文件事件，
实现命令的接收和发送的整个过程。

时间事件
-----------

只有一个时间事件： ``redis.c/serverCron``


时间事件的应用：服务器中断器
---------------------------------

TODO


事件的执行顺序和调度
------------------------

TODO
