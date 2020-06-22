import glob
from src.compare_trees.development_tree import TreeNode, Axis
import xml.etree.ElementTree as ElementTree

ns = {'b': 'http://bioinfweb.info/xmlns/xtg'}


def parse_xml_node(xml, name, src_level, address):
    data = xml.find('b:Branch', ns).find('b:TextLabel', ns).attrib['Text'].replace(",", ".").lower().split(' ')

    node = TreeNode(name = name, address = address, src_level = src_level)

    if data[0] == 'ww':
        data[0] = 'w_in_w'
    if data[0] == 'wb':
        data[0] = 'b_in_w'

    # if data[0] != 'w' and data[0] != 'b':
    #     print(f"{name} : {data[0]}") # error message on wrong input

    assert len(data) == 2, f"name: {name}, data: {data}" # error message on wrong input

    if data[1] == 's' or data[1] == 'e':
        # chain item, no growth
        node.axis = Axis.NONE
        node.growth = 1
    else:
        try:
            # chain item, there is growth
            node.axis = Axis.NONE
            node.growth = float(data[1])
            assert node.growth >= 1
        except:
            if data[1] == "x":
                node.axis = Axis.X
            elif data[1] == "y":
                node.axis = Axis.Y
            elif data[1] == "z":
                node.axis = Axis.Z
            elif data[1] == "d" or data[1] == "xy":
                node.axis = Axis.DIAGONAL
            else:
                assert False, f"wrong node description: '{data[0]} {data[1]}' in file: {name}, address: {address}"

    children = xml.findall('b:Node', ns)
    assert len(children) <= 2, f"name: {name}, children: {children}"

    # if no children - it's a leave
    if len(children) == 0:
        node.axis = Axis.LEAVE

    if len(children) > 0:
        node.left = parse_xml_node(xml=children[0], name=name, src_level=src_level + 1, address=address + ".L")
    if len(children) > 1:
        node.right = parse_xml_node(xml=children[1], name=name, src_level=src_level + 1, address=address + ".R")

    return node


def read_tree_from_xml(filename):
    path = filename.split('/')
    name = path[len(path) - 1][:-4]  # "../input/xtg/Arabidopsis_thaliana.xtg" => "Arabidopsis_thaliana"

    node = parse_xml_node(xml=ElementTree.parse(filename).getroot().find('b:Tree', ns).find('b:Node', ns),
                          name=name, src_level=0, address="Z")

    return node


def read_all_trees(pattern, max_levels):
    # read source files
    filenames = glob.glob(pattern)
    filenames.sort()
    src_trees = [read_tree_from_xml(filename) for filename in filenames]

    # cut to max_levels and assert, that all files has at least 11 levels
    for src_tree in src_trees:
        src_tree.cut(max_levels - 1)

        #assert src_tree.depth == max_levels - 1, f"{src_tree.name}, {src_tree.depth}"

    return src_trees
