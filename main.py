# -*- coding:utf-8 -*-
import Topology, Node, Packet, time


if __name__ == '__main__':

    node_list = []

    # 实例化普通节点
    name_list = Topology.name_list1 + Topology.name_list2
    for item in name_list:
        temp_node = Node.Node(item)
        node_list.append(temp_node)

    # 实例化校验节点对
    # _________________________________________________________________________________
    check_node_namelist = ['B', 'D', 'E', 'G']
    for i in range(2):
        for node in node_list:
            if node.name in check_node_namelist:
                node_list.remove(node)
    temp_len = len(node_list)
    for i in range(4):
        check_node = Node.CheckNode(check_node_namelist[i])
        node_list.append(check_node)
    node_list[temp_len].pair = node_list[temp_len + 2]
    node_list[temp_len + 2].pair = node_list[temp_len]
    node_list[temp_len + 1].pair = node_list[temp_len + 3]
    node_list[temp_len + 3].pair = node_list[temp_len + 1]
    # _______________________________________________________________________________________

    # 实例化篡改节点
    # _________________________________________________________________________________
    falsify_node_list = ['C']
    for i in range(1):
        for node in node_list:
            if node.name in falsify_node_list:
                node_list.remove(node)
    for i in range(1):
        falsify_node = Node.FalsifyNode(falsify_node_list[i])
        node_list.append(falsify_node)
    # _______________________________________________________________________________________

    start = 'A'
    end = ['I']
    for j in range(len(end)):
        shortestPath, length = Topology.topo.get_shortest_path(start, end[j])
        shortestPath.reverse()
        print('{}->{}的最短路径是：{}，最短路径为：{}'.format(start, end[j], shortestPath, length))

        # 根据最短路，将相应的节点按次序放入路由表
        route_table = []
        for item in shortestPath:
            for node in node_list:
                if item == node.name:
                    route_table.append(node)

        # 设置链路经过的节点的路由表
        for node in route_table:
            node.src = route_table[0]
            node.dst = route_table[len(route_table) - 1]
            if node != route_table[len(route_table) - 1]:
                node.nextHop = route_table[route_table.index(node) + 1]

        # 源节点发送数据包
        content = ["Hello", "Simulator", "Hi", "my", "own", "network", "Wonderful"]
        for i in range(1):
            route_table[0].packets = [Packet.Packet() for row in range(1)]
            num = 0
            for item in route_table[0].packets:
                item.src = route_table[0]
                item.dst = route_table[len(route_table) - 1]
                item.content = content[num]
                num += 1
                route_table[0].send_packets(item, route_table)

            for node in route_table:
                print(node.name + '\t', end='')
                for pkt in node.packets:
                    #print(pkt.src.name + '\t' + pkt.dst.name + '\t' + pkt.content + '\t', end='')
                    print('|' + pkt.content + '|' +  '\t', end='')
                print('')

            time.sleep(0.1)
            print('____________________________________________________________________________')
