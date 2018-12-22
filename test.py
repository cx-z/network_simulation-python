class Node:
    def __init__(self):
        self.name = ""
        self.nextHop = self

    def route(self, node_list):
        self.nextHop = node_list[node_list.index(self)+1]

    def judge(self):
        if self.nextHop != self:
            print("true")
        else:
            print("false")


if __name__ == "__main__":
    A = Node()
    B = Node()
    A.name = "A"
    B.name = 'B'
    nodeList = [A, B]
    #A.route(nodeList)
    A.judge()
