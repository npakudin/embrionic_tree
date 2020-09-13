def prepare_trees(trees, max_level=10, is_reducing=True):
    for tree in trees:
        # print(f"prepare {tree.name}")

        # cut all to 11 (10, because it's 0-based) levels to ignore overlevels if we have 12 or 13 for some species
        # notice: zygote has level=0
        tree.cut(max_level=10)

        if is_reducing:
            tree.reduce()
        tree.prepare()
        tree.cut(max_level=max_level)


# 'Arabidopsis_thaliana' => 'A. thaliana'
def short_sp_name(name):
    underscore_index = name.find('_')

    personal_name = name[underscore_index + 1:]
    return f"{name[0]}._{personal_name}"
