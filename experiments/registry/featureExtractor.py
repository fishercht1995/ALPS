import datetime
import igraph
import time
import os
import sys
from datetime import datetime
import re
def f(n):

    start = round(time.time(),6)
    #sleep_time = args.get("time","50")
    n = int(n)
    in_file = "/datain/shakespeare_dataset.txt"
    data = open(in_file,"r").read()
    cleanup_re = re.compile('[a-z]+')
    result = cleanup_re.findall(data)
    end = round(time.time(),6)