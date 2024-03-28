# from variables import *
# import copy

# # Game state
# from gameState import *

# '''
#     Breadth First Search
#         @start: [tupple] -> start location
#         @target: [tupple] -> target location
#         @gameState: [GameState]

# '''

from variables import *
import copy

def bfs(grid, start, target, max_dist=float("inf")):
    visited = []
    queue = [(start, [])]

    while len(queue) > 0:
        nxt = queue.pop(0)
        visited.append(nxt[0])
        new_path = copy.deepcopy(nxt[1])
        new_path.append(nxt[0])
        loc = nxt[0]
        if type(target) is tuple:
            if target == loc:
                return new_path
        elif grid[loc[0]][loc[1]] in target:
            return new_path

        if grid[loc[0] + 1][loc[1]] in [o, e, O] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] + 1, loc[1]),new_path))
        if grid[loc[0] - 1][loc[1]] in [o, e, O] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0] - 1, loc[1]),new_path))
        if grid[loc[0]][loc[1] + 1] in [o, e, O] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] + 1),new_path))
        if grid[loc[0]][loc[1] - 1] in [o, e, O] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
            queue.append(((loc[0], loc[1] - 1),new_path))

    return None


# def bfs(start, target, pelletsArray, max_dist=float("inf")):
#     # print('var')
#     # print(start)
#     # print(type(target) is str)
#     visited = []
#     queue = [(start, [])]
#     # print('nvfdvd')
#     # print(pelletsArray)

#     def specialLocation(row, col):
#         boolean = bool((pelletsArray[row] >> col) & 1)
#         # print('bool')
#         # print(boolean)
#         return boolean
    
#     def identifyTarget(identifier, row, col):
#         # print('identifying target')
#         if identifier == 'p':
#             isThereApellet = specialLocation(row, col)
#             # print('target has been identified: ', isThereApellet)
#             return isThereApellet
#         elif identifier == 's':
#             return bool((pelletsArray[row] >> col) & 1) and \
# 			    ((row == 3) or (row == 23)) and ((col == 1) or (col == 26))
#         # elif identifier == 'f':
#         #     return gs.fruitAt(row, col)
#         return False

#     while len(queue) > 0:
#         nxt = queue.pop(0)
#         visited.append(nxt[0])
#         new_path = copy.deepcopy(nxt[1])
#         new_path.append(nxt[0])
#         loc = nxt[0]
#         # print('loc')
#         # print(loc[0])
#         if type(target) is tuple:
#             if target == loc:
#                 # print('RETURN')
#                 return new_path
#         elif type(target) is str:
#             if identifyTarget(target, loc[0], loc[1]):
#                 # print('RETURN')
#                 return new_path

#         # if grid[loc[0] + 1][loc[1]] in [o, e, O] and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
#         #     queue.append(((loc[0] + 1, loc[1]),new_path))
#         # if grid[loc[0] - 1][loc[1]] in [o, e, O] and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
#         #     queue.append(((loc[0] - 1, loc[1]),new_path))
#         # if grid[loc[0]][loc[1] + 1] in [o, e, O] and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
#         #     queue.append(((loc[0], loc[1] + 1),new_path))
#         # if grid[loc[0]][loc[1] - 1] in [o, e, O] and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
#         #     queue.append(((loc[0], loc[1] - 1),new_path))
#         # print('continue')
#         # print(specialLocation(loc[0], loc[1] - 2))
#         # print((loc[0], loc[1] - 1) not in visited)
#         if specialLocation(loc[0] + 1, loc[1]) and (loc[0] + 1, loc[1]) not in visited and len(new_path) <= max_dist:
#             queue.append(((loc[0] + 1, loc[1]),new_path))
#             # print('first if')
#         if specialLocation(loc[0] - 1, loc[1]) and (loc[0] - 1, loc[1]) not in visited and len(new_path) <= max_dist:
#             queue.append(((loc[0] - 1, loc[1]),new_path))
#             # print('second if')
#         if specialLocation(loc[0], loc[1] + 1) and (loc[0], loc[1] + 1) not in visited and len(new_path) <= max_dist:
#             queue.append(((loc[0], loc[1] + 1),new_path))
#             # print('third if')
#         if specialLocation(loc[0], loc[1] - 1) and (loc[0], loc[1] - 1) not in visited and len(new_path) <= max_dist:
#             queue.append(((loc[0], loc[1] - 1),new_path))
#             # print('fourth if')

#     return None

