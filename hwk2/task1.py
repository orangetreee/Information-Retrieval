from collections import defaultdict


def PageRank(G, iterations, nodePre):
    """
    :param G: directed graph
    :return: dict in {'node': rank value}
    """
    alpha = 0.85
    tol = 1.0e-6
    N = len(G)  # number of nodes in G
    PR = {}  # {'node': value}
    sink = set()  # set of all nodes without out links
    m = dict()  # {'node1': set{'node2', 'node3'}} nodes that links to nodes

    if len(G) == 0:
        return {}

    # initialization
    # p is the set of all nodes
    p = G.keys()
    for node in p:
        PR[node] = 1/N
        #  add sink p into set sink
        if len(G.get(node)) == 0:
            sink.add(node)

    # initialize m
    for node in p:
        tmp = set()
        for i in p:
            if G.get(i).__contains__(node):
                tmp.add(i)
        m[node] = tmp
    # print(m)

    file = open("task1.txt", "a")
    file.write("\ntotal iterations: " + str(iterations) + "\n")
    print("\ntotal iterations: ", iterations)
    while iterations > 0:
        prePR = PR
        PR = dict.fromkeys(prePR.keys(), 0)
        sinkPR = 0

        # calculate total sink PR
        for node in sink:
            sinkPR += prePR.get(node)

        for node in p:
            PR[node] = (1.0 - alpha)/N
            PR[node] += alpha*sinkPR/N

            for q in m.get(node):
                PR[node] += alpha * prePR[q] / len(G.get(q))

        # # check convergence
        # err = sum([abs(PR[n] - prePR[n]) for n in PR])
        # if err < N * tol:
        #     return PR
        #     # printRes(PR)
        #     # break
        #
        iterations -= 1

    printRes(PR, file, nodePre)


def printRes(pr, file, nodePre):
    _id = 0
    for thing in pr.items():
        content = str("id:"+str(_id)+" node:"+str(nodePre.get(thing[0]))+" value"+str(thing[1]) + "\n")
        file.write(content)
        print("id:", _id, " node:", nodePre[thing[0]], " value:", thing[1])
        _id += 1
    file.close()

def operate():
    # graph = {
    #     'A': {'B', 'C', 'F'},
    #     'B': {'C', 'D', 'E', 'F'},
    #     'C': {'D', 'E'},
    #     'D': {'E', 'F', 'A', 'C'},
    #     'E': {'A'},
    #     'F': {'A', 'B', 'E'}
    # }
    node = {}  # {id: name}
    graph =  defaultdict(set) # {id: {id}}
    fnode = open("node.txt", "r")
    l = fnode.readlines()
    for i in l:
        i = i.split()
        node[i[0]] = (i[1])
        print(node)

    fedge = open("edge.txt", "r")
    l = fedge.readlines()
    for i in l:
        i = i.split()
        graph[i[0]].add(i[1])

    file = open("task1.txt", "w")
    file.close()
    iterations = [1, 10, 100]
    for i in iterations:
        pr = PageRank(graph, i, node)
        # print(pr)
