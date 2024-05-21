import datetime
import igraph
import time
import os
import sys
from datetime import datetime

def f(n):

    start = round(time.time(),6)
    #sleep_time = args.get("time","50")
    n = int(n)

    size = int(n)
    graph = igraph.Graph.Barabasi(size, size)

    result = graph.spanning_tree(None, False)
    end = round(time.time(),6)