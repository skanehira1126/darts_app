#!/usr/bin/env python

import argparse
import numpy as np
import pandas as pd

class ArrangeHelper(object):
    
    #{n_mark:[points]}
    point_master = {n_mark:[place*n_mark for place in range(1, 21)] for n_mark in range(1,4)}

    #{n_mark : String}
    n_mark_master = {0:"bull", 1:"single", 2:"double", 3:"triple"}

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
    def search(cls, point, get_init=[], bull_type="fat", out_type="everything"):
        """
        1ラウンドで上がれるかを確認
        Parameters
        -----
        point : int
            ラウンド最初のポイント
        get_init : 
            すでに確定している得点
        bull_type : str
            ブルのタイプ
        out_type : str
            上がり方
        
        Returns
        -----
        flag : Bool
            上がれるかどうか
        points : list of list
            とるべきポイントの一覧
        """
        
        #引数チェック
        cls._check_args(bull_type=bull_type, out_type=out_type)
        cls.get_init = get_init
        
        #組み合わせList
        cls.finishable_points = []
        
        #探索
        if out_type == "everything":
            cls._search_points(point, get=get_init, out_flag=True)
        else:
            cls._search_points(point, get=get_init, out_flag=False)
        
        #すでに確定しているスローを消す
        
        if len(cls.finishable_points) != 0:
            return True, sorted(cls.finishable_points, key=cls.calc_score, reverse=True)
        else:
            return False, None
    
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
            return
        
        #上がれるパターンを追加
        if cls._check_finish(unenough_point, out_flag):
            #初期確定しているポイント分を削除
            get_real = get[len(cls.get_init):]
            points_list = sorted(get_real + [unenough_point])
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
        if cls.out_type == "double" and (point in cls.point_master[2] or point==50):
            return True
        elif cls.out_type == "master" and (point in cls.point_master[2]
                                          or point in cls.point_master[3]
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
        score = 4-len(points)
        if cls.bull_type == "sepa" or cls.out_type == "double": #sepaブルかdoubleアウトはブルを狙わない
            if (25 in points) or (50 in points):
                return 0
            else:
                return score
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
            
    @classmethod
    def convert_point(cls, point, last_flag):
        """
        ポイントをボードの場所に変換
        Parameters
        -----
        point : int 
            狙うポイント
        last_flag : bool
            上がるチャンスかどうか
        
        Returns
        -----
        board_place : list of [mark_name, place]
            ボードの場所
        
        Notes
        -----
        mark_name : str
            inner_bull, outer_bull, inner_single, outer_single,  double or triple
        """
            
        # 上がり方に制限があるとき
        if last_flag and cls.out_type != "everything":
            if cls.out_type == "double":
                mark_name = "double"
                place = int(point/2)
            elif  cls.out_type == "master":
                #masterアウトではbull -> double -> singleで優先順位をつける
                if point in cls.point_master[0]:
                    mark_name = "inner_bull"
                    place = 25
                elif point in cls.point_master[2]:
                    mark_name = "double"
                    place = int(point/2)
                elif point in cls.point_master[3]:
                    mark_name = "triple"
                    place = int(point/3)
        else : #どれでも良い
            for n_mark, points in cls.point_master.items():
                if n_mark == 0:
                    mark_name = "inner_bull"
                    place = 25
                    break
                else:
                    if point in points:
                        place = int(point/n_mark)
                        mark_name = cls.n_mark_master[n_mark]
                        if mark_name == "bull" :
                            mark_name = "inner_" + mark_name
                        elif mark_name == "single":
                            mark_name = "outer_" + mark_name
                        break
                    else:
                        #取得できるポイントがなかった場合
                        continue
        return [mark_name, place]