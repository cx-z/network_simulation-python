# -*- coding:utf-8 -*-
import Graph


name_list1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
name_list2 = ['a', 'b', 'c', 'd1', 'd2', 'e', 'f1', 'f2', 'g', 'h1', 'h2', 'i', 'j', 'k', 'l1', 'l2']

topo = Graph.Graph()
topo.add_vertex('A', {'B': 10, 'D': 12, 'a': 3})
topo.add_vertex('B', {'A': 10, 'C': 8, 'G': 20, 'b': 3})
topo.add_vertex('C', {'B': 8, 'E': 14, 'c': 3})
topo.add_vertex('D', {'B': 12, 'F': 12, 'd1': 3, 'd2': 7})
topo.add_vertex('E', {'C': 14, 'F': 10, 'I': 12, 'e': 5})
topo.add_vertex('F', {'D': 10, 'E': 10, 'G': 6, 'f1': 5, 'f2': 10})
topo.add_vertex('G', {'B': 20, 'F': 6, 'H': 6, 'g': 3})
topo.add_vertex('H', {'G': 6, 'K': 8, 'h1': 4, 'h2': 5})
topo.add_vertex('I', {'E': 13, 'J': 6, 'L': 10, 'i': 6})
topo.add_vertex('J', {'I': 6, 'K': 5, 'j': 3})
topo.add_vertex('K', {'H': 8, 'J': 5, 'L': 3, 'k': 2})
topo.add_vertex('L', {'I': 10, 'K': 3, 'l1': 3, 'l2': 5})
topo.add_vertex('a', {'A': 3})
topo.add_vertex('b', {'B': 3})
topo.add_vertex('c', {'C': 3})
topo.add_vertex('d1', {'D': 3})
topo.add_vertex('d2', {'D': 7})
topo.add_vertex('e', {'E': 5})
topo.add_vertex('f1', {'F': 5})
topo.add_vertex('f2', {'F': 5})
topo.add_vertex('g', {'G': 3})
topo.add_vertex('h1', {'H': 4})
topo.add_vertex('h2', {'H': 5})
topo.add_vertex('i', {'I': 6})
topo.add_vertex('j', {'J': 3})
topo.add_vertex('k', {'K': 2})
topo.add_vertex('l1', {'L': 3})
topo.add_vertex('l2', {'L': 5})
