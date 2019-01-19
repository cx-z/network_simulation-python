# -*- coding:utf-8 -*-
import time
import Packet


def copy_packet(pkt):  # 复制数据包
    packet = Packet.Packet()
    packet.content = pkt.content
    packet.seq_num = pkt.seq_num
    packet.dst = pkt.dst
    packet.src = pkt.src
    return packet


class Link:
    def __init__(self, node1, node2, length):
        self.Pre = node1
        self.Next = node2
        self.channel = []
        self.length = length

    def trans_packet(self):
        while True:
            if len(self.channel) > 0:
                temp_packet = copy_packet(self.channel.pop(0))
                time.sleep(0.05*self.length)
                self.Next.entry.append(temp_packet)
                print(self.Pre.address + self.Next.address + "发包 |" + temp_packet.content + "| 到" + self.Next.address)
