class Data:
    def __init__(self):
        self.edge = dict()
        self.edge_all = dict()


class Node:
    _data = None

    @classmethod
    def set_data(cls, data):
        cls._data = data

    @classmethod
    def get_data(cls):
        if cls._data is None:
            cls._data = Data()
        return cls._data

    def __init__(self, name):
        self.name = name
        self.link_map = dict()

    def link(self, node2):
        self_node_port = NodePort(self.name, "%s->%s" % (self.name, node2.name))
        node2_port = NodePort(node2.name, "%s->%s" % (node2.name, self.name))
        self.link_map[self_node_port.port] = node2
        node2.link_map[node2_port.port] = self

        data = Node.get_data()
        data.edge[self_node_port] = node2_port
        data.edge_all[self_node_port] = node2_port
        data.edge_all[node2_port] = self_node_port


class NodePort:
    def __init__(self, node, port):
        self.node = node
        self.port = port

