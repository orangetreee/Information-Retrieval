from collections import defaultdict
from task2 import initial_inlinks
from task2 import buildgraph


def operate():
    inlinks = initial_inlinks()
    graph = defaultdict(set)
    outlinks = buildgraph(graph)


    tsk3 = open("tsk3_345.txt", "w")
    # Q3
    noInLinkNum = 0
    for node, link in inlinks.items():
        if len(link) == 0:
            noInLinkNum += 1
    print("proportion of no inlinks: ", noInLinkNum / len(inlinks) * 100, " %")
    tsk3.write("proportion of no inlinks: " + str(noInLinkNum / len(inlinks) * 100) + " %" + "\n")

    # Q4
    noOutLinkNum = 0
    for node, link in outlinks.items():
        if len(link) == 0:
            noOutLinkNum += 1
    print("proportion of no outlinks: ", noOutLinkNum / len(outlinks) * 100, "%")
    tsk3.write("proportion of no outlinks: " + str(noOutLinkNum / len(outlinks) * 100) + "%" + "\n")

    # Q5
    f = open("pagerank2.txt", "r")
    l = f.readlines()
    f.close()
    lessThanInitialNum = 0
    initial = 1 / len(outlinks)
    for thing in l:
        thing = thing.split()
        # _node = str(thing[0][5:])
        _rankVal = float(thing[1][6:])
        if _rankVal < initial:
            lessThanInitialNum += 1
    print("proportion of PageRank that less than initial: ", lessThanInitialNum / len(outlinks) * 100, "%")
    tsk3.write("proportion of PageRank that less than initial: " + str(lessThanInitialNum / len(outlinks) * 100) + "%")
