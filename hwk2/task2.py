import time
from collections import defaultdict
import math


def PageRank(G, insinks):
    """
    :param G: a graph stores outlinks
    :param insinks: a graph stores inlinks
    :return:
    """
    alpha = 0.85
    N = len(G)  # number of nodes in G
    PR = {}  # {'node': value}
    sink = set()  # set of all nodes without out links
    m = insinks  # {'node1': set{'node2', 'node3'}} nodes that links to nodes
    perplexity = []  # list of perplexity value

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
    j = 0
    while isConverge(j, perplexity, PR):
        print("iteration:", j+1, end=" ")
        calcprep(PR)
        prePR = PR
        PR = dict.fromkeys(prePR.keys(), 0)
        sinkPR = 0
        print(" perplexity:", perplexity[len(perplexity) - 1])

        # calculate total sink PR
        for node in sink:
            sinkPR += prePR.get(node)

        for node in p:
            PR[node] = (1.0 - alpha)/N
            PR[node] += alpha*sinkPR/N

            for q in m.get(node):
                PR[node] += alpha * prePR[q] / len(G.get(q))

        # check convergence
        # if not isConverge(j, perplexity, PR):
        #     break
        j += 1

    # write perplexity into txt file
    _id = 1
    fper = open("perplexity.txt", "w")
    for thing in perplexity:
        content = str("iter:" + str(_id) + "  perplexity: " + str(thing) + "\n")
        fper.write(content)
        _id += 1
    fper.close()
    print("file: perplexity.txt created")

    # write pagerank into txt file
    fpr = open("pagerank2.txt", "w")
    for thing in PR.items():
        content = str("node:"+str(thing[0])+" value:"+str(thing[1]) + "\n")
        fpr.write(content)
    fpr.close()
    print("file: pagerank2.txt created")

    # print(j)
    # print(perplexity)
    # return PR


# Function to calculate perplexity value.
def calcprep(PR):
    entropy = 0
    for page in PR.keys():
        entropy += PR[page]*math.log(1/PR[page], 2)
    return 2**entropy


# Function to find out if the perplexity values have converged or not.
def isConverge(j, perplexity, PR):
    perplexvalue = calcprep(PR)
    perplexity.append(perplexvalue)
    if len(perplexity) > 4:
        if abs(perplexity[j] - perplexity[j-1]) < 1.0 and abs(perplexity[j-1] - perplexity[j-2]) < 1.0 and \
                abs(perplexity[j-2] - perplexity[j-3]) < 1.0:

            print("final calculated perplexity", perplexvalue)
            print("iter ends at :", j)
            return False
        else:
            return True
    else:
        return True


def buildgraph(graph):
    # build graph from file

    G = {}

    # load graph from txt file
    fnode = open("vertices-edu.txt", "r")
    nodes = fnode.readlines()
    for line in nodes:
        line = line.split()
        G[line[0]] = line[1]
        graph[line[0]] = set()
    fnode.close()

    fedge = open("edges-edu.txt", "r")
    edges = fedge.readlines()

    for edge in edges:
        edge = edge.split()
        graph[edge[0]].add(edge[1])
    fedge.close()
    print("graph created")
    return graph


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

# graph = {
#     'A': {'B', 'C', 'F'},
#     'B': {'C', 'D', 'E', 'F'},
#     'C': {'D', 'E'},
#     'D': {'E', 'F', 'A', 'C'},
#     'E': ['A'],
#     'F': {'A', 'B', 'E'}
# }


def operate():
    s = time.time()
    graph = defaultdict(set)
    buildgraph(graph)
    m = initial_inlinks()
    PageRank(graph, m)
    # print(pr)

    e = time.time()
    print("time: ", e - s)

