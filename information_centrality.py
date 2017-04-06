# -*- coding: utf-8 -*-
import networkx as nx
from heapq import heappush, heappop
from itertools import count
import json
import math
from math import sqrt
import functools
import sys
from straightness_centrality import straightness_centrality

def parseNodes(filename):
    with open(filename, "r") as f:
        data = json.load(f, encoding="utf-8")
    features = [feature for feature in data["features"]]
    nodes    = []
    for feature in features:
        coordinates = feature['geometry']['coordinates']
        nodes.append(str(coordinates[0]))
        nodes.append(str(coordinates[-1]))
    return list(set(nodes))
def parseEdges(filename):
    with open(filename, "r") as f:
        data = json.load(f, encoding="utf-8")
    features = [feature for feature in data["features"]]
    edges    = []
    for feature in features:
        coordinates = feature["geometry"]["coordinates"]
        heisoku2    = feature["properties"]["Heisoku2"]
        if 1-math.fabs(heisoku2) == 0:
            p = 1000000000000
        else:
            p = math.fabs(math.log(1-math.fabs(heisoku2), 10))
        edges.append((str(coordinates[0]), str(coordinates[-1]), {"weight": sqrt((coordinates[0][0] - coordinates[-1][0])**2 + (coordinates[0][1] - coordinates[-1][1])**2)}))
    return edges
def euclidean_distance(xs, ys, xt, yt):
    return sqrt((xs - xt)**2 + (ys - yt)**2)

def information_centrality(G, weight="weight"):
    Ci  = {}
    EG  = straightness_centrality(G, weight) / len(G.nodes())
    Eg  = sum(list(EG.values()))
    ns  = G.nodes()
    for n in Graph.nodes():
        Gt = G.copy()
        for neighbor in G.neighbors(n):
            Gt.remove_edge(n, neighbor)
        delta_EG  =  (Eg - sum(list(straightness_centrality(Gt, weight).values()))) / len(G.nodes())
        Ci[n] = delta_EG / Eg
        print(n)
    return Ci

def main():
    filename = "map.geojson"
    Graph = nx.Graph()
    nodes = parseNodes(filename)
    edges = parseEdges(filename)
    for node in nodes:
        Graph.add_node(node, pos=(float(node.split(',')[0].replace('[', '')), float(node.split(',')[1].replace(' ', '').replace(']', ''))))
    Graph.add_edges_from(edges)
    Ci = information_centrality(Graph)
    with open("information_centrality" + argv0 + "-" + argv1 + ".json", "w") as f:
        f.write(json.dumps(Ci))

if __name__ == '__main__':
    main()
