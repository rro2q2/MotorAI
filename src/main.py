import search as sr
import nms
import time

goal_coord = [(1, 1)]
bldg_coord = [(1, 2), (1, 4), (2, 1), (2, 2), (2, 4), (3, 1), (4, 3)]
"""
    [(0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18),
               (0, 22), (0, 23), (0, 24), (1, 0), (1, 1), (1, 2), (1,4), (1,5), (1,6), (1,7), (1,8), (1,14), (1,15),
               (1,16), (1,17), (1,18), (1,19), (1,20), (1,21), (1,23), (2, 18), (2,19), (2,20), (2,23), (2,24),
               (3,4), (3,14), (3,15), (3,16), (3,22), (4,0), (4,1), (4,2), (4,5), (4,11), (4,12), (4,21), (4,22),
               (4,23), (4,24), (5,1), (5,5), (5,13), (5,14), (5,15), (5,16), (5,20), (5,21), (5,22), (5,23), (5,24),
               (6,4), (6,11), (6,13), (6,14), (6,15), (6,21), (6,23), (6,24), (7, 4), (7, 8), (7,9), (7,10), (7,14),
               (7,15), (7,16), (7,18), (7,19), (7,20), (7,21), (7,22), (7,23), (7,24), (8, 1), (8,2), (8,10), (8,11),
               (8, 12), (8, 15), (9, 5), (9, 8), (9, 12), (9, 14), (9, 19), (10, 1), (10, 2), (10, 5), (10, 11),
               (10, 12), (10, 13), (10, 19), (11, 2), (11, 6), (11, 21), (11, 22), (12, 3), (12, 5), (12, 7), (12, 9),
               (12, 10), (12, 11), (12, 13), (12, 16), (13, 6), (13, 7), (13, 9), (13, 13), (13, 17), (13, 18),
               (13, 19), (13, 21), (13, 22), (13, 23), (14, 0), (14, 1), (14, 2), (14, 3), (14, 6), (14, 7), (14, 8),
               (14, 9), (14, 19), (15, 13), (15, 14), (15, 15), (15, 16), (15, 17), (15, 19), (16, 0), (16, 19), (16, 22),
               (17, 8), (17, 10), (17, 11), (17, 12), (17, 14), (17, 15), (18, 20), (18, 21), (18, 24), (19, 0),
               (19, 1), (19, 19), (19, 21), (19, 24), (20, 1), (20, 2), (20, 4), (20, 6), (20, 18), (20, 24),
               (21, 9), (21, 10), (21, 13), (21, 15), (21, 21), (21, 23), (22, 10), (22, 13), (22, 21), (22, 23),
               (23, 0), (23, 1), (23, 3), (23, 4), (23, 6), (23, 7), (23, 8), (23, 10), (23, 11), (23, 13), (23, 16),
               (23, 17), (23, 19), (24, 0), (24, 1), (24, 2), (24, 4), (24, 13), (24, 17), (24, 19)]
"""
#[(1, 2), (1, 4), (2, 1), (2, 2), (2, 4), (3, 1), (4, 3)] - for 5 by 5
stop_coord = [(0, 2), (1, 3), (2, 0), (3, 3), (4, 1)]
"""
    [(0, 13), (2, 2), (2, 11), (2, 14), (2, 21), (3, 0), (3, 10), (4, 18), (5, 6), (6, 0), (6, 5), (6, 16),
              (8, 19), (9, 4), (9, 23), (10, 16), (11, 0), (11, 9), (11, 18), (12, 21), (12, 24), (13, 4), (14, 11),
              (14, 14), (15, 9), (15, 21), (16, 4), (17, 3), (17, 16), (17, 21), (18, 9), (19, 13), (20, 8), (21, 1),
              (21, 6), (21, 24), (22, 4), (22, 16), (22, 19), (23, 22), (24, 9), (24, 23)]
"""
#[(0, 2), (1, 3), (2, 0), (3, 3), (4, 1)] - for 5 by 5


# Initializes each element on the grid as an empty node
# Returns a 2d list of empty nodes
def initGrid(node, dim: tuple):
    k = [[' ' for i in range(dim[0])] for j in range(dim[1])]
    for i in range(dim[0]):
        for j in range(dim[1]):
            if (i, j) == node.pos:
                k[i][j] = node.value
            elif (i, j) in bldg_coord:
                k[i][j] = 'X'
            elif (i, j) in goal_coord:
                k[i][j] = 'G'
            elif (i, j) in stop_coord:
                k[i][j] = 'S'
    return k

def showGridStates(path, dim: tuple):
    for index in range(len(path)):
        k = initGrid(path[0], dim)
        for i in range(dim[0]):
            for j in range(dim[1]):
                if (i, j) not in bldg_coord and (i, j) not in goal_coord and (i, j) not in stop_coord:
                    k[i][j] = ' '
                if (i, j) == path[index].pos:
                    temp = k[i][j]
                    k[i][j] = 'C' # path[index].value
                    print('\n')
        displayGrid(k)

# Store the contents in a 2d temp list and display it
def displayGrid(k):
    for i in range(len(k)):
        print(k[i])

def main():
    start_pos = (4, 2)
    grid_size = (5, 5)
    node = sr.Node(start_pos, 0, 0, 0, 'C', None, None)
    grid = initGrid(node, grid_size)

    startTime = time.time()
    res = sr.aStarSearch(node, grid)
    # Path to Goal function
    path = sr.pathToGoal(res)
    endTime = time.time()
    print("TIME:", endTime - startTime)
    print("PATH")
    for states in path:
        print(states.pos)
        if states.value == 'S':
            #time.sleep(3)
            print("STOP")

    print("Result", res.pos)
    print("------Initial Grid------")
    displayGrid(grid)
    print("Path to Goal")
    showGridStates(path, grid_size)

    # Non Maximum Suppression
    #rects = nms.locateBoundingBoxes(nms.gray)
    #nms_rects = nms.nms(rects, 0.2)
    #nms.displayImage(rects, nms_rects)

    #detections = [[31, 31, .9, 10, 10], [31, 31, .12, 10, 10], [100, 34, .8, 10, 10]]
    #print("Detections before NMS = {}".format(detections))
    #print("Detections after NMS = {}".format(nms.nms(detections)))
    return

if __name__ == '__main__':
    main()
