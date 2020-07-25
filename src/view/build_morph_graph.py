import xml.etree.ElementTree as ElementTree

xml_ns = {'b': 'http://bioinfweb.info/xmlns/xtg'}


def taxon_from_xml(filename):
    with open(filename, "r") as f:
        xml_tree = ElementTree.parse(filename)
        root = xml_tree.getroot()
        path = filename.split('/')
        name = path[len(path) - 1][:-4]

        taxon = Taxon(xml=root.find('b:Tree', xml_ns).find('b:Node', xml_ns))
        return taxon


# work if start from the same depth only!
def find_common_ancestor_level(t1, t2):
    # print(f"find_common_ancestor_level {t1.name} / {t1.parent} =?= {t2.name} / {t2.parent}")
    if t1 == t2:
        return 0
    else:
        if t1.parent is None or t2.parent is None:
            print(f"No parent for one of {t1.name} and {t2.name}")
        return 1 + find_common_ancestor_level(t1.parent, t2.parent)


class Taxon:
    def __init__(self, xml, level=0):
        xml_name = xml.find('b:Branch', xml_ns).find('b:TextLabel', xml_ns).attrib['Text']
        xml_children = xml.findall('b:Node', xml_ns)

        self.index = None
        self.level = level
        self.name = xml_name.replace(" ", "_")
        self.children = []
        self.necessary = None
        self.parent = None
        for xml_child in xml_children:
            child = Taxon(xml_child, level + 1)
            self.children.append(child)

        self.set_parents()

    def internal_leave_only_marked(self):
        ch = list(filter(lambda x: x.necessary, self.children))
        self.children = ch

        for child in self.children:
            child.internal_leave_only_marked()

    # remove all leaves excluding with names
    def leave_only_names(self, names):
        self.mark_names(names)
        self.set_parents_necessarity()
        self.internal_leave_only_marked()

    def mark_names(self, names, mark_all_children=False):
        self.necessary = mark_all_children or (self.name in names)
        for child in self.children:
            child.mark_names(names, self.necessary)

    def set_parents_necessarity(self):
        if self.necessary:
            self.mark_parents()
        for child in self.children:
            child.set_parents_necessarity()

    def mark_parents(self):
        if self.parent is not None and self.parent.necessary != True:
            self.parent.necessary = True
            self.parent.mark_parents()

    def calculate(self):
        leaves = self.get_leaves()
        for i, leave in enumerate(leaves):
            leave.index = i

        distances = []
        for i, leave1 in enumerate(leaves):
            distances.append([])
            leaves2 = self.get_leaves()
            for j, leave2 in enumerate(leaves2):
                distances[i].append(find_common_ancestor_level(leave1, leave2))
        return distances

    def get_leaves(self):
        if len(self.children) == 0:
            return [self]

        res = []
        for child in self.children:
            res += child.get_leaves()
        res = sorted(res, key=lambda x: x.name)
        return res

    def set_parents(self):
        self.parent = None
        self.private_set_parents()

    def private_set_parents(self):
        for child in self.children:
            child.parent = self
            child.private_set_parents()

    def to_str(self, level):
        res = ""
        pad = "\n" + ("  " * level)
        res += pad + "name: " + str(self.name)
        res += pad + "necessary: " + str(self.necessary)
        if self.index is not None:
            res += pad + "index: " + str(self.index)
        res += pad + ("!" if len(self.children) == 0 else "") + "level: " + str(self.level)
        if len(self.children) > 0:
            pad + "children: "
            for child in self.children:
                res += child.to_str(level + 1)
        return res

    def __str__(self):
        return self.to_str(0)
