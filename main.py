# -*- coding:utf-8 -*-
import Topology
import Node
import Packet
import threading
import Link


def simulator_start(src_node, dst_node, content):
    start = src_node.address
    end = dst_node.address
    shortestPath, length = Topology.topo.get_shortest_path(start, end)
    shortestPath.reverse()
    print('{}->{}的最短路径是：{}，最短路径为：{}'.format(start, end, shortestPath, length))

    # 源节点发送数据包
    src_node.packets = [Packet.Packet() for row in range(len(content))]
    num = 0
    print('包个数' + str(len(src_node.packets)))
    for item in src_node.packets:
        item.src = src_node
        item.dst = dst_node
        item.content = content[num]
        num += 1
        item.seq_num = num
        src_node.entry.append(item)


if __name__ == '__main__':

    node_list = []
    link_list = []

    # 实例化普通节点
    for item in Topology.address_list:
        temp_node = Node.Node(item)
        node_list.append(temp_node)

    # 本次仿真的输入
    # ----------------------------------------------------------------------------------------------------
    del node_list[0]
    NodeA = Node.DiversionNode(Topology.address_list[0])
    node_list.insert(0, NodeA)
    content1 = ["Hello", "Simulator", "Hi", "my", "own", "network"]
    simulator_start(node_list[0], node_list[-1], content1)
    # ----------------------------------------------------------------------------------------------------

    # 所有相邻节点间的单向链路
    link0 = Link.Link(node_list[0], node_list[1], 5)
    link1 = Link.Link(node_list[0], node_list[2], 5)
    link2 = Link.Link(node_list[0], node_list[3], 5)
    link3 = Link.Link(node_list[1], node_list[0], 5)
    link4 = Link.Link(node_list[2], node_list[0], 5)
    link5 = Link.Link(node_list[3], node_list[0], 5)
    link6 = Link.Link(node_list[1], node_list[4], 5)
    link7 = Link.Link(node_list[4], node_list[1], 5)
    link8 = Link.Link(node_list[2], node_list[4], 5)
    link9 = Link.Link(node_list[4], node_list[2], 5)
    link10 = Link.Link(node_list[3], node_list[4], 5)
    link11 = Link.Link(node_list[4], node_list[3], 5)
    link_list.append(link0)
    link_list.append(link1)
    link_list.append(link2)
    link_list.append(link3)
    link_list.append(link4)
    link_list.append(link5)
    link_list.append(link6)
    link_list.append(link7)
    link_list.append(link8)
    link_list.append(link9)
    link_list.append(link10)
    link_list.append(link11)
    # ------------------------------------------------------------------------------------------

    threads = []
    for i in range(len(node_list)):
        thread = threading.Thread(target=node_list[i].deal_packets, args=(node_list, link_list))
        threads.append(thread)
    for i in range(len(link_list)):
        thread = threading.Thread(target=link_list[i].trans_packet, args=())
        threads.append(thread)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join(2)

    for node in node_list:
        print(node.address + '\t' + 'nexthop' + node.nextHop.address + '\t', end='')
        for pkt in node.packets:
            print('| {} : {} |\t'.format(pkt.seq_num, pkt.content), end='')
        print('')
    print('_______________________________END________________________________________')
