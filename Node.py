# -*- coding:utf-8 -*-
import Packet


def check(pkt):
    check_pkt = Packet.Packet()
    check_pkt.content = str(hash(pkt.content))
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
        self.packets.append(pkt)
        if self.nextHop != self:  # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            self.send_packets(pkt, route_table)

    # 发送数据包到下一跳
    def send_packets(self, pkt, route_table):
        self.src = pkt.src
        self.dst = pkt.dst
        if pkt.src == self:
            self.flag = True
        if self.flag:
            self.nextHop = route_table[route_table.index(self) + 1]
            self.nextHop.receive_packets(pkt, route_table)
            self.flag = False


class CheckNode(Node):
    def __init__(self, seq):
        super(CheckNode, self).__init__(seq)
        self.pair = self
        self.count = 0
        self.check_state = False

    def receive_packets(self, pkt, route_table):
        self.packets.append(pkt)  # 收到数据包
        if self.nextHop != self:   # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            if self.pair in route_table:
                if route_table.index(self) < route_table.index(self.pair):  # 如果该校验节点在前
                    self.send_packets(pkt, route_table)
                    if self.count % 3 == 0:
                        check_packet = check(pkt)
                        check_packet.src = self
                        check_packet.dst = self.pair
                        #pkt.content = "falsified"  # 篡改数据包
                        self.packets.append(check_packet)
                        self.send_packets(check_packet, route_table)
                elif route_table.index(self) > route_table.index(self.pair):  # 如果该校验节点在后
                    if pkt.dst != self:
                        self.send_packets(pkt, route_table)
                    if self.count % 3 == 0:
                        check_packet = check(pkt)
                        self.packets.append(check_packet)
                    if pkt.src == self.pair and pkt.dst == self:
                        for item in self.packets:
                            if item.content == pkt.content:
                                self.check_state = True
                        if self.check_state:
                            print(self.name + '处检测结果：数据包未被篡改')
                        else:  # 检测到数据包被篡改后，向目的节点发送通知
                            print(self.name + '处检测结果：数据包已被篡改')
                            notify_packet = Packet.Packet()
                            notify_packet.content = "The stream from {} to {} has been falsified".format(route_table[0].name,
                                                                                                         route_table[len(
                                                                                                             route_table) - 1].name)
                            notify_packet.src = self
                            notify_packet.dst = route_table[len(route_table) - 1]
                            self.packets.append(notify_packet)
                            self.send_packets(notify_packet, route_table)
                self.count += 1
