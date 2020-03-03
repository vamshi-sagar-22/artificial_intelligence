import math

#this function is to read locations file
def readLocations(locations_filepath):
    #print("in locations")
    f1 = open(locations_filepath,"r")
    nodes = []
    coordinates = []
    t = f1.readlines()
    for i in range(0,len(t)):
        l = t[i]
        if l!="END":
            tokens = l.split()
            nodes.append(tokens[0])
            dist = []
            dist1 = int(tokens[1])
            dist2 = int(tokens[2])
            dist.append(dist1)
            dist.append(dist2)
            coordinates.append(dist)
    sortNodes(nodes,coordinates)
    list2d = readConnections("connections.txt", nodes)
    return nodes,coordinates,list2d


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

#this function creates a 2d list to store neighbors
def initialize2dList(length):
    list2d = [[False]*length for i in range(length)]
    return list2d

#this function is to read connections file
def readConnections(connections_filepath,nodes):
    f2 = open(connections_filepath,"r")
    #initialize a 2 dimensional list to store neighbors of a node
    list2d = initialize2dList(len(nodes))
    t1 = f2.readlines()
    for i in range(0,len(t1)):
        if t1[i]!="END":
            toks = t1[i].split()
            node = toks[0]
            index = nodes.index(node)
            for j in range(2,len(toks)):
                neighbor_node = toks[j]
                idx = nodes.index(neighbor_node)
                #update the neighbors in 2d list
                list2d[index][idx]= True
                list2d[idx][index]= True
    return list2d

#this function is for debugging
def test(list2d,nodes):
    for i in range(0,len(nodes)):
        #print()
        pass
    return


def printpaths(nodes,coordinates,allpaths,st_node,en_node):
    print("all dfs paths from {} to {} are".format(st_node,en_node))
    p = []
    print(allpaths)
    for i in range(0,len(allpaths)):
        print("\n")
        p = allpaths[i]
        t=0
        for j in range(0,len(p)-1):
            node1 = p[j]
            node2 = p[j+1]
            l1 = nodes[node1]
            l2 = nodes[node2]
            #now find the length between two nodes
            d = math.sqrt(pow(abs(coordinates[p[j]][0]-coordinates[p[j+1]][0]),2)+pow(abs(coordinates[p[j]][1]-coordinates[p[j+1]][1]),2))
            t = t+d
            print("{} to {} length {}".format(l1,l2,d))
        print("Total path length {}".format(t))
        #print("\n")



#this is the function to calculate all paths from source to destination using dfs
def dfspath(st_node,en_node,vis,nodes,list2d,allpaths):
    #test(list2d,nodes)
    #find other paths between two nodes
    otp = []
    l = 0
    s = len(nodes)
    while l < s:
        if (list2d[st_node][l]):
            try:
                vis.index(l)
            except:
                otp.append(l)
        l = l + 1
    test(list2d,nodes)
    for i in range(0,len(otp)):
        #copy the visited nodes
        vis_new = vis.copy()
        vis_new.append(otp[i])
        #check if the other nodes are destination
        #if yes we check for the total paths
        if otp[i]==en_node:
            no_of_paths = len(allpaths)
            #check if the total number of paths is greater than 5
            if no_of_paths>5:
                return
            else:
                allpaths.append(vis_new)
        #if not, then we go for dfs paths using recursion
        else:
            dfspath(otp[i],en_node,vis_new,nodes,list2d, allpaths)

#main function
def main():
    #read locations file
    nodes, coordinates,list2d = readLocations("locations.txt")

    print("all the nodes are")
    print(nodes)

    #enter staring node
    print("enter starting node")
    st_node = input()
    #enter ending node
    print("enter ending node")
    en_node = input()
    #initialize visited and allpaths lists
    vis = []
    allpaths = []
    #append the starting node to visited
    vis.append(nodes.index(st_node))
    #now call the dfspath function to find all paths using dfs
    dfspath(nodes.index(st_node),nodes.index(en_node),vis,nodes,list2d,allpaths)
    #now print all the paths
    printpaths(nodes,coordinates,allpaths,st_node,en_node)

if __name__ == '__main__':
    main()