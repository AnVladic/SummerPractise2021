from Robot import *
from World import *


if __name__ == '__main__':
    robots = [Robot([1, 2], (9, 9), -1, 10)]
    vis = World((11, 11), 60, robots)
    vis.run()
