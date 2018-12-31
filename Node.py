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
        self.send_flag = False  # 标识符，若为True，则将数据包转发到下一跳
        self.receive_flag = True  # 标识符，若为True，表示可以接收数据包；若为False，接收功能正在被其他节点占用

    # 从上一跳接收数据包
    def receive_packets(self, node_list):
        while True:
            if not self.receive_flag:  # 如果另一个上一跳发来了包
                time.sleep(0.1)
                print(self.address + "收包" + self.entry[-1].content)
                if len(self.packets) > 5:
                    del self.packets[0]
                if self.entry[-1].dst != self:  # 如果不是目的节点，向下一跳发送数据包
                    self.send_flag = True
                    self.send_packets(self.entry[-1], node_list)
                else:  # 如果是目的节点，将数据包交由应用程序处理
                    self.deliver(self.entry[-1])
                self.receive_flag = True

    # 发送数据包到下一跳
    def send_packets(self, pkt, node_list):
        for item in Topology.route_table:  # 根据全局路由表中查找下一跳
            if item[-2] == pkt.dst.address and item[0] == self.address:
                self.nextHop = get_nexthop(node_list, item[1])
        for item in Topology.route_table:  # 根据全局路由表查找下一跳
            if item[-2] == self.nextHop.address and item[0] == self.address:
                time.sleep(item[-1] * 0.01)  # 和下一跳距离越远，发送时间越长
        if pkt.src == self:  # 如果是源节点，不经过接收直接发送数据包
            self.send_flag = True
        while self.send_flag:  # 若有需要转发的数据包
            if self.nextHop.receive_flag:  # 下一跳接收功能没有被占用
                self.send_flag = False
                temp_packet = Packet.Packet()
                temp_packet.content = pkt.content
                temp_packet.dst = pkt.dst
                temp_packet.src = pkt.src
                temp_packet.seq_num = pkt.seq_num
                print(self.address + "发包" + temp_packet.content + "到" + self.nextHop.address)
                sec = len(temp_packet.content)
                time.sleep(0.01 * sec)  # 数据包越大，发送时间越长
                self.nextHop.receive_flag = False  # 发送包之前，将下一跳接收标识符设为False，不允许其他节点给下一跳发送报文
                self.nextHop.entry.append(temp_packet)
                break
            else:  # 等待下一跳接收功能解除占用
                time.sleep(0.05)

    def deliver(self, pkt):  # 将数据包交由应用程序处理
        temp_packet = Packet.Packet()
        temp_packet.content = pkt.content
        temp_packet.dst = pkt.dst
        temp_packet.src = pkt.src
        temp_packet.seq_num = pkt.seq_num
        self.packets.append(temp_packet)
        print(self.address + "处理数据" + temp_packet.content)
