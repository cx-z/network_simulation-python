# -*- coding:utf-8 -*-
import Topology
import Node
import Packet
import threading
import time


def simulator_start(src_node, dst_node):
    start = src_node.address
    end = dst_node.address
    shortestPath, length = Topology.topo.get_shortest_path(start, end)
    shortestPath.reverse()
    print('{}->{}的最短路径是：{}，最短路径为：{}'.format(start, end, shortestPath, length))

    # 源节点发送数据包
    content = ["Hello", "Simulator", "Hi", "my", "own", "network", "Wonderful"]
    src_node.packets = [Packet.Packet() for row in range(3)]
    num = 0
    print('包个数' + str(len(src_node.packets)))
    for item in src_node.packets:
        item.src = src_node
        item.dst = dst_node
        item.content = content[num]
        num += 1
        item.seq_num = num
        src_node.send_packets(item, node_list)
        print("源节点发包" + item.content)


if __name__ == '__main__':

    node_list = []

    # 实例化普通节点
    for item in Topology.address_list:
        temp_node = Node.Node(item)
        node_list.append(temp_node)

    threads = []
    for i in range(len(node_list)):
        thread = threading.Thread(target=node_list[i].receive_packets,args=(node_list,))
        threads.append(thread)
    thread = threading.Thread(target=simulator_start, args=(node_list[0], node_list[-1]))
    start_time = time.time()
    for t in threads:
        t.start()
    thread.start()
    thread.join(2)
    for t in threads:
        t.join(2)

    for node in node_list:
        print(node.address + '\t' + 'nexthop' + node.nextHop.address + '\t', end='')
        for pkt in node.packets:
            print('| {} : {} |\t'.format(pkt.seq_num, pkt.content), end='')
        print('')
    print('_______________________________________________________________________')
