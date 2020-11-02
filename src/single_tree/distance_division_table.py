from src.single_tree.development_tree import Axis, dist_div

axes = [(name, value) for name, value in vars(Axis).items() if not name.startswith('_')]

print(f"-", end='')
for (name, value) in axes:
    print(f"   {name[0]}", end='')

for (name1, value1) in axes:
    print(f"\n{name1[0]}", end='')
    for (name2, value2) in axes:
        dist = dist_div(value1, value2)
        if isinstance(dist, int):
            print(f"   {dist}", end='')
        else:
            print(f" {dist:0.1f}", end='')
