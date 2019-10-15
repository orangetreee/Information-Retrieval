import operator

def operate():
    f = open("pagerank2.txt", "r")
    l = f.readlines()
    f.close()
    pagerank2 = dict()
    for thing in l:
        thing = thing.split()
        _node = thing[0][5:]
        _rankVal = float(thing[1][6:])
        # print(_node)
        # print(type(_rankVal))
        pagerank2[_node] = _rankVal

    sorted_pr2 = sorted(pagerank2.items(), key=operator.itemgetter(1), reverse=True)
    sorted_pr2_50 = dict()

    for i in range(50):
        sorted_pr2_50[sorted_pr2[i][0]] = sorted_pr2[i][1]
    f = open("vertices-edu.txt", "r")
    l = f.readlines()
    f.close()
    domain = dict()
    for thing in l:
        thing = thing.split()
        domain[thing[0]] = thing[1]


    f = open("task3_1.txt", "w")
    for i in sorted_pr2_50.keys():
        tsk3_1 = []
        tsk3_1.append(i)
        tsk3_1.append(domain.get(i))
        tsk3_1.append(sorted_pr2_50.get(i))
        tmp = str(str(tsk3_1[0]) + " " + str(tsk3_1[1]) + "\t" + str(tsk3_1[2]) + "\n")
        f.write(tmp)
    f.close()




