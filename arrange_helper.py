#!/usr/bin/env python

import argparse
import numpy as np

class ArrangeHelper(object):
    
    #{n_mark:{points:num}}
    point_master = {coef: {place*coef:place for place in range(1, 21)}  for coef in range(1,4)}

    #{coef : String}
    coef_master = {1:"Single", 2:"Double", 3:"Triple"}

    @classmethod
    def _check_args(cls, **args):
        """
        引数のチェック
        
        Parameters
        -----
        bull_type : str 
            ブルのタイプ
        
        out_type : str
            アウトのタイプ
        
        Raises
        ------
        SystemExit
            引数のミス
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("bull_type", choices=["fat", "sepa"])
        parser.add_argument("out_type", choices=["master", "double", "everything"])
        #引数の確認
        args = parser.parse_args([args["bull_type"], args["out_type"]])
        
        #変数の追加
        if args.bull_type == "fat":
            cls.point_master[1][50] = 25
            cls.point_master[2][50] = 25
        else:
            cls.point_master[1][25] = 25
            cls.point_master[2][50] = 25
        
        cls.out_type = args.out_type
            
    @classmethod
    def search(cls, point, bull_type="fat", out_type="everything"):
        #引数チェック
        cls._check_args(bull_type=bull_type, out_type=out_type)
        
        #組み合わせList
        cls.finishable_points = []
        
        cls._search_coef(point)
        
        return cls.finishable_points
    
    @classmethod
    def _search_coef(cls, point, get=[]):
        #足りないポイントを計算
        unenough_point = point-sum(get)
        if unenough_point < 0 :
            return
        finishable_points = cls._check_finish(unenough_point)
        if finishable_points != []:
            for finish_point in finishable_points:
                points_list = sorted(get + [finish_point])
                if points_list not in cls.finishable_points:
                    cls.finishable_points.append(points_list)
        
        #3投投げたのでおしまい
        if len(get) == 2:
            return
        
        #得点の候補作成
        candidate_point_list = list(cls.point_master[3].keys())
        if unenough_point <= 50*(3-len(get)):
            candidate_point_list += list(cls.point_master[2].keys())
        if unenough_point <= 25*(3-len(get)):
            candidate_point_list += list(cls.point_master[1].keys())

        candidate_point_list = list(set(candidate_point_list))
        #print(candidate_point_list)
        for candidate_point in candidate_point_list:
            cls._search_coef(point, get+[candidate_point])
    
    @classmethod
    def _check_finish(cls, point):
        point_list = [point for coef in [1, 2, 3] if point in cls.point_master[coef].keys()]
        return list(set(point_list))
    
    