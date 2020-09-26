
from math import *
import copy


def print_move(n, x_a, y_a, x_b, y_b, **kwargs):
    """
    Output a move action of n pieces from square (x_a, y_a)
    to square (x_b, y_b), according to the format instructions.
    """
    print("MOVE {} from {} to {}.".format(n, (x_a, y_a), (x_b, y_b)), **kwargs)


def print_boom(x, y, **kwargs):
    """
    Output a boom action initiated at square (x, y) according to
    the format instructions.
    """
    print("BOOM at {}.".format((x, y)), **kwargs)

#Checkng for visited nodes
def repeats(visited , loc):
    for i in range(0,len(visited)):
        if visited[i][1] == loc[1] and visited[i][2] == loc[2]:
            return 1
    return 0
#For a given point on the board returns the number of whites boomed
def goal_h(data , point , count , v):

    cop = point.copy()
    for i in range(-1 , 2):
        for j in range(-1 , 2):
            restart(point , cop)
            if (i != 0) or (j != 0):
                point[1] += i
                point[2] += j
                #print(point)

                if check_b(data , point ,v) == 1:
                    count += 1
                    count = goal_h(data , point , count ,v)
    return count

#Check for black collisions
def check_b(data , point , v):

    for i in range(0 , len(data['black'])):
        if point[1] == data['black'][i][1] and point[2] == data['black'][i][2] :
            if (v[i] == 0):
                v[i] = 1
                return 1

    return 0

def restart(point , cop):
    point[1] = cop[1]
    point[2] = cop[2]

#Function that uses Breadth first search to find if there is direct path(not needing stacks)
#from point to goal
def bfs(data , point ,goal ):
    q = [point]
    visited = [point]
    count = 0
    v = [0] * len(data['black'])
    if point[1] == goal[1] and point[2] == goal[2]:
        return 1
    while q:
        point = q.pop(0)
        cop = point.copy()

        for i in range(1,3):
            for j in range(-1 , 2):
                point = cop.copy()
                if j:
                    if point[i] + j <= 7 and  point[i] + j >= 0:
                        point[i] += j
                        if point not in visited and inblack(point , data):
                            q.append(point)
                            visited.append(point)
                            if point[1] == goal[1] and point[2] == goal[2]:
                                return 1
                            #visited[len(visited) - 1].append(goal_h(data , point , count , v))



    return 0

#check to see if point is on a black point
def inblack(point , data):
    for i in range(0,len(data['black'])):
        if point[1] == data['black'][i][1] and point[2] == data['black'][i][2]:
            return 0
    return 1
#add number of blacks boomed to a list corresponding to points on the board
def add_h(visited , data , h):
    count = 0
    v = [0] * len(data['black'])

    for i in range(0 , len(visited)):
        point = visited[i]
        v = [0] * len(data['black'])
        h[i] = goal_h(data , visited[i] , count , v)
        count = 0

#Finding the point with maximum blacks boomed
def max_find(h):
    max = 0
    for i in range(1 , len(h)):
        if h[max] < h[i]:
            max = i
    return max

#Removing the boomed black peices from a copy of the board
def delete_piece(data , point):
    cop = point.copy()

    for i in range(-1 , 2):
        for j in range(-1 , 2):
            restart(point , cop)

            if (i != 0) or (j != 0):
                point[1] += i
                point[2] += j
                #print(point)

                if boom_point(point , data) == 0:
                    delete_piece(data , point)

#Deleting the boomed blacks from a copy of the board state
def boom_point(point , data):
    for i in range(0,len(data['black'])):
        if point[1] == data['black'][i][1] and point[2] == data['black'][i][2]:
            del data['black'][i]
            return 0

    return 1

#Using the A star search algorithm to find the shortest path to the goals
#Returns 0 if there is no path(i.e need stacks)
def Astar(start , goal , data):
    openlist = [start]
    closedlist = []
    while len(openlist):
        current = openlist[min_index(openlist)]
        if current[1] == goal[1] and current[2] == goal[2]:
            return current
        closedlist.append(current)
        openlist.remove(current)
        for i in range(1,3):
            for j in range(-1*current[0],current[0]+1):
                neighbour = current.copy()

                if j:
                    if current[i] + j >= 0 and current[i] + j < 8:
                        neighbour[i] = current[i] + j
                        v = [0] * len(data['black'])
                        count = 0
                        if check_black(neighbour , data , 1 , 2):
                            tmp_score = current[3] + 1
                            neighbour[5] = current
                            neighbour[3] = tmp_score
                            neighbour[4] = heuristic(neighbour , goal) + tmp_score
                            if check_vists(closedlist , neighbour):
                                new = neighbour.copy()
                                openlist.append(new)


    return 0

#Checking to see if white is on a black returning 0 if it is
def check_black(location, data , index_1 , index_2):

    for black_piece in data["black"]:
        if (black_piece[1] == location[index_1]) and (black_piece[2] == location[index_2]):
            return 0
    return 1

#Check to see if the new node has already been expanded in A star
def check_vists(closed , neighbour):
    for i in range(0,len(closed)):
        if neighbour[1] == closed[i][1] and neighbour[2] == closed[i][2]:
            return 0
    return 1

#The heuristic function used for the A star algorithm
#Returns Manhattan Distance
def heuristic(location , goal):
    return abs(location[1] - goal[1]) + abs(location[2] - goal[2])


#Finding the minimum F(n) value in the Open list
def min_index(openlist):
    min = 0
    if len(openlist) > 1:
        for i in range(1,len(openlist)):
            if openlist[i][4] < openlist[min][4]:
                min = i
    return min
#Finding the path based on A star
def iter_print(move):
    path = []
    while move[5] != None:
        path.append(move[0:3])
        move = move[5]
    path.append(move[0:3])

    return path

#Printing the path
def move_output(move):
    for i in range(0,len(move)):
        if i+1 < len(move):
            print_move(move[i+1][0],move[i][1],move[i][2],move[i+1][1],move[i+1][2])

#Check every point on the board to find the number of blacks boomed at every point
def check_board(data):
    visited = []
    point = [1,0,0]
    visited.append(point.copy())
    for x in range(0,8):
        for y in range(0,8):
            point[1] = x
            point[2] = y
            cop = point.copy()
            if check_black(point , data , 1 , 2):

                visited.append(cop)
    expanded = copy.deepcopy(visited)
    h = [0]*len(visited)
    add_h(visited , data , h)
    return h,expanded

#Printing the whites boomed
def boom_loop(boom_p):
    for i in range(0,len(boom_p)):
        print_boom(boom_p[i][1] , boom_p[i][2])
#Finding the best white piece to boom a certain cluster
#Returns : min_goal - goal  , closest_white - White piece closest to goal
def goal_best(expanded , scores , data , max):
    minim = 1000
    min_goal = -2
    closest_white = -2
    for i in range(0,len(expanded)):
        if scores[i] == max:
            for j in range(0,len(data['white'])):
                if len(data['white'][j]) < 4:
                    temp = heuristic(data['white'][j] , expanded[i])
                    if minim > temp:
                        minim = temp
                        min_goal = i
                        closest_white = j
    return min_goal , closest_white
#Function to assign goals to every white
def goal_find(data):
    data_copy = copy.deepcopy(data)
    total = []
    goal = []
    visited = []
    while sum(total) != len(data['black']):
        if len(goal) == len(data['white']):
            goal = []
            data_copy = copy.deepcopy(data)
        scores,expanded = check_board(data_copy)
        min_goal , closest_white =  goal_best(expanded , scores , data , max(scores))
        total.append(scores[min_goal])
        goal_index = max_find(scores)
        if expanded[goal_index] not in visited:
            goal.append(expanded[goal_index].copy())
            visited.append(goal[-1].copy())
            data['white'][closest_white].append(goal[-1].copy())
            delete_piece(data_copy,goal[-1].copy())

    return goal
#Returns a list of zeros or ones corresponding to each white piece
def need_stacks(data):
    stack_need = []
    if data['white'][0][0] < 3:
        for i in range(0,len(data['white'])):
            if len(data['white'][i]) > 3:
                if bfs(data ,data['white'][i] , data['white'][i][3]):
                    stack_need.append(0)
                else:
                    stack_need.append(1)
            else:
                stack_need.append(0)
    return stack_need

#Makes stacks such that the white peices do not need stacks
def make_stack(data,ns):
    start = []
    while 1 in ns:
        for i in range(0,len(data['white'])):

            if i >= len(data['white']):
                break
            #If a white piece needs a stack to move use A star to move to the other white
            if ns[i]:
                for j in range(0,len(data['white'])):
                    if j != i:
                        if bfs(data, data['white'][i],data['white'][j]):
                            start = data['white'][i][0:3].copy()
                            end = data['white'][j].copy()
                            start.append(0)
                            start.append(0)
                            start.append(None)
                            move = Astar(start, end,data)
                            path = iter_print(move)
                            path.reverse()
                            move_output(path)
                            data['white'][i][1] = data['white'][j][1]
                            data['white'][i][2] = data['white'][j][2]
                            data['white'][i][0] += 1
                            ns[i] = 0
                            break
#Check to see if all whites are at the goals
def all_goals(data):
    valid = 1
    for i in range(0,len(data['white'])):
        if len(data['white'][i]) == 4:
            if data['white'][i][1] != data['white'][i][3][1] or data['white'][i][2] != data['white'][i][3][2]:
                valid = 0
    return valid
#Fix the stack values for the white pieces
def fix_data(data):
    for i in range(0,len(data['white'])):
        count = 1
        for j in range(0,len(data['white'])):
            if i != j:
                if data['white'][i][1] == data['white'][j][1] and data['white'][i][2] == data['white'][j][2]:
                    count += 1

        data['white'][i][0] = count
#Function to use A star to return the move
def move(data,i):
    start = []
    if len(data['white'][i]) > 3:
        start = data['white'][i][0:3].copy()
        end = data['white'][i][3].copy()
        start.append(0)
        start.append(0)
        start.append(None)
        move = Astar(start, end,data)

    return move
#Get the first move from the A star search algorithm
def getFirstMove(path):
    first = [0,0,0]
    if path[5] != None:
        while path[5] != None:
            first[1] = path[1]
            first[2] = path[2]
            path = path[5]
    else:
        first[1] = path[1]
        first[2] = path[2]
    return first

#Returns 1 if a certain white is at the goal
def at_goal(data , i):
    if data['white'][i][1] == data['white'][i][3][1] and data['white'][i][2] == data['white'][i][3][2]:
        return 1
    return 0

#If A star fails the algoritm makes stacks and then does the best move at that point
def best_first(data , i,visited):
    start = data['white'][i][0:3].copy()
    goal = data['white'][i][3].copy()
    moves = []
    h = []
    cop = start.copy()
    for k in range(1,3):

        for j in range(-1*start[0] , start[0] + 1):
            start = cop.copy()
            if j:
                start[k] += j
                if start[k] >= 0 and start[k] < 8:
                    moves.append(start.copy())
                    h.append(heuristic(start,goal))
                    if len(visited):
                        #print(visited , start)
                        if repeats(visited ,start):
                            h[-1] = 1000
                    if check_black(start , data ,1 ,2) == 0:

                        h[-1] = 1000

    index = best(h)
    return moves[index]

def best(h):
    min = 0
    for i in range(1,len(h)):
        if h[min] > h[i]:
            min = i
    return min

#Function that finds and prints the moves using A star and if failing greedy best first search_trial
#Furthermore, algorithm also uses BFS to check for direct path or not
def find_moves(data):
    visited = []
    while all_goals(data) == 0:

        for i in range(0,len(data['white'])):
            if len(data['white'][i]) == 4:
                while heuristic(data['white'][i],data['white'][i][3]):
                    path = move(data , i)
                    if path:
                        first = getFirstMove(path)
                        count = 1
                        a = data['white'][i][1]
                        b = data['white'][i][2]
                        data['white'][i][1] = first[1]
                        data['white'][i][2] = first[2]
                        size = data['white'][i][0]

                        if size > 1:

                            for j in range(0,len(data['white'])):
                                if j != i:
                                    if data['white'][j][0] == size:
                                        if len(data['white'][j]) < 4:
                                            data['white'][j][1] = first[1]
                                            data['white'][j][2] = first[2]
                                            count += 1
                                        elif bfs(data , first , data['white'][j][3]):
                                            if at_goal(data , j) == 0:
                                                data['white'][j][1] = first[1]
                                                data['white'][j][2] = first[2]
                                                count += 1
                                            else:
                                                fix_data(data)

                                        else:
                                            data['white'][j][0] += -1
                                            data['white'][i][0] += -1
                        fix_data(data)
                        print_move(count  , a, b , first[1] , first[2])
                        #print(data)
                    else:
                        #print(visited)
                        ns = need_stacks(data)
                        make_stack(data,ns)
                        fix_data(data)
                        first = best_first(data , i ,visited)
                        count = 1
                        visited.append(first.copy())
                        a = data['white'][i][1]
                        b = data['white'][i][2]
                        data['white'][i][1] = first[1]
                        data['white'][i][2] = first[2]
                        size = data['white'][i][0]
                        if size > 1:
                            for j in range(0,len(data['white'])):
                                if j != i:

                                    if data['white'][j][0] == size:
                                        #if next move is reachable
                                        if len(data['white'][j]) < 4:
                                            data['white'][j][1] = first[1]
                                            data['white'][j][2] = first[2]
                                            count += 1
                                        elif bfs(data , first , data['white'][j][3]):
                                            #at goal?
                                            data['white'][j][1] = first[1]
                                            data['white'][j][2] = first[2]
                                            count += 1
                                            fix_data(data)

                                        else:
                                            data['white'][j][0] += -1
                                            data['white'][i][0] += -1

                        print_move(count  , a, b , first[1] , first[2])
#Checking a changing the data from Json file to whats needed for the program
def initialStacks(data):
    for i in range(0,len(data['white'])):
        if data['white'][i][0] > 1:
            for count in range(data['white'][i][0]-1) :
                data['white'].append(data['white'][i].copy())
