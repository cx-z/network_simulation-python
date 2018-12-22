# -*- coding:utf-8 -*-
import Packet, sys


def check(pkt):
    check_pkt = Packet.Packet()
    check_pkt.content = str(hash(pkt.content))
    return check_pkt


class Node(object):
    def __init__(self, seq):
        self.name = seq
        self.packets = []
        self.nextHop = self
        self.flag = False

    # 从上一跳接收数据包
    def receive_packets(self, pkt, route_table):
        temp_packet = Packet.Packet()
        temp_packet.content = pkt.content
        temp_packet.dst = pkt.dst
        temp_packet.src = pkt.src
        self.packets.append(temp_packet)
        # if len(self.packets) > 5:
        #     del self.packets[0]
        if self.nextHop != self:  # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            self.send_packets(temp_packet, route_table)

    # 发送数据包到下一跳
    def send_packets(self, pkt, route_table):
        if pkt.src == self:
            self.flag = True
        if self.flag:
            self.nextHop = route_table[route_table.index(self) + 1]
            self.flag = False
            self.nextHop.receive_packets(pkt, route_table)


class CheckNode(Node):
    def __init__(self, seq):
        super(CheckNode, self).__init__(seq)
        self.pair = self
        self.count = 0
        self.check_state = False

    def receive_packets(self, pkt, route_table):
        temp_packet = Packet.Packet()
        temp_packet.content = pkt.content
        temp_packet.dst = pkt.dst
        temp_packet.src = pkt.src
        # if len(self.packets) > 10:
        #     del self.packets[0]
        if self.nextHop != self:   # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            if self.pair in route_table:
                if route_table.index(self) < route_table.index(self.pair):  # 如果该校验节点在前
                    self.packets.append(temp_packet)  # 收到数据包
                    self.send_packets(temp_packet, route_table)
                    if self.count % 3 == 0:  # 每三个包校验一次
                        check_packet = check(pkt)
                        check_packet.src = self
                        check_packet.dst = self.pair
                        self.packets.append(check_packet)
                        self.send_packets(check_packet, route_table)
                elif route_table.index(self) > route_table.index(self.pair):  # 如果该校验节点在后
                    if pkt.dst != self:
                        self.send_packets(temp_packet, route_table)
                    if self.count % 3 == 0:  # 每三个包校验一次
                        check_packet = check(pkt)
                        self.packets.append(check_packet)  # 将生成的校验包放入自己的缓存
                    if temp_packet.src == self.pair and temp_packet.dst == self:
                        for item in self.packets:
                            if item.content == temp_packet.content:
                                print(item.content)
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
                    self.packets.append(temp_packet)  # 收到数据包
                self.count += 1
                self.check_state = False
            else:
                self.send_packets(temp_packet, route_table)


class FalsifyNode(Node):
    def __init__(self, seq):
        super(FalsifyNode, self).__init__(seq)
        self.count = 0

    def receive_packets(self, pkt, route_table):
        temp_packet = Packet.Packet()
        temp_packet.content = pkt.content
        temp_packet.dst = pkt.dst
        temp_packet.src = pkt.src
        self.packets.append(temp_packet)
        # if len(self.packets) > 5:
        #     del self.packets[0]
        if self.nextHop != self:  # 如果不是目的节点，向下一跳发送数据包
            self.flag = True
            if self.count % 3 == 0:  # 每三个包篡改一次
                temp_packet.content = "falsified"
                pass
            self.count += 1
            self.send_packets(temp_packet, route_table)
