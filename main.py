#!/usr/bin/env python3
import time
import sys
from logging import getLogger

from pkg.logger_util import init_logger
from pkg.player import Player


#parameter
bull_type = "fat"
out_type = "everything"
#標準偏差
sigma = 100

init_logger("darts.log")
logger = getLogger("darts")

player = Player(score=501, sigma=10, game_type="01", bull_type="fat", out_type="everything")
for round_num in range(1, 21):
    logger.info("=================")
    logger.info("Start round  {} : ".format(round_num))
    logger.info("Point  {} : ".format(player.score))
    #狙うポイントを計算
    player.calc_aims()
    #当たったところを覚えておく配列
    hit_point_list = []
    for hit_result, throw_result in player.play():
        point = throw_result["point"]
        mark = throw_result["mark"]
        place = throw_result["place"]
        print(f"point : {point}, mark : {mark}, place : {place}")
        logger.info(f"point : {point}, mark : {mark}, place : {place}")
        hit_point_list.append(point)
        
        #BURSTチェック
        #物理的に取れない点数になった場合
        if player.score - sum(hit_point_list) < (0 + int(out_type in ["double", "master"])):
            logger.info("BURST : {}".format(player.score - sum(hit_point_list) ))
            hit_point_list = []
            break
        elif player.score - sum(hit_point_list) == 0 and (out_type in ["double", "master"]):
            mark_rules = ["inner_bull", "double"]
            if out_type == "master" :
                mark_rules += ["outer_bull", "triple"]
            if mark not in mark_rules:
                logger.info("BURST : {}".format(player.score - sum(hit_point_list) ))
                hit_point_list = []
                break

        #上がりチェック
        if player.score - sum(hit_point_list) == 0:
            if out_type == "double" and (mark in ["inner_bull", "double"]):
                logger.info("Finished")
                sys.exit(0)
            elif out_type == "master" and (mark in ["inner_bull", "outer_bull", "double", "triple"]):
                logger.info("Finished")
                sys.exit(0)
            elif out_type == "everything":
                logger.info("Finished")
                sys.exit(0)
                
        #外れた場合の目標再計算
        player.calc_aims(hit_point_list)
    
    print("hit_point_list", hit_point_list)
    player.score = player.score - sum(hit_point_list)
    time.sleep(1)

