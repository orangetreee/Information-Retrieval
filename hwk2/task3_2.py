from collections import defaultdict
import operator


# build dict with all inlinks
def initial_inlinks():
    m = defaultdict(set)
    fnode = open("vertices-edu.txt", "r")
    nodes = fnode.readlines()  # {"node", set()}
    for line in nodes:
        line = line.split()
        m[line[0]] = set()
    fnode.close()

    fedge = open("edges-edu.txt", "r")
    edges = fedge.readlines()

    for edge in edges:
        edge = edge.split()
        m[edge[1]].add(edge[0])
    fedge.close()
    print("inlinks initialized")
    return m


def operate():
    # m is the dict of all inlinks
    m = initial_inlinks()
    inlink_count = dict()
    for key, value in m.items():
        inlink_count[key] = len(value)

    # sort inlinks and get top 50
    sorted_inlink = sorted(inlink_count.items(), key=operator.itemgetter(1))
    sorted_inlink = sorted_inlink[::-1]
    sorted_inlink_50 = dict()
    for i in range(50):
        sorted_inlink_50[sorted_inlink[i][0]] = sorted_inlink[i][1]

    # get all {node: domain}
    f = open("vertices-edu.txt", "r")
    l = f.readlines()
    f.close()
    node = dict()  # {id: domain}
    for thing in l:
        thing = thing.split()
        node[thing[0]] = thing[1]

    # write file
    f = open("task3_2.txt", "w")
    for key, value in sorted_inlink_50.items():
        tmp = []
        tmp.append(str(key))
        tmp.append(str(node.get(key)))
        tmp.append(str(value))
        f.write(str(tmp[0] + "\t" + tmp[1] + "\t" + tmp[2] + "\n"))
    f.close()
    print("task3_2.txt created")


