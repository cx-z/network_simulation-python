# network_simulation-python
用python模拟了网络环境,实现了数据包的收、发功能；
Node.py文件实现了节点功能，所有节点的函数deal_packets()都是一个子线程，并发运行；
Route.py实现了寻找最短路的功能；
Topology.py中构造了网络拓扑，并生成了全局路由表；
