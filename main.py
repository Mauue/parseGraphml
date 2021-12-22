from xml.dom.minidom import parse
import xml.dom.minidom
import os
from element import Node, Data

GEN_FILE_EXTENSION = ".topology"
DIRNAME = r""
OUT_DIRNAME = r""


def parse_file(filename):
    key_for_node_map = dict()
    node_map = dict()
    collection = _get_dom(filename)
    key_element_list = collection.getElementsByTagName("key")
    node_element_list = collection.getElementsByTagName("node")
    edge_element_list = collection.getElementsByTagName("edge")
    for key in key_element_list:
        if key.getAttribute("for") != "node":
            continue
        key_id = key.getAttribute("id")
        key_name = key.getAttribute("attr.name")
        key_for_node_map[key_id] = key_name
    for node_element in node_element_list:
        name = ""
        id = ""
        for data_element in node_element.getElementsByTagName("data"):
            if key_for_node_map[data_element.getAttribute("key")] == "label":
                name = "-".join(data_element.firstChild.data.split(" "))
            elif key_for_node_map[data_element.getAttribute("key")] == "id":
                id = data_element.firstChild.data
        node_map[id] = Node(name)
    for edge_element in edge_element_list:
        source = edge_element.getAttribute("source")
        target = edge_element.getAttribute("target")
        source_node = node_map.get(source)
        target_node = node_map.get(target)
        source_node.link(target_node)


def parse_files(dirname, out_dirname):
    for filename in os.listdir(dirname):
        fl = filename.split(".")
        if len(fl) > 1 and fl[1] == "graphml":
            Node.set_data(Data())
            parse_file(os.path.join(dirname, filename))
            gen_topology_file(os.path.join(out_dirname, filename.split(".")[0] + GEN_FILE_EXTENSION))


def gen_topology_file(filename):
    data = Node.get_data()
    with open(filename, mode="w", encoding="utf-8") as f:
        for np1, np2 in data.edge.items():
            f.write(np1.node + " " + np1.port + " " + np2.node + " " + np2.port + "\n")


def _get_dom(filename) -> xml.dom.minidom.Element:
    dom_tree = parse(filename)
    return dom_tree.documentElement


if __name__ == "__main__":
    for i in range(1, 13):
        parse_files(DIRNAME+str(i), OUT_DIRNAME+str(i))

