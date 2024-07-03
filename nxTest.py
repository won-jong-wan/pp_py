# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 23:27:02 2024

@author: jonwo
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

c = 1
r = 1

adj_matrix = [
    [0, c, 0, r+c, 0, 0],
    [c, 0, c, 0, r+c, 0],
    [0, c, 0,  0, 0, r+c],
    [r+c, 0, 0, 0, c, 0],
    [0, r+c, 0, c, 0, c],
    [0, 0, r+c, 0, c, 0]]

grid = nx.from_numpy_array(np.matrix(adj_matrix), create_using=nx.DiGraph)

pos=nx.spring_layout(grid) # 각 노드, 엣지를 draw하기 위한 position 정보
weight = nx.get_edge_attributes(grid, 'weight')

nx.draw(grid,pos,with_labels=True)
nx.draw_networkx_edge_labels(grid,pos, edge_labels=weight)