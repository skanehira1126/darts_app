#!/usr/bin/env python

import argparse
import numpy as np
import pandas as pd

class ArrangeHelper(object):
    
    #{n_mark:[points]}
    point_master = {n_mark:[place*n_mark for place in range(1, 21)] for n_mark in range(1,4)}

    #{n_mark : String}
    n_mark_master = {0:"Bull", 1:"Single", 2:"Double", 3:"Triple"}

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
            argparserによる引数のミスの検知
        """
        
        parser = argparse.ArgumentParser()
        parser.add_argument("bull_type", choices=["fat", "sepa"])
        parser.add_argument("out_type", choices=["master", "double", "everything"])
        #引数の確認
        args = parser.parse_args([args["bull_type"], args["out_type"]])
        
        #変数の追加
        cls.bull_type = args.bull_type
        if args.bull_type == "fat":
            cls.point_master[0] = [50]
        else:
            cls.point_master[0] = [25, 50]
            
        #上がり方のチェック
        cls.out_type = args.out_type
        
    @classmethod
    def search(cls, point, bull_type="fat", out_type="everything"):
        """
        1ラウンドで上がれるかを確認
        Parameters
        -----
        point : int
            ラウンド最初のポイント
        bull_type : str
            ブルのタイプ
        
        Returns
        -----
        flag : Bool
            上がれるかどうか
        points : list of list
            とるべきポイントの一覧
        """
        
        #引数チェック
        cls._check_args(bull_type=bull_type, out_type=out_type)
        
        #組み合わせList
        cls.finishable_points = []
        #cls
        cls.under_180_list = []
        
        #探索
        if out_type == "everything":
            cls._search_points(point, get=[], out_flag=True)
        else:
            cls._search_points(point, get=[], out_flag=False)
        if len(cls.finishable_points) != 0:
            return True, sorted(cls.finishable_points, key=cls.calc_score, reverse=True)
        else:
            return False, cls.under_180_list
    
    @classmethod
    def _search_points(cls, point, get=[], out_flag=False):
        """
        上がることのできる or 次上がれる可能性のある点の組み合わせを探す
        
        Parameters
        -----
        point : int
            取得したい得点
        get : list of int
            同じラウンド中にとった得点
        out_flag : bool
            上がり条件を満たしているかどうか
        """
        #足りないポイントを計算
        unenough_point = point-sum(get)
        if unenough_point < 0 :
            return
        #3投投げたのでおしまい
        if len(get) == 3:
            if point-sum(get) <= 180:
                cls.under_180_list.append(get)
            return
        
        if cls._check_finish(unenough_point, out_flag):
            points_list = sorted(get + [unenough_point])
            if points_list not in cls.finishable_points:
                cls.finishable_points.append(points_list)
        #得点の候補作成
        #=====
        # 50 < point <= 60 : tripleのみ
        # 40 < point <= 50 : triple + double bull
        # 25 < point <= 40 : triple + double bull + double
        # 20 < point <= 25 : triple + double bull + double + inner_bull
        # point <= 20 : triple + double bull + double + inner_bull + single
        #=====
        candidate_point_list = []
        if unenough_point <= 60*(3-len(get)):
            candidate_point_list += list(cls.point_master[3])
        if unenough_point <= 50*(3-len(get)):
            candidate_point_list += [50]
        if unenough_point <= 40*(3-len(get)):
            candidate_point_list += list(cls.point_master[2])
        if cls.bull_type == "sepa" and unenough_point <= 25*(3-len(get)):
            candidate_point_list += [25]
        if unenough_point <= 20*(3-len(get)):
            candidate_point_list += list(cls.point_master[1])

        candidate_point_list = list(set(candidate_point_list))
        for candidate_point in candidate_point_list:
            #上がり条件を確認
            out_condition_flag = cls._check_out_condition(out_flag, candidate_point)
            #さらに探索
            cls._search_points(point, get+[candidate_point], out_condition_flag)
    
    @classmethod
    def _check_finish(cls, point, out_flag):
        """
        上がれるかチェック
        
        Parameters
        -----
        point : int
            探索する点
        out_flag : bool
            上がり条件を満たしているかどうか
        Returns
        -----
        finishable_flag : bool
            終われるかどうか
        """
        #とって良いポイント
        candidate_points = []
        #上がり条件を満たしている時
        if out_flag:
            candidate_points += list(cls.point_master[0])
            candidate_points += list(cls.point_master[1])
            candidate_points += list(cls.point_master[2])
            candidate_points += list(cls.point_master[3])
        else : 
            if cls.out_type == "double":
                candidate_points += [50]
                candidate_points += list(cls.point_master[2])
            elif cls.out_type == "master":
                candidate_points += list(cls.point_master[0])
                candidate_points += list(cls.point_master[2])
                candidate_points += list(cls.point_master[3])
            
        if point in candidate_points:
            return True
        else :
            return False
     
    @classmethod
    def _check_out_condition(cls, out_flag, point):
        """
        上がり条件を満たしているか確認
        Parameters
        -----
        out_flag : bool
            現在の上がり条件フラグ
        point : int
            確認するポイント
        
        Returns
        -----
        out_condition_flag : bool
            上がり条件を満たしているかどうか
        """

        #既に満たしている場合はOK
        if out_flag :
            return True
        #満たしていない場合、確認
        if cls.out_type == "double" and point%2 == 0 :
            return True
        elif cls.out_type == "master" and (point%2 == 0
                                          or point%3 == 0
                                          or point in cls.point_master[0]):
            return True
        #どの条件も満たさない場合、False
        return False

    @classmethod
    def calc_score(cls, points):
        """
        ソートに用いる
        スコアを計算。
        1. bull_typeを検証
            * sepa : bullを狙わない
            * fat : bullを積極的に使う
        2. out_typeを検証
            * double : bull無視
            * master : bull->double->tripleで優先順位をつける
            * everything : single優先
        
        Parameters
        ----- 
        points : list of int
            とるポイント
        
        Returns
        -----
        score : float
            とるポイントの組み合わせのスコア
        """
        score = 0
        if cls.bull_type == "sepa" or cls.out_type == "double": #sepaブルかdoubleアウトはブルを狙わない
            if (25 in points) or (50 in points):
                return 0
            else:
                return 1
        if cls.out_type == "everything" : 
            for p in points:
                if p <= 20 :
                    score = score + 1
        elif cls.out_type == "master":
            for p in sorted(points, reverse=True):
                if p == 50 : # bullが一番良い
                    score = score + 1.5
                    break
                if p % 2 == 0 : #次にダブル
                    score = score + 1
                    break
            else: #最後トリプル
                score = score + 0.5 
        return score
            