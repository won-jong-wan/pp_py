# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 23:27:02 2024

@author: jonwo
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

A = [
    [0, 1,  0,  .8, 0],
    [0, 0,  .4, 0,  .3],
    [0, 0,  0,  0,  0],
    [0, 0,  .6, 0,  .7],
    [0, 0,  0,  .2, 0]]

G = nx.from_numpy_array(np.matrix(A), create_using=nx.DiGraph)

pos=nx.spring_layout(G) # 각 노드, 엣지를 draw하기 위한 position 정보
weight = nx.get_edge_attributes(G, 'weight')

nx.draw(G,pos,with_labels=True)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)