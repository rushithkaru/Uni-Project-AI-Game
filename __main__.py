import sys
import json
from math import *
import copy

from search.util import *

def main():
    with open(sys.argv[1]) as file:
        #Dictionary with locations of all pieces
        data = json.load(file)

    initialStacks(data)
    goals = goal_find(data)
    ns = need_stacks(data)
    make_stack(data,ns)
    fix_data(data)
    find_moves(data)
    boom_loop(data['white'])


if __name__ == '__main__':
    main()
