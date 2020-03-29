#!/usr/bin/env python3

import time
import sys
import argparse
from pprint import pprint

from pkg.logger_util import init_logger
from pkg.strategy import Strategy
from pkg.board import Board
from pkg.throw import Throw

import numpy as np

#parameter
bull_type = "fat"
out_type = "double"
#標準偏差
st = Strategy(bull_type, out_type)
sigma = 50
throw = Throw(sigma)

bd = Board(bull_type)

point = 501
for round_num in range(1, 21):
    print("=====", round_num)
    print("left point", point)
    aim_points = st.get_aims(point)
    print("aim_points", aim_points)
    hit_point_list = []
    for i in range(3):
        r, theta = bd.get_aim_coordinate(aim_points[i][0], aim_points[i][1])
        r, theta = throw.aim(r, theta)
        hit_point, place, base_point = bd.throw(r=r, theta=theta)
        print(hit_point)
        hit_point_list.append(hit_point)

        #上がりチェック
        if point - sum(hit_point_list) == 0:
            if out_type == "double" and (place in ["inner_bull", "double"]):
                sys.exit(0)
            elif out_type == "master" and (place in ["inner_bull", "outer_bull", "double", "triple"]):
                sys.exit(0)
            else:
                print("BREAK")
                hit_point_list = []
                break
        elif point - sum(hit_point_list) < (0 + int(out_type in ["double", "master"])):
            print("BREAK")
            hit_point_list = []
            break

        #狙った場所から外した場合、再計算
        if i != 2 and hit_point != aim_points[i][2]:
            print("Miss and update aim_points")
            aim_points[i+1:] = st.get_aims(point, hit_point_list)
            print(aim_points)

    print("hit_point_list", hit_point_list)
    point = point - sum(hit_point_list)
    time.sleep(1)



