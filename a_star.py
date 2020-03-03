import matplotlib.pyplot as plt
import sys
import math
import time

plt.ion()


def readLocations(locations_filepath):
    # print("in locations")
    f1 = open(locations_filepath, "r")
    nodes = []
    coordinates = []
    t = f1.readlines()
    for i in range(0, len(t)):
        l = t[i]
        if l != "END":
            tokens = l.split()
            nodes.append(tokens[0])
            dist = []
            dist1 = int(tokens[1])
            dist2 = int(tokens[2])
            dist.append(dist1)
            dist.append(dist2)
            coordinates.append(dist)
    new_nodes, new_coor = sortNodes(nodes, coordinates)
    list2d = readConnections("connections.txt", new_nodes)
    return new_nodes, new_coor, list2d


def sortNodes(nodes, coordinates):
    m = {}
    for i in range(0, len(nodes)):
        m.update({nodes[i]: coordinates[i]})
    a = sorted(m.items())
    l1 = []
    l2 = []
    for i in range(0, len(a)):
        key, value = a[i]
        l1.append(key)
        l2.append(value)
    nodes = l1.copy()
    coordinates = l2.copy()
    return nodes, coordinates


def initialize2dList(length):
    list2d = [[False] * length for i in range(length)]
    return list2d


def readConnections(connections_filepath, nodes):
    f2 = open(connections_filepath, "r")
    list2d = initialize2dList(len(nodes))
    t1 = f2.readlines()
    for i in range(0, len(t1)):
        if t1[i] != "END":
            toks = t1[i].split()
            node = toks[0]
            index = nodes.index(node)
            for j in range(2, len(toks)):
                neighbor_node = toks[j]
                idx = nodes.index(neighbor_node)
                list2d[index][idx] = True
                list2d[idx][index] = True
    return list2d


# this is for debugging
def test(list2d, nodes):
    for i in range(0, len(nodes)):
        # print()
        pass
    return


def neighbors(st_node, nodes, list2d, ex_list):
    # print("in neighbors")
    altpaths = []
    for i in range(0, len(nodes)):
        if list2d[st_node][i]:
            # print(nodes[i])
            if nodes[i] not in ex_list:
                altpaths.append(i)
    return altpaths


def discoverpath(par, curr):
    # print("in discoverpath")
    p = []
    p.append(curr)
    while par[curr] != -sys.maxsize - 1:
        curr = par[curr]
        p.append(curr)
    p.reverse()
    return p


def find_distance(st_nodei, en_nodei, coordinates, op2):
    # print("in distance")
    if op2 == 2:
        return 1
    else:
        return math.sqrt(pow(abs(coordinates[st_nodei][0] - coordinates[en_nodei][0]), 2) + pow(
            abs(coordinates[st_nodei][1] - coordinates[en_nodei][1]), 2))


def printpaths(allpaths, nodes, coordinates, op2):
    # print("in output {}".format(allpaths))
    if len(allpaths) == 0:
        print("no path exists from start to end with selected options")
    for i in range(0, len(allpaths)):
        p = allpaths[i]
        t = 0
        print("**********************************************************************")
        print()
        for j in range(0, len(p) - 1):
            d = find_distance(p[j], p[j + 1], coordinates, op2)
            t = t + d
            print("{} to {} length {}".format(nodes[p[j]], nodes[p[j + 1]], d))
        print("total path length {}".format(t))
        print()
        print("**********************************************************************")


def initialize_dist(nodes):
    return [sys.float_info.max] * len(nodes)


def ani_nodes(coordinates, nodes):
    plt.title("Nodes that are available and their Connectivity")
    for i in range(0, len(nodes)):
        x = coordinates[i][0]
        y = coordinates[i][1]
        plt.plot(x, y, marker='o', color='r')
        plt.text(x + 5, y + 5, nodes[i], color='black')


def ani_connections(list2d, coordinates, nodes):
    nl = list2d.copy()
    for i in range(0, len(nodes)):
        for j in range(0, len(nodes)):
            if nl[i][j]:
                x1 = coordinates[i][0]
                y1 = coordinates[i][1]
                x2 = coordinates[j][0]
                y2 = coordinates[j][1]
                plt.plot([x1, x2], [y1, y2], color='black', lw=0.3)
    plt.draw()
    plt.pause(0.5)


def initialize_est(nodes):
    return [sys.float_info.max] * len(nodes)


def animate1(coordinates, nodes, start, end):
    for i in range(0, len(nodes)):
        x = coordinates[i][0]
        y = coordinates[i][1]
        if start == i:
            plt.plot(x, y, marker='8', color='green', markersize=8)
        elif end == i:
            plt.plot(x, y, marker='*', color='green', markersize=14)
        else:
            plt.plot(x, y, marker='o', color='r')
        plt.text(x + 5, y + 5, nodes[i], color='black')


def animate2(list2d, coordinates, nodes):
    nl = list2d.copy()
    for i in range(0, len(nodes)):
        for j in range(0, len(nodes)):
            if nl[i][j]:
                x1 = coordinates[i][0]
                y1 = coordinates[i][1]
                x2 = coordinates[j][0]
                y2 = coordinates[j][1]
                plt.plot([x1, x2], [y1, y2], color='black', lw=0.3)


def get_neighbors(node, coordinates, list2d, nodes, vis):
    l = []
    for i in range(0, 29):
        if list2d[node][i]:
            if i in vis:
                continue
            l.append(i)
    return l


def anim(paths, nodes, list2d, coordinates):
    if len(paths) == 0:
        return
    plt.clf()
    plt.title("final path")
    animate1(coordinates, nodes, paths[0], paths[len(paths) - 1])
    animate2(list2d, coordinates, nodes)
    plt.draw()
    x = []
    y = []
    for i in range(0, len(paths)):
        x.append(coordinates[paths[i]][0])
        y.append(coordinates[paths[i]][1])
    plt.plot(x, y, color='green', lw=3)
    plt.draw()
    plt.pause(5)


def initialize_prev(nodes):
    d = initialize_dist(nodes)
    e = initialize_est(nodes)
    return [-sys.maxsize - 1] * len(nodes),d,e


def plot_neighbors(par, l, coordinates, nodes, vis):
    # print("par {} l{} vis{}".format(par,l,vis))
    x1 = coordinates[par][0]
    y1 = coordinates[par][1]
    plt.pause(0.5)
    for i in range(0, len(l)):
        if l[i] in vis:
            continue
        x2 = coordinates[l[i]][0]
        y2 = coordinates[l[i]][1]
        plt.plot([x1, x2], [y1, y2], color='green', linestyle='dashed', lw=2)
        plt.draw()
    plt.pause(0.5)
    plt.plot(x1, y1, marker='o', color='red')
    # plt.pause(1)
    plt.draw()


def get_parent(sel, dic):
    return dic.get(sel)


def plot_selected(sel, coordinates, dic, nodes, list2d, vis, en_nodei):
    par = get_parent(sel, dic)
    x1 = coordinates[par][0]
    y1 = coordinates[par][1]
    x2 = coordinates[sel][0]
    y2 = coordinates[sel][1]
    plt.plot(x2, y2, marker='o', color='blue')
    plt.draw()
    plt.pause(0.5)
    plt.plot([x1, x2], [y1, y2], color='red', lw=2.3)
    #plt.draw()
    plt.pause(0.5)
    if sel != en_nodei:
        plot_neighbors(sel, get_neighbors(sel, coordinates, list2d, nodes, vis), coordinates, nodes, vis)
        plt.draw()
        plt.pause(0.5)


def initialize_par(nodes):
    l = [[False] * len(nodes) for i in range(len(nodes))]
    return l


def set_parents(dic, par, l, vis1):
    for i in range(0, len(l)):
        if l[i] not in vis1:
            dic.update({l[i]: par})
            vis1.append(l[i])


def minimum_node(op, est_distance):
    s = op[0]
    est = est_distance[s]
    min = 0
    i = 0
    while i < len(op):
        c_est = est_distance[op[i]]
        if c_est < est:
            est = c_est
            min = i
        i = i + 1
    return min


def a_star(st_nodei, en_nodei, nodes, coordinates, opt1, ex_list, allpaths, list2d, op2):
    test(list2d, nodes)
    animate1(coordinates, nodes, st_nodei, en_nodei)
    animate2(list2d, coordinates, nodes)
    plt.title("process")
    line1, = plt.plot([], [], label='path selected', color='red')
    line2, = plt.plot([], [], label='cities where to travel', color='green', linestyle='dashed')

    l1 = plt.legend(handles=[line1], loc='lower left', bbox_to_anchor=(0.7, 1.05), ncol=2,
                    borderaxespad=0, frameon=False)
    ax = plt.gca().add_artist(l1)
    l2 = plt.legend(handles=[line2], loc='lower left', bbox_to_anchor=(0.7, 1), ncol=2,
                    borderaxespad=0, frameon=False)
    ax = plt.gca().add_artist(l2)
    plt.draw()

    t = []
    op = []
    vis = []
    par, dist_travel, est_distance = initialize_prev(nodes)
    vis1 = []
    op1 = []
    dic = {}
    
    op.append(st_nodei)

    

    dist_travel[st_nodei] = 0
    est_distance[st_nodei] = find_distance(st_nodei, en_nodei, coordinates, op2)

    # print(est_distance[st_nodei])

    while len(op) > 0:
        # print("in while")
        mi_node = minimum_node(op, est_distance)
        curr = op[mi_node]
        vis.append(curr)
        l = neighbors(curr, nodes, list2d, ex_list)
        set_parents(dic, curr, l, vis1)
        # print("here")
        if opt1 == 2:
            print()
            print("city selected {}".format(nodes[curr]))
            print()

        if curr == st_nodei:
            dic.update({curr: curr})
            plot_selected(curr, coordinates, dic, nodes, list2d, vis, en_nodei)
            plt.draw()
            plt.pause(0.5)
        else:
            plot_selected(curr, coordinates, dic, nodes, list2d, vis, en_nodei)
            plt.draw()
            plt.pause(0.5)
        if curr == en_nodei:

            allpaths.append(discoverpath(par, curr))

            if opt1 == 2:
                op.remove(op[mi_node])
                print("possible cities where to travel", end=" ")
                for i in range(0, len(l)):
                    print("{} ".format(nodes[l[i]]), end=" ")
                print("\n")
                print("cities at the end of possible paths", end=" ")
                for j in range(0, len(op)):
                    print("{}({}) ".format(nodes[op[j]], est_distance[op[j]]), end=" ")
                print("\n")
            return allpaths

        op.remove(op[mi_node])
        test(list2d,
             nodes)
        op1.append(curr)
        for i in range(0, len(l)):
            # print("in 4 for loop")
            try:
                ex_list.index(l[i])
            except:
                pass
            else:
                if ex_list.index(l[i]) > -1:
                    continue

            try:
                op1.index(l[i])
            except:
                pass
            else:
                continue
            d1 = dist_travel[curr]
            d2 = find_distance(curr, l[i], coordinates, op2)
            t_dist = d1+d2

            try:
                op.index(l[i])
            except:

                op.append(l[i])
            else:
                if t_dist >= dist_travel[l[i]]:
                    continue
            node = l[i]
            par[node] = curr
            dist_travel[l[i]] = t_dist
            d3 = dist_travel[l[i]]
            d4 = find_distance(l[i], en_nodei, coordinates, op2)
            est_distance[l[i]] = d3+d4
        if opt1 == 2:
            print("possible cities where to travel: ", end=" ")
            for i in range(0, len(l)):
                print("{} ".format(nodes[l[i]]), end=" ")
            print("\n")
            print("cities at the end of possible paths: ", end=" ")

            for j in range(0, len(op)):
                print("{}({})".format(nodes[op[j]], est_distance[op[j]]), end=" ")
            print("\n")
            print("**********************************************************************")

    return allpaths


# main function
def main():
    # read locations file
    nodes, coordinates, list2d = readLocations("locations.txt")
    print("look at the plot for available nodes and their connectivity")
    ani_nodes(coordinates, nodes)
    ani_connections(list2d, coordinates, nodes)
    # print("nodes available are")
    # print(nodes)

    # enter staring node
    print("enter starting node")
    while 1:
        st_node = input()
        if st_node not in nodes:
            print("enter a node from the available nodes")
        else:
            break
    # enter ending node
    print("enter ending node")
    while 1:
        en_node = input()
        if en_node not in nodes:
            print("enter a node from the available nodes")
        elif en_node == st_node:
            print("start and end nodes cannot be same, enter another node")
        else:
            break
    ex_list = []
    allpaths = []
    print("do you want to exclude some nodes? press y for yes or n for no")
    yn = input()
    while yn != "n":
        print("enter node you want to exclude")
        en = input()
        if en not in nodes:
            print("enter a node you want to exclude from available nodes")
        if en == st_node or en == en_node:
            print("enter nodes other than staring or ending nodes")
            en = input()
        ex_list.append(en)
        print("do you want to exclude some more nodes? press y for yes, n for no")
        yn = input()
    print("press 1 for final output")
    print("press 2 for step by step")
    op1 = int(input())
    print("press 1 for straight line heuristic")
    print("press 2 for fewest cities heuristic")
    op2 = int(input())
    plt.clf()
    paths = a_star(nodes.index(st_node), nodes.index(en_node), nodes, coordinates, op1, ex_list, allpaths, list2d, op2)
    printpaths(paths, nodes, coordinates, op2)
    if len(paths) != 0:
        anim(paths[0], nodes, list2d, coordinates)


if __name__ == '__main__':
    main()