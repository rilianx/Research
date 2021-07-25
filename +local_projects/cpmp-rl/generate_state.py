## EXAMPLE
#stackValues: [1, 2, 1, 1, 2]
#stacksLen: [5, 5, 5, 5, 5]
#topStacks: [8, 5, 6, 11, 23]
#yard:
# [[2, 22, 14, 20, 8], [9, 1, 19, 21, 5], [7, 24, 3, 17, 6], [15, 18, 16, 12, 11], [25, 4, 13, 10, 23]]
#elevateState:
# [[25, 25, 2, 22, 14, 20, 8], [25, 25, 9, 1, 19, 21, 5], [25, 25, 7, 24, 3, 17, 6], [25, 25, 15, 18, 16, 12, 11], [25, 25, 25, 4, 13, 10, 23]]
#compactState:
# [[25, 25, 2, 22, 14, 20, 8], [25, 25, 9, 1, 19, 21, 5], [25, 25, 7, 24, 3, 17, 6], [25, 25, 15, 18, 16, 12, 11], [25, 25, 25, 4, 13, 10, 23]]
#flattenState:
# [25, 25, 2, 22, 14, 20, 8, 25, 25, 9, 1, 19, 21, 5, 25, 25, 7, 24, 3, 17, 6, 25, 25, 15, 18, 16, 12, 11, 25, 25, 25, 4, 13, 10, 23]
#normalize:
# [1.   1.   0.08 0.88 0.56 0.8  0.32 1.   1.   0.36 0.04 0.76 0.84 0.2
# 1.   1.   0.28 0.96 0.12 0.68 0.24 1.   1.   0.6  0.72 0.64 0.48 0.44
# 1.   1.   1.   0.16 0.52 0.4  0.92]
#state:
# [1.         1.         0.08       0.88       0.56       0.8
# 0.32       1.         1.         0.36       0.04       0.76
# 0.84       0.2        1.         1.         0.28       0.96
# 0.12       0.68       0.24       1.         1.         0.6
# 0.72       0.64       0.48       0.44       1.         1.
# 1.         0.16       0.52       0.4        0.92       0.14285714
# 0.28571429 0.14285714 0.14285714 0.28571429 0.71428571 0.71428571
# 0.71428571 0.71428571 0.71428571 0.32       0.2        0.24
# 0.44       0.92      ]


import numpy as np

def compactState(yard):
    sort = []
    for stack in yard:
      for container in stack:
        if not container in sort:
          sort.append(container)
    sort = sorted(sort)
    maxValue = 0
    for i in range(len(yard)):
      for j in range(len(yard[i])):
        yard[i][j] = sort.index(yard[i][j]) + 1
        if yard[i][j] > maxValue:
          maxValue = yard[i][j]
    return yard

def elevateState(yard, h, max_item):
    for stack in yard:
      while len(stack) < h:
        stack.insert(0,max_item)
        #stack.insert(0,1)
    return yard

def flattenState(state):
    flatten = []
    for lista in state:
        for item in lista:
            flatten.append(item)
    return flatten

def normalize(state,max_item):
    return np.array(state)/max_item


def getStackValues(yard): #sorted stacks?
    values = []
    for stack in yard:
        flag = False
        cont = 0
        for i in range(len(stack)):
            if i==0:
                cont += 1
            else:
                if stack[i] <= stack[i-1]:
                    cont += 1
                else: break
        values.append(cont)
    return values

def getStackLen(yard):
    lens = []
    for stack in yard:
        lens.append(len(stack))
    return lens

def getTopStacks(yard,max_item):
    tops = []
    for stack in yard:
        if len(stack) != 0:
            tops.append(stack[len(stack)-1])
        else:
            tops.append(max_item)
    return tops

def generate_ann_state(yard,H):
    max_item = max([max(stack) for stack in yard])
    stackValues=getStackValues(yard) #well-placed
    stacksLen = getStackLen(yard)
    topStacks = getTopStacks(yard,max_item)
    print("stackValues:",stackValues)
    print("stacksLen:",stacksLen)
    print("topStacks:",topStacks)
    
    print("yard:\n",yard)
    yard=elevateState(yard,H, max_item)
    print("elevateState:\n",yard)
    yard=compactState(yard)
    print("compactState:\n",yard)
    yard=flattenState(yard)
    print("flattenState:\n",yard)
    yard=normalize(yard,max_item)
    print("normalize:\n",yard)
    state=yard
    state=np.append(state,normalize(stackValues,H))
    state=np.append(state,normalize(stacksLen,H))
    state=np.append(state,normalize(topStacks,max_item))
    print("state:\n",state)
    return state

yard = [[2, 22, 14, 20, 8], [9, 1, 19, 21, 5], [7, 24, 3, 17, 6], [15, 18, 16, 12, 11], [25, 4, 13, 10, 23]]
generate_ann_state(yard,7)

