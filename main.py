from Robot import *
from World import *


if __name__ == '__main__':
    robots = [Robot([1, 2], (26, 26), -1, 10)]
    vis = World((30, 30), 30, robots)
    vis.run()
