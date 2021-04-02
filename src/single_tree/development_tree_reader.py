import glob
from src.single_tree.development_tree import TreeNode, Axis, Tree, NONE_NODE
import xml.etree.ElementTree as ElementTree

ns = {'b': 'http://bioinfweb.info/xmlns/xtg'}


# name is necessary for debug and input control
def parse_xml_node(xml, name, src_level, address, is_test_nodes):
    data = xml.find('b:Branch', ns).find('b:TextLabel', ns).attrib['Text'].replace(",", ".").lower().split(' ')

    node = TreeNode(address=address, src_level=src_level, left=NONE_NODE, right=NONE_NODE)

    if data[0] == 'ww':
        data[0] = 'w_in_w'
    if data[0] == 'wb':
        data[0] = 'b_in_w'

    assert data[0] == 'w' or data[0] == 'w_in_w' or data[0] == 'b', f"{name} : {data[0]}"  # wrong input

    assert len(data) == 2, f"name: {name}, data: {data}"  # error message on wrong input

    if data[1] == 'e':
        # chain item, no growth
        node.axis = Axis.LEAVE
    elif data[1] == 's':
        # chain item, no growth
        node.axis = Axis.GROWTH
        node.growth = 1
    else:
        try:
            # chain item, there is growth
            node.axis = Axis.GROWTH
            node.growth = float(data[1])
            assert node.growth >= 1
        except ValueError:
            if data[1] == "x":
                node.axis = Axis.X
            elif data[1] == "y":
                node.axis = Axis.Y
            elif data[1] == "z":
                node.axis = Axis.Z
                # print(f"Axis Z {name}")
            elif data[1] == "d" or data[1] == "xy":
                node.axis = Axis.DIAGONAL
                # print(f"diagonal {name}")
            elif data[1] == "a":
                node.axis = Axis.APOPTOSIS
            elif data[1] == "n":
                node.axis = Axis.NONE
                node.reduced_depth = 0
                node.leaves_number = 0
            else:
                assert False, f"wrong node description: '{data[0]} {data[1]}'. File: {name}, address: {address}"

    children = xml.findall('b:Node', ns)
    assert len(children) <= 2, f"name: {name}, children: {children}"

    # if no children - it's a leave:
    if len(children) == 0:
        if node.axis == Axis.LEAVE or node.axis == Axis.APOPTOSIS:
            pass # it's OK
        else:
            if node.axis == Axis.GROWTH:
                if not is_test_nodes and node.growth != 1.0:
                    node.axis = Axis.LEAVE
            else:
                if not is_test_nodes:
                    # it's OK in test_input - to draw X at the last level for illustration in the paper
                    assert False, f"invalid node type for 0 children: '{node.axis}'. File: {name}, address: {address}"

    if len(children) > 0:
        node.left = parse_xml_node(xml=children[0], name=name, src_level=src_level + 1, address=address + ".L", is_test_nodes=is_test_nodes)
    if len(children) > 1:
        node.right = parse_xml_node(xml=children[1], name=name, src_level=src_level + 1, address=address + ".R", is_test_nodes=is_test_nodes)

    return node


def parse_name_type(name_type):
    strings = name_type.split('_')  # ["Arabidopsis", "thaliana", "onagrad"]
    if len(strings) == 1:
        return strings[0], strings[0]
    if len(strings) == 3:
        [gen_name, sp_name, embryo_type] = strings
        return f"{gen_name}_{sp_name}", embryo_type
    return name_type, name_type


def read_tree_from_xml(filename, is_test_nodes):
    path = filename.split('/')
    # "../input/xtg/Arabidopsis_thaliana_onagrad.xtg" => "Arabidopsis_thaliana_onagrad"
    filename_type = path[len(path) - 1][:-4]
    (name, embryo_type) = parse_name_type(filename_type)

    root = parse_xml_node(xml=ElementTree.parse(filename).getroot().find('b:Tree', ns).find('b:Node', ns),
                          name=name, src_level=0, address="Z", is_test_nodes=is_test_nodes)

    return Tree(root, name=name, embryo_type=embryo_type)


def read_all_trees(pattern, is_test_nodes=False, max_level=11):
    # read source files
    filenames = glob.glob(pattern)
    if len(filenames) == 0:
        filenames = glob.glob(f"../../{pattern}")
    filenames.sort()
    src_trees = [read_tree_from_xml(filename, is_test_nodes) for filename in filenames]

    # it's very important to cut trees here, BEFORE reduce
    # Example: distance between chain_13 and chain_13_with_division_at_12 = 0
    # cut all to 11 (10, because it's 0-based) levels to ignore over_levels if we have 12 or 13 for some species
    # notice: zygote has level=0
    for src_tree in src_trees:
        src_tree.cut(max_level - 1)

        # Johansen trees have 4-7 levels, real trees have 11-13 levels (and should be cut to 11)
        # So cannot assert it
        #assert src_tree.depth == max_level - 1, f"{src_tree.name}, {src_tree.depth}"

    return src_trees
