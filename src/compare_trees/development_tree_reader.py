import glob
from src.compare_trees.development_tree import Tree, TreeNode
import xml.etree.ElementTree as ElementTree

ns = {'b': 'http://bioinfweb.info/xmlns/xtg'}


def parse_xml_node(xml, filename, cell_timer, address):
    data = xml.find('b:Branch', ns).find('b:TextLabel', ns).attrib['Text'].replace(",", ".").lower().split(' ')

    node = TreeNode()
    node.name = filename
    node.address = address

    if data[0] == 'ww':
        data[0] = 'w_in_w'
    if data[0] == 'wb':
        data[0] = 'b_in_w'
        node.z = data[0]

    # error message on wrong input
    assert len(data) == 2, f"filename: {filename}, data: {data}"

    if data[1] == 'e':
        node.axis = 'L'  # leave
        # pass
    else:
        if data[1] == 's':
            # chain item, no growth
            node.axis = 'None'
            node.growth = 1
        else:
            try:
                # chain item, there is growth
                node.axis = 'None'
                node.growth = float(data[1])
                assert node.growth >= 1
            except:
                node.axis = data[1] # axis of division x or y
                #print(node.axis)
                assert any(node.axis == x for x in ['x', 'y', 'd']), f"filename={filename}"
    children = xml.findall('b:Node', ns)
    assert len(children) <= 2, f"filename: {filename}, children: {children}"
    if len(children) > 0:
        node.left = parse_xml_node(xml=children[0], filename=filename, cell_timer=cell_timer + 1, address=address + ".L")
    if len(children) > 1:
        node.right = parse_xml_node(xml=children[1], filename=filename, cell_timer=cell_timer + 1, address=address + ".R")

    return node


def read_tree_from_xml(filename):
    path = filename.split('/')
    name = path[len(path) - 1][:-4]  # "../input/xtg/Arabidopsis_thaliana.xtg" => "Arabidopsis_thaliana"

    node = parse_xml_node(xml=ElementTree.parse(filename).getroot().find('b:Tree', ns).find('b:Node', ns),
                          filename=filename, cell_timer=0, address="Z")

    tree = Tree(root=node, name=name)

    return tree


def read_all_trees(pattern, max_levels):
    # read source files
    filenames = glob.glob(pattern)
    filenames.sort()
    src_trees = [read_tree_from_xml(filename) for filename in filenames]

    # cut to max_levels and assert, that all files has at lease 11 levels
    for src_tree in src_trees:
        src_tree.root.cut(max_levels - 1)

        assert src_tree.root.depth == max_levels - 1, f"{src_tree.name}, {src_tree.root.depth}"

    return src_trees
