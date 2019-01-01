# -*- coding:utf-8 -*-
import Packet
import time
import Topology


def get_nexthop(node_list, name):
    nextHop = node_list[0]
    for node in node_list:
        if node.address == name:
            nextHop = node
    return nextHop


class Node(object):
    def __init__(self, addr):
        self.address = addr  # 本节点IP地址
        self.entry = []  # 缓存区，上一跳将数据包发送到缓存区，本节点从缓存区取出数据包
        self.nextHop = self  # 下一跳
        self.packets = []  # 应用程序处理的数据包

    # 发送数据包到下一跳
    def send_packets(self, node_list):
        while True:
            if len(self.entry) != 0:  # 如果有等待发送的数据包
                if self.entry[0].dst != self:
                    temp_packet = Packet.Packet()
                    temp_packet.content = self.entry[0].content
                    temp_packet.dst = self.entry[0].dst
                    temp_packet.src = self.entry[0].src
                    temp_packet.seq_num = self.entry[0].seq_num
                    for item in Topology.route_table:  # 根据全局路由表中查找下一跳
                        if item[-2] == self.entry[0].dst.address and item[0] == self.address:
                            self.nextHop = get_nexthop(node_list, item[1])
                    for item in Topology.route_table:  # 根据全局路由表查找下一跳
                        if item[-2] == self.nextHop.address and item[0] == self.address:
                            time.sleep(item[-1] * 0.01)  # 和下一跳距离越远，发送时间越长
                    while True:
                        if len(self.nextHop.entry) < 5:  # 若有需要转发的数据包
                            print(self.address + "发包" + temp_packet.content + "到" + self.nextHop.address)
                            sec = len(temp_packet.content)
                            time.sleep(0.01 * sec)  # 数据包越大，发送时间越长
                            self.nextHop.entry.append(temp_packet)  # 将数据包发送到下一跳
                            del self.entry[0]
                            break
                        else:  # 等待下一跳接收功能解除占用
                            time.sleep(0.05)
                else:
                    self.deliver(self.entry[0])
                    del self.entry[0]

    def deliver(self, pkt):  # 将数据包交由应用程序处理
        temp_packet = Packet.Packet()
        temp_packet.content = pkt.content
        temp_packet.dst = pkt.dst
        temp_packet.src = pkt.src
        temp_packet.seq_num = pkt.seq_num
        self.packets.append(temp_packet)
        print(self.address + "处理数据" + temp_packet.content)
