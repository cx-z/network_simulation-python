# -*- coding:utf-8 -*-
import Packet


def check(pkt):
    check_pkt = Packet.Packet()
    check_pkt.content = pkt.content + ": check packet"
    return check_pkt


class Node(object):
    def __init__(self, seq):
        self.name = seq
        self.packets = []
        self.src = self
        self.dst = self
        self.nextHop = self
        self.flag = False

    # 从上一跳接收数据包
    def receive_packets(self, pkt, route_table):
        self.packets = pkt
        if self.nextHop != self:  # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            self.send_packets(self.packets, route_table)

    # 发送数据包到下一跳
    def send_packets(self, pkts, route_table):
        for pkt in pkts:
            self.src = pkt.src
            self.dst = pkt.dst
            if self.src == self:
                self.flag = True
            if self.flag:
                self.nextHop = route_table[route_table.index(self) + 1]
                self.nextHop.receive_packets(self.packets, route_table)
                self.flag = False


class CheckNode(Node):
    def __init__(self, seq):
        super(CheckNode, self).__init__(seq)
        self.pair = self
        self.count = 0

    def receive_packets(self, pkts, route_table):
        self.packets = pkts  # 收到数据包
        self.count += 1
        self.flag = True
        if self.nextHop != self and self.count <= 1:  # 如果不是目的节点，向下一跳发送数据包
            if self.pair in route_table:
                if route_table.index(self) < route_table.index(self.pair):  # 如果该校验节点在前
                    check_packet = check(self.packets[0])
                    check_packet.src = self
                    check_packet.dst = self.pair
                    self.packets[0].content = "falsified"  # 篡改数据包
                    self.packets.append(check_packet)
                else:  # 如果该校验节点在后
                    check_state = False
                    check_packet = check(self.packets[0])
                    for item in self.packets:
                        if item.content == check_packet.content:
                            self.packets.remove(item)
                            check_state = True
                        elif item.dst == self:
                            self.packets.remove(item)
                    if check_state:
                        print(self.name + '处检测结果：数据包未被篡改')
                        print(self.packets)
                    else:
                        print(self.name + '处检测结果：数据包已被篡改')
                        print(self.packets)
                        notify_packet = Packet.Packet()
                        notify_packet.content = "The stream from {} to {} has been falsified".format(route_table[0].name,
                                                                                                     route_table[len(
                                                                                                         route_table) - 1].name)
                        notify_packet.src = self
                        notify_packet.dst = route_table[len(route_table) - 1]
                        self.packets.append(notify_packet)
            self.send_packets(self.packets, route_table)
