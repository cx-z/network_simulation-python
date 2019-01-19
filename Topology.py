import Route


address_list = ['A', 'B', 'C', 'D', 'E']

topo = Route.Graph()
topo.add_vertex('A', {'B': 5, 'C': 5, 'D': 5})
topo.add_vertex('B', {'A': 5, 'E': 5, 'C': 5})
topo.add_vertex('C', {'A': 5, 'E': 5, 'B': 5})
topo.add_vertex('D', {'A': 5, 'E': 5})
topo.add_vertex('E', {'B': 5, 'C': 5, 'D': 5})

logic_link = []  # 所有的逻辑连接
for i in range(len(address_list)):
    for j in range(len(address_list)):
        if i != j:
            logic_link.append({address_list[i]: address_list[j]})

route_table = []  # 全局路由表
for item in logic_link:
    for key in item:
        shortest_path, length = Route.Graph.get_shortest_path(topo, key, item[key])
        shortest_path.reverse()
        shortest_path.append(length)
        route_table.append(shortest_path)  # 生成所有逻辑连接的最短路

if __name__ == "__main__":
    print(logic_link)
    print(route_table)
