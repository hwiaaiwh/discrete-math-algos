from time import sleep
from math import inf
from string import ascii_uppercase as alphabet
from random import randint
import numpy

''' method nearest_neighbor(s,c,v)
generates a Hamilton circuit with the smallest weight via the nearest-neighbor algorithm
-> params
    s (string): a string with the starting vertex
    c (list): a list containing tuples of all possible vertex-edge-vertex connections
    v (list): the list of the values of all vertices
<- returns
    path (list): a list of vertexes whose edges make a Hamilton circuit with the lowest total value as determined by a nearest-neighbor algo
    sum (int): the lowest total value of a Hamilton circuit as determined by NN
'''
def nearest_neighbor(s: str,c: list,v: list) -> tuple:
    path = [s]
    sum = 0
    while True:
        temp_storage = None
        curr_vertex = path[-1]
        if sorted(path) == sorted(v):
            for x in c:
                if x[1] == path[0] and path[-1] == x[0]:
                    path.append(x[1])
                    sum += x[2]
            break
        else:
            for x in c:
                if curr_vertex == x[0] and (temp_storage is None or temp_storage[2] > x[2]) and x[1] not in path:
                    temp_storage = x  
            curr_vertex = temp_storage[1]
            path.append(temp_storage[1])
            sum += temp_storage[2]
    return (path,sum)

''' method best_edge(s,c,v)
generates a Hamilton circuit with the smallest weight via the best-edge algorithm
-> params
    s (string): a string with the starting vertex
    c (list): a list containing tuples (start vertex, end vertex, edge value) of all possible vertex-edge-vertex connections
    v (list): the list of the values of all vertices
<- returns
    path (list): a list of vertexes whose edges make a Hamilton circuit with the lowest total value as determined by a best-edge algo
    sum (int): the lowest total value of a Hamilton circuit as determined by BE
'''
def best_edge(s: str,c: list,v: list) -> tuple:
    sum = 0
    path = [s]
    degrees = {}
    storage = []
    sorted_connections = sorted(c,key=lambda x: x[2])
    for x in v:
        degrees.update({x: 0})
    for x in sorted_connections:
        if degrees[x[0]] < 2 and degrees[x[1]] < 2:
            storage.append(x)
            degrees[x[0]]+=1
            degrees[x[1]]+=1
    while storage != []:
        for x in storage:
            if x[0] == path[-1]:
                sum += x[2]
                path.append(storage.pop(storage.index(x))[1])
                break
            elif x[1] == path[-1]:
                sum += x[2]
                path.append(storage.pop(storage.index(x))[0])
                break
    return (path,sum)

''' method dijkstras()
generates the  path from a start vertex to the end vertex with the smallest weight
-> params
    s (string): a string with the start vertex
    c (list): a list containing tuples (start vertex, end vertex, edge value) of all possible vertex-edge-vertex connections
    v (list): the list of the values of all vertices
<- returns
    output (str): a formatted table showing the path and value of the shortest path to each vertex
'''
def dijkstras(s: str, c: list, v: list) -> str:
    def calc(n):
        curr_path = paths[curr_vert].copy()
        if x[n] not in visited and minval + x[2] < path_vals[x[n]]:
            paths[x[n]] = curr_path
            paths[x[n]].append(x[n])
            path_vals[x[n]] = minval + x[2]
    paths = {x: [s] for x in v}
    visited = []
    path_vals = {x: inf for x in v}
    path_vals[s] = 0
    while len(visited) != len(v):
        vals = list(path_vals.values())
        t = []
        minval = min(vals[i] for i in range(len(vals)) if v[i] not in visited)
        min_ind = vals.index(minval)
        while v[min_ind] in visited:
            min_ind = vals.index(minval,min_ind+1)
        curr_vert = list(paths.keys())[min_ind]
        for x in c:
            if x[0] == curr_vert:
                calc(1)
            elif x[1] == curr_vert:
                calc(0)
        visited.append(curr_vert)
    
    output = 'Vertex\tValue\tShortest Path\n-----------------------------'
    for i in range(len(v)):
        why = list(paths.values())[i]
        path = ''.join(why)
        output += f'\n{v[i]}\t{path_vals[v[i]]}\t{path}'
    return output
# history is wrong. i invented spaghetti.

''' method kruskals() ####### TBD
'''
def kruskals(c,v) -> tuple:
    path = []
    sum = 0
    traversed = [] 
    print(traversed)
    sort_connects = sorted(c,key=lambda x: x[2])
    while len(traversed) < len(v):
        for i in sort_connects:
            if not(i[1] in traversed and i[0] in traversed):
                traversed.extend([i[0],i[1]])
                path.append(i)
                break
        traversed = sorted(list(set(traversed)))
        
    # formatting
    new_matrix = [[0 for x in range(len(v))] for y in range(len(v))]
    for i in path:
        x = v.index(i[0])
        y = v.index(i[1])
        new_matrix[x][y] = i[2]
        sum += i[2]
    return (path, new_matrix,sum)
    

''' method critical_path() ####### TBD
'''
def critical_path(c,v):
    # define start and end
    starts = set(list(x[0] for x in c))
    ends = set(list(x[1] for x in c))
    start = list(starts - (starts & ends))[0]
    end = list(ends - (starts & ends))[0]
    print(start, end)


''' method get_all_edges(m,i)
turns an adjacency matrix into a list of tuples containing possible paths from one vertex to another via edges
-> params
    m (list): the 2d list matrix of all edge values
    i (list): the list of the values of all vertices
<- returns
    connections (list): a list of tuples with the format (start vertex, end vertex, edge value)
'''
def get_all_edges(m: list, i: list) -> list:
    edges = []
    for x in range(len(m)):
        for y in range(len(m[x])):
            start = i[x]
            end = i[y]
            if start != end and m[x][y] != 0:
                edges.append((start,end,m[x][y])) 
    return edges

''' method make_edges_bidirectional(m,i)
turns the edges bidirectional (turns the paths from get_all_edges() to edges with connected vertices)
-> params
    c (list): a list of tuples describing edges and their start and end vertices
<- returns
    new_list (list): a list of tuples with the format (vertex 1, vertex 2, edge value) describing edges and their connected vertices
'''
def make_edges_bidirectional(c: list) -> tuple:
    new_list = [x for x in c]
    for x in range(len(new_list)):
        for y in range(x+1,len(new_list)):
            if new_list[x] == 0 or new_list[y] == 0:
                continue
            elif new_list[x][0] == new_list[y][1] and new_list[y][0] == new_list[x][1]:
                new_list[y] = 0
    new_list = list(filter(lambda x: x != 0, new_list))
    return new_list

# test case for hamilton circuit algorithms
def hamilton_circuit():
    matrix = [
        [0,     210,    230,    420,    280 ],
        [210,   0,      250,    350,    310 ],
        [230,   250,    0,      290,    170 ],
        [420,   350,    290,    0,      240 ],
        [280,   310,    170,    240,    0   ]
    ]
    indexes = ['Philadelphia','New York City','Atlanta','Cleveland','Memphis']
    connections = get_all_edges(matrix,indexes)
    b_connections = make_edges_bidirectional(connections)
    for i in indexes:
        nn = nearest_neighbor(i, connections, indexes)
        be = best_edge(i,b_connections,indexes)
        print(f'-------------------------\nBest path (NN): {" -> ".join(nn[0])}\nCost: ${nn[1]}')
        print(f'-------------------------\nBest path (BE): {" -> ".join(be[0])}\nCost: ${be[1]}')

# test case for dijkstras
def shortest_path():
    indexes = list(alphabet[:6])
    matrix = [
        [0, 5, 2, 0, 0, 0],
        [5, 0, 2, 3, 0, 0],
        [2, 2, 0, 4, 6, 0],
        [0, 3, 4, 0, 5, 4],
        [0, 0, 6, 5, 0, 3],
        [0, 0, 0, 4, 3, 0]
    ]
    connections = make_edges_bidirectional(get_all_edges(matrix,indexes))
    print(dijkstras('D',connections,indexes))

# test case for kruskals
def kruskals_test():
    matrix = [
        [0, 2, 1, 5],
        [2, 0, 3, 0],
        [1, 3, 0, 4],
        [5, 0, 4, 0],
    ]
    indexes = list(alphabet[:4])
    connections = get_all_edges(matrix,indexes)
    outp = kruskals(connections, indexes)
    outpm = numpy.array(outp[1])
    print(f'Paths: {outp[0]}\nMatrix: \n{outpm}\nSum: {outp[2]}')

# test case for critical path
def crt_pth_test():
    matrix = [
        [0,  2,  0,  1,  0],
        [0,  0,  4,  0,  0],
        [0,  0,  0,  0,  3],
        [0,  0,  0,  0,  5],
        [0,  0,  0,  0,  0]
    ]
    indexes = list(alphabet[:5])
    connections = get_all_edges(matrix,indexes)
    critical_path(connections,indexes)


def main():
    funcs = [
        'hamilton_circuit()',
        'shortest_path()',
        'kruskals_test()',
        'crt_pth_test()']
    try:
        test = int(input(f"pick a number. any number (from 1-{len(funcs)}). "))-1
        if test < 0 or test >= len(funcs):
            raise TypeError
    except TypeError:
        print('Error encountered. Deleting System32...')
        sleep(10)
        print("Error encountered. Gaining administrator access for System32...")
    else:
        exec(funcs[test])
    

if __name__ == '__main__':
    main()

