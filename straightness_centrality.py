# -*- coding: utf-8 -*-
import networkx as nx
from heapq import heappush, heappop
from itertools import count
import json
import math
from math import sqrt
import functools
import sys
import random

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

def straightness_centrality(G, weight="weight", normalized=True, seed = None):
    random.seed(seed)
    path_length          = functools.partial(nx.single_source_dijkstra_path_length, weight=weight)
    shortest_path_length = functools.partial(nx.shortest_path_length, weight=weight)

    nodes = G.nodes()
    Cs    = {}
    for n in nodes:
        straightness = 0.0
        sp           = path_length(G, n)
        if len(sp) > 0 and len(G) > 1:
            coords_source = list(nx.get_node_attributes(G, 'pos')[n])
            if coords_source is not None:
                for target in sp:
                    if n != target:
                        coords_target  = list(nx.get_node_attributes(G, 'pos')[target])
                        network_dist   = sp[target]
                        euclidean_dist = euclidean_distance(coords_source[0], coords_source[1], coords_target[0], coords_target[1])
                        straightness   += ( euclidean_dist / network_dist )
                Cs[n] = straightness / (len(G) - 1.0)
                if normalized and len(sp) > 1.0:
                    s = ( len(G) - 1.0 ) / ( len(sp) - 1.0 )
                    Cs[n] *= s
        else:
            Cs[n] = 0.0
    return Cs

def main():
    filename = "map.geojson"
    Graph = nx.Graph()
    nodes = parseNodes(filename)
    edges = parseEdges(filename)
    for node in nodes:
        Graph.add_node(node, pos=(float(node.split(',')[0].replace('[', '')), float(node.split(',')[1].replace(' ', '').replace(']', ''))))
    Graph.add_edges_from(edges)
    Cs = straightness_centrality(Graph)
    with open("straightness_centrality10.json", "w") as f:
        f.write(json.dumps(Cs))

if __name__ == '__main__':
    main()
