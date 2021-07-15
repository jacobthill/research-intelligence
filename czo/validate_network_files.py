import math
import numpy as np
import pandas as pd
from itertools import combinations


f = open('output/pubs_author_graph.txt', 'r')
for line in f.readlines()[1:]:
    print(line)
