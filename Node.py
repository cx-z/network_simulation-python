# -*- coding:utf-8 -*-
import Packet
import time
import Topology


def get_nexthop(node_list, name):  # 获取下一跳
    nextHop = node_list[0]
    for node in node_list:
        if node.address == name:
            nextHop = node
    return nextHop


def copy_packet(pkt):  # 复制数据包
    packet = Packet.Packet()
    packet.content = pkt.content
    packet.seq_num = pkt.seq_num
    packet.dst = pkt.dst
    packet.src = pkt.src
    return packet


class Node(object):
    def __init__(self, addr):
        self.address = addr  # 本节点IP地址
        self.entry = []  # 缓存区，上一跳将数据包发送到缓存区，本节点从缓存区取出数据包
        self.nextHop = self  # 下一跳
        self.packets = []  # 应用程序处理的数据包

    def send_packets(self, node_list, link_list):
        temp_packet = copy_packet(self.entry[0])
        for item in Topology.route_table:  # 根据全局路由表中查找下一跳
            if item[-2] == self.entry[0].dst.address and item[0] == self.address:
                self.nextHop = get_nexthop(node_list, item[1])
        # for item in Topology.route_table:  # 根据全局路由表查找下一跳
        #     if item[-2] == self.nextHop.address and item[0] == self.address:
        #         time.sleep(item[-1] * 0.01)  # 和下一跳距离越远，发送时间越长
        while True:
            if len(self.nextHop.entry) < 5:  # 若有需要转发的数据包
                sec = len(temp_packet.content)
                time.sleep(0.1 * sec)  # 数据包越大，发送时间越长
                for link in link_list:  # 将数据包发送到与下一跳之间的链路
                    if link.Pre == self and link.Next == self.nextHop:
                        link.channel.append(temp_packet)
                        print(self.address + "发包 |" + temp_packet.content + "| 到" + link.Pre.address + link.Next.address)
                # print(self.address + "发包 |" + temp_packet.content + "| 到" + self.nextHop.address)
                # self.nextHop.entry.append(temp_packet)  # 将数据包发送到下一跳
                break
            else:  # 等待下一跳接收功能解除占用
                time.sleep(0.5)

    # 发送数据包到下一跳
    def deal_packets(self, node_list, link_list):
        while True:
            if len(self.entry) != 0:  # 如果缓存区有数据包
                if self.entry[0].dst != self:  # 如果不是目的节点
                    self.send_packets(node_list, link_list)  # 转发数据包
                else:  # 如果是目的节点
                    self.deliver(self.entry[0])  # 向上层传递数据包
                del self.entry[0]  # 删除已经被处理过的数据包

    def deliver(self, pkt):  # 将数据包交由应用程序处理
        temp_packet = copy_packet(pkt)
        self.packets.append(temp_packet)
        print(self.address + "处理数据 |" + temp_packet.content + '|')


class DiversionNode(Node):
    def __init__(self, addr):
        super(DiversionNode, self).__init__(addr)
        self.diver_num = 0
        self.nextHops = []
        self.diver_length = []
        self.diver_flag = True  # True表示还没有对数据流进行分片选路

    def get_nextHops(self, node_list, packet):
        for item in Topology.route_table:
            if len(item) == 3 and item[0] == self.address:
                temp_nextHop = get_nexthop(node_list, item[1])
                for link in Topology.route_table:  # 如果下一跳与目的节点间存在链路且不返回本节点
                    if link[0] == temp_nextHop.address and link[-2] == packet.dst.address:
                        # print('+++++++'+ packet.dst.address + '+++++++++')
                        # print('************' + temp_nextHop.address + '***********')
                        if self.address not in link:
                            self.nextHops.append(temp_nextHop)
                            for item in Topology.route_table:  # 根据全局路由表查找下一跳
                                if item[-2] == temp_nextHop.address and item[0] == self.address:
                                    trans_next_time = item[-1] * 0.1  # 和下一跳距离越远，发送时间越长
                                    self.diver_length.append(link[-1] + trans_next_time + (len(link)-1)*len(packet.content)*0.1)

    def rank_nextHops(self):
        temp_dic = {}
        for i in range(len(self.nextHops)):
            temp_dic.update({self.nextHops[i]: self.diver_length[i]})
        temp_list = sorted(temp_dic.items(), key=lambda x: x[1], reverse=True)
        self.nextHops = []
        for i in range(len(temp_list)):
            self.nextHops.append(temp_list[i][0])
        self.nextHops.reverse()

    def send_packets(self, node_list, link_list):
        temp_packet = copy_packet(self.entry[0])
        self.get_nextHops(node_list, temp_packet)
        if self.diver_flag:
            self.rank_nextHops()
            self.diver_flag = False
        # self.nextHop = self.nextHops[self.diver_num % len(self.nextHops)]
        if self.diver_num <= 2:
            self.nextHop = self.nextHops[0]
        elif self.diver_num <= 4:
            if self.diver_num == 3:
                time.sleep(1)
            self.nextHop = self.nextHops[1]
        else:
            if self.diver_num == 5:
                time.sleep(1)
            self.nextHop = self.nextHops[2]
        self.diver_num += 1
        # for item in Topology.route_table:  # 根据全局路由表查找下一跳
        #     if item[-2] == self.nextHop.address and item[0] == self.address:
        #         temp_wait = item[-1] * 0.01
                # time.sleep(item[-1] * 0.01)  # 和下一跳距离越远，发送时间越长
        while True:
            if len(self.nextHop.entry) < 5:  # 若有需要转发的数据包
                sec = len(temp_packet.content)
                time.sleep(0.1 * sec)  # 数据包越大，发送时间越长
                for link in link_list:  # 将数据包发送到与下一跳之间的链路
                    if link.Pre == self and link.Next == self.nextHop:
                        link.channel.append(temp_packet)
                        print(self.address + "发包 |" + temp_packet.content + "| 到" + link.Pre.address + link.Next.address)
                # self.nextHop.entry.append(temp_packet)  # 将数据包发送到下一跳
                break
            else:  # 等待下一跳接收功能解除占用
                time.sleep(0.5)
