#!/usr/bin/Python
# -*- coding: utf-8 -*-

import arff
import numpy as np
import matplotlib.pyplot as plt
import math
import sys,getopt
from heapq import *
from Queue import *
import random

random.seed(a=None)

# # MutualInfo stores the 
# class MutualInfo:
#     def __init__(self,a,b,value):
#         self.nodePair = []
#         self.nodePair.append(a)
#         self.nodePair.append(b)
#         self.value = value

#     # update compare function so as to implement max heap
#     def __lt__(self, other):
#         return self.value - other.value
#     def __ge__(self, other):
#         return other.value - self.value

#     def __cmp__(self, other):
#         return other.value - self.value


def calprior(data,priorset,postset,attributes):
    prior = 1.0
    totalprior = 1
    for i in range(len(priorset)):
        totalprior *= len(attributes[priorset[i][0]][1])
    totalprior *= 2
    totalprior += len(data)

    for instance in data:
        haspost = True
        hasprior = True
        for each in postset:
            if instance[each[0]] != each[1]:
                hasprior = False
                break
        if hasprior:
            for each in priorset:
                if instance[each[0]]!= each[1]:
                    haspost = False
                    break;
        if hasprior and haspost:
            prior +=1
    prob = prior/totalprior
    return prob


def calpost(data,priorset,postset,attributes):
    post = 1.0
    totalpost = 1.0

    for i in range(len(priorset)):
        totalpost *= len(attributes[priorset[i][0]][1])

    for instance in data:
        haspost = True
        hasprior = True
        for each in postset:
            if instance[each[0]]!= each[1]:
                haspost = False
                break
        if haspost:
            totalpost += 1
            for each in priorset:
                if instance[each[0]] != each[1]:
                    hasprior = False
                    break
            if hasprior:
                post += 1
    prob = post/totalpost
    return prob


def calmutualinfo(data,i,j,attributes):
    num_attr = len(attributes)
    info = 0
    for x in range(len(attributes[i][1])):
        for y in range(len(attributes[j][1])):
            for c in range(len(attributes[len(attributes)-1][1])):
                priorset = [(i,x),(j,y)]
                postset = [(len(attributes)-1,c)]

                priorpij = calprior(data,priorset,postset,attributes)

                postpij = calpost(data,priorset,postset,attributes)

                priorset = [(i, x)]
                pi = calpost(data,priorset,postset,attributes)
                priorset = [(j, y)]
                pj = calpost(data,priorset,postset,attributes)

                info += priorpij * (math.log(postpij/(pi*pj))/math.log(2))

    return info

# use bfs to build DAG
def direction(edges, idx, visited):
    q = Queue()
    q.put(idx)
    visited.add(idx)
    while not q.empty():
        node = q.get()
        for i in range(len(edges[node])):
            if edges[node][i] == 1 and i not in visited:
                visited.add(i)
                edges[node][i]  = 0
                q.put(i)

# implement peek func for heap, bacause no build in func in python
def heappeek(heap):
    item = heappop(heap)
    heappush(heap,item)
    return item

# find the parents of each node
def findparent(idx, instance, edges):
    ret = []
    for i in range(len(edges[idx])-1):
        if edges[idx][i] == 1:
            ret.append((i,instance[i]))
    return ret

# the main function for tree augment naive bayes algo
def tan(data, test_data, attributes):
    num_attr = len(attributes)
    total = len(data)
    # compute the mutual information
    edges = [[0 for i in range(num_attr)] for j in range(num_attr)]
    visited = set()
    visited.add(0)
    nvertices = []
    nvertices.append(0)
    k = 0
    h = []

    # prims algo to build the maximum spanning tree
    while len(nvertices) < num_attr-1:
        node = nvertices[k]
        for j in range(len(edges[node])-1):
            if j not in visited and j != node:
                mutualinfo = calmutualinfo(data,node,j,attributes)
                heappush(h,(-mutualinfo,node,j))
        while(heappeek(h)[2] in visited):
            heappop(h)
            continue
        pop = heappop(h)
        nvertices.append(pop[2])
        visited.add(pop[2])
        edges[pop[1]][pop[2]] = 1
        edges[pop[2]][pop[1]] = 1
        k += 1

    # transform from graph to tree
    direction(edges,0,set())

    # debug for printing the tree
    # print the spanning tree
    # for row in range(len(edges)):
    #     for col in range(len(edges[0])):
    #         if edges[row][col] == 1:
    #             print col,row

    # make the class node connect to each attr node
    for i in range(num_attr-1):
        edges[i][-1] = 1

    # debug for printing the tree
    # print the tree in matrix form
    # for row in range(len(edges)):
    #     print row,edges[row]


    # compute post prob according to the evidence
    cnt = 0
    for instance in test_data:
        postprob = [1.0 for i in range(2)]
        for c in range(2):
            for i in range(num_attr):
                if i == num_attr-1:
                    priorset = [(i,c)]
                    postset = []
                else:
                    priorset = [(i,instance[i])]
                    postset = findparent(i,instance,edges)
                    postset.append((num_attr-1,c))
                postprob[c] *= calpost(data, priorset, postset, attributes)

        sumprob = sum(postprob)

        print instance[-1],
        if postprob[0] > postprob[1]:
            guess = 0
        else:
            guess = 1
        if guess == instance[-1]:
            cnt +=1
        print guess, max(postprob[0]/sumprob, postprob[1]/sumprob)
    print cnt
    return float(cnt)/len(test_data)



def naive_bayes(data, test_data, attributes):

    num_attr = len(attributes)
    total = len(data)
    n, p = 1, 1
    npd = [[] for i in range(num_attr-1)]
    ppd = [[] for i in range(num_attr-1)]
    for i in range(num_attr-1):
        for j in range(len(attributes[i][1])):
            npd[i].append(1)
            ppd[i].append(1)

    for i in range(total):
        instance = data[i]
        if instance[-1] == 0:
            n += 1
            for j in range(num_attr-1):
                npd[j][int(instance[j])] += 1
        elif instance[-1] == 1:
            p += 1
            for j in range(num_attr-1):
                ppd[j][int(instance[j])] += 1
    # test the model
    cnt = 0
    for i in range(len(test_data)):
        instance = test_data[i]
        nprob = 1.0
        for j in range(num_attr-1):
            nprob = nprob * npd[j][int(instance[j])]/float(sum(npd[j]))
        nprob = nprob*n/(total+2)

        pprob = 1.0
        for j in range(num_attr-1):
            pprob = pprob * ppd[j][int(instance[j])]/float(sum(ppd[j]))
        pprob = pprob*p/(total+2)

        prob = max(nprob/(nprob+pprob), pprob/(nprob+pprob))
        print instance[-1],
        if nprob > pprob:
            guess = 0
        else:
            guess = 1
        print guess,
        if guess == instance[-1]:
            cnt +=1
        print prob
    print cnt
    return float(cnt)/len(test_data)


def pickuprandom(num,data):
    ret = [0 for i in range(num)]
    for i in range(len(data)):
        if i<num:
            ret[i] = data[i]
        else:
            rand = random.randrange(0,i,2)
            if rand < num:
                ret[rand] = data[i]
    return ret



def drawcurves(func,data,test_data,attributes):
    arr = []
    # draw learning curve
    for i in [25, 50, 100]:
        meanarr = []
        for j in range(4):
            sampledata = pickuprandom(i, data)
            meanarr.append(func(sampledata, test_data,attributes))
        temp = reduce(lambda x, y: x + y, meanarr) / len(meanarr)
        arr.append(temp)
    return arr

def main():

    args = sys.argv
    train_files = None
    test_files = None
    para = None

    if len(args) < 4:
        train_files = "lymph_train.arff"
        test_files = "lymph_test.arff"
        para = args[1]
    else:
        train_files = args[1]
        test_files = args[2]
        para = args[3]

    train_data = arff.load(open(train_files, 'rb'))
    test_data = arff.load(open(test_files, 'rb'))

    data = train_data['data']
    attributes = train_data['attributes']
    testdata  = test_data['data']
    # encode the data
    # build the map from value to idx

    name2idx = [dict() for k in range(len(attributes))]

    for i in range(len(attributes)):
        for j in range(len(attributes[i][1])):
            name2idx[i][attributes[i][1][j]] = j

    ndata = [[] for i in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data[i])):
            ndata[i].append(name2idx[j][data[i][j]])

    ntestdata = [[] for i in range(len(testdata))]
    for i in range(len(testdata)):
        for j in range(len(testdata[i])):
            ntestdata[i].append(name2idx[j][testdata[i][j]])

    if para == 'n':
        print "Results of Naive Bayes:"
        naive_bayes(ndata,ntestdata,attributes)

    elif para == 't':
        print "Results of TAN:"
        tan(ndata,ntestdata,attributes)

    else:
        print "wrong para"

    # draw learning curves
    # tanresult = drawcurves(tan, ndata, ntestdata, attributes)
    # nbresult = drawcurves(naive_bayes, ndata, ntestdata, attributes)
    #
    # line1, = plt.plot([25, 50, 100], tanresult, "r--", label="TAN")
    # line2, = plt.plot([25,50,100], nbresult, label="Naive Bayes")
    # plt.scatter([25, 50, 100], tanresult)
    # plt.scatter([25, 50, 100], nbresult)
    # plt.xlabel("number of data")
    # plt.ylabel("acc")
    # plt.legend(loc= 'upper left')
    # plt.title("Learning curves of two methods")
    #
    # plt.show()



if __name__ == "__main__":
    main()