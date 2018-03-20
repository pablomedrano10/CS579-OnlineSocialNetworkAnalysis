
import networkx as nx


def jaccard_wt(graph, node):
    result = []
    list1 = []
    list2 = []
    sum1 = 0

    for i in list(graph.neighbors(node)):

        list1.append((i,list(graph.neighbors(i))))
        list2.append(set(list(graph.neighbors(node))) & set(list(graph.neighbors(i))))
        sum1 += graph.degree(i)

    while list1:

        list3 = list1.pop()
        common = list2.pop()
        sum2 = 0
        sum3 = 0

        for j in list3[1]:

            sum2 += graph.degree(j)

        for k in common:

            if k != node and k != list3[0]:
                sum3 += 1/graph.degree(k)

        result.append(((node,list3[0]), sum3/(1/sum1+1/sum2)))

    result = sorted(result, key=lambda x: x[0][1])
    return result
