from math import sqrt
from heapq import heappush, heappop

def find_path(src, dest, mesh):
    #
    adj = mesh['adj']

    #use the given clicked coordinates to and find what boxes they are in
    startBox=None
    endBox=None
    for box in mesh["boxes"]:
        if withinBox(box,src):
            print ("We found the source!!!!")
            startBox=box
        if withinBox(box,dest):
            print ("We found the dest!!!!")
            endBox=box
    #if both start and end aren't in boxes, there's no point in continuing
    if (startBox is None) or (endBox is None):
        print ('No path!')
        return [],[]
    #begin initializing A* stuff
    frontBoxPoint = {startBox: src}
    backBoxPoint = {endBox: dest}
    queue = []
    queue.append((0, startBox, 'end' ))
    queue.append((0, endBox, 'start'))
    visited = []
    frontParent = {startBox: None}
    backParent = {endBox: None}
    frontDist = { startBox:0 } 
    backDist = { endBox:0 }
    #begin processing boxes
    while queue:
        prior, node, goal = heappop(queue)
        visited.append(node)
        #the search 'clouds' have overlapped each other
        if (node in backParent) and (node in frontParent):
            currFront = currBack = node
            pathFront = []
            pathBack = [(frontBoxPoint[node],backBoxPoint[node])]
            while frontParent[currFront] is not None:
                pathFront.append((frontBoxPoint[frontParent[currFront]],frontBoxPoint[currFront]))
                currFront = frontParent[currFront]
            pathFront.reverse()
            while backParent[currBack] is not None:
                pathBack.append((backBoxPoint[backParent[currBack]],backBoxPoint[currBack]))
                currBack = backParent[currBack]
                fullPath = pathFront + pathBack
            return fullPath, visited

        for neighbor in adj[node]:
            if goal == 'end':
                boxPoint = frontBoxPoint
                dist = frontDist
                parent = frontParent
                goal_point = dest
            else:
                boxPoint = backBoxPoint
                dist = backDist
                parent= backParent
                goal_point = src
            #help route the lines through the boxes
            x,y = boxPoint[node]
            if boxPoint[node][0]<= neighbor[0]: x = neighbor[0]
            if boxPoint[node][0]>= neighbor[1]: x = neighbor[1]
            if boxPoint[node][1]<= neighbor[2]: y = neighbor[2]
            if boxPoint[node][1]>= neighbor[3]: y = neighbor[3]
            newPoint = (x,y)
            newDist = dist[node] + distance(boxPoint[node], newPoint)
            if (neighbor not in dist) or (newDist < dist[neighbor]):
                heuristic = distance(newPoint,goal_point)
                boxPoint[neighbor] = newPoint
                dist[neighbor] = newDist
                #addition of heuristic changes dijkstra's to A*
                heappush(queue, (newDist + heuristic, neighbor,goal))
                parent[neighbor] = node
    #haven't found a scenario where this next part ever reached, but we've
    #still kept it from when we were using BFS just in case
    print('No path!')
    return [],[]

def withinBox(box, point):
    #Boxes are defined by their bounds: (x1,x2,y1,y2)
    if point[0]>=box[0] and point[0]<box[1] and point[1]>=box[2] and point[1]<box[3]:
        return True
    else:
        return False

def distance(p1, p2):
    return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
