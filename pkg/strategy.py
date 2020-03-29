import numpy as np
import pandas as pd

from pkg.arrange_helper import ArrangeHelper

class Strategy(object):
    
    #スコア格納用dfのパラメータ
    columns = ["point", "n_throw", "n_pattern"]
    arrange_score_master = pd.DataFrame([], columns=columns)
    all_score_master = pd.DataFrame([], columns=columns)
    
    def __init__(self, bull_type, out_type):
        self.bull_type = bull_type
        self.out_type = out_type
        #スコア計算
        self._calc_scores()
    
    def _calc_scores(self):
        for n_throw in range(1,4):
            for point in range(1, 60 * n_throw + 1):
                #上がり条件がある得点一覧
                flag, point_list = ArrangeHelper.search(point, get_init=[0]*(3-n_throw)
                                                        , bull_type=self.bull_type, out_type=self.out_type)
                if flag :
                    self.arrange_score_master = pd.concat([self.arrange_score_master
                                                           , pd.DataFrame([[point, n_throw, len(point_list)]]
                                                           , columns=self.columns)])
                
                #上がりを気にしないで取得できる得点一覧
                flag, point_list = ArrangeHelper.search(point, get_init=[0]*(3-n_throw)
                                                        , bull_type=self.bull_type, out_type="everything")
                if flag :
                    self.all_score_master = pd.concat([self.all_score_master
                                                       , pd.DataFrame([[point, n_throw, len(point_list)]]
                                                       , columns=self.columns)])
            #値をソート
            self.arrange_score_master = self.arrange_score_master.sort_values("n_pattern", axis=0, ascending=False)
            self.all_score_master = self.all_score_master.sort_values("n_pattern", axis=0, ascending=False)
    
    def get_aims(self, left_point, get=[]):
        """
        狙う場所を返す
        
        Parameters
        -----
        left_point : int
            残りポイント
        
         Returns
         -----
         aims : list of board_list
             狙う場所のリスト
        """
        
        #聴牌可能性
        n_throw = 3 - len(get)
        if 180 + 180*(n_throw)/3 < left_point: #聴牌できない
            aims = self._get_aims_not_finishable(n_throw)
        else: #聴牌できる or 上がれる
            flag, point_list = ArrangeHelper.search(left_point, get_init=get, bull_type=self.bull_type, out_type=self.out_type)
            if flag : #上がれる
                #一番スコアが高い点の組み合わせを取得
                aim_point_list = point_list[0]
                #変換
                aims = self.convert_point_list(aim_point_list)  
            else : #上がれない
                arrange_point = self.get_arrange_point(left_point, get)
                print("arrange_point: ",arrange_point)
                print(get)
                if arrange_point is None: #アレンジできない
                    aims = self._get_aims_not_finishable(n_throw)
                else: #アレンジできる
                    print(left_point, arrange_point)
                    _, point_list = ArrangeHelper.search(left_point-arrange_point, get_init=get
                                                         , bull_type=self.bull_type, out_type="everything")
                    #一番スコアが高い点の組み合わせを取得
                    aim_point_list = point_list[0]
                    #変換
                    aims = self.convert_point_list(aim_point_list)
        return aims

    def _get_aims_not_finishable(self, n_throw):
        """
        上がれない場合の基本戦略
        
        Paramters
        -----
        n_throw : int
            投げれる回数

        Returns
        -----
        aims : list of board_place
            狙う場所
        """
        if self.bull_type == "fat":
            aims = [[25, "inner_bull", 50]] * n_throw
        elif self.bull_type == "sepa":
            aims = [[20, "triple", 120]] * n_throw
        return aims
    
    def convert_point_list(self, point_list):
        """
        ポイントリストを変換する
        [p1, p2, p3] -> [[place, n_mark, point], [place, n_mark, point], [place, n_mark, point]]
        
        Parameters
        -----
        point_list : list of int
            狙うポイントの組み合わせ
        
        Returns
        -----
        board_place : list of list
            ボードの場所
        """
        board_place_list = []
        if self.bull_type == "sepa": 
            if self.out_type == "double":
                point_list = sorted(point_list, key=_sort_func_of_double)
            elif self.out_type == "master":
                point_list = sorted(point_list, key=_sort_func_of_sepa_master)
            else :
                point_list = sorted(point_list, reverse=True)
                    
        elif self.bull_type == "fat":
            if self.out_type == "double":
                point_list = sorted(point_list, key=_sort_func_of_double)
            elif self.out_type == "master":
                point_list = sorted(point_list, key=_sort_func_of_fat_master)
            else :
                point_list = sorted(point_list, reverse=True)
        
        #変換
        for idx, p in enumerate(point_list):
            last_flag = (len(point_list) == idx+1)
            board_place = ArrangeHelper.convert_point(p, last_flag)
            board_place_list.append(board_place + [p])
        
        return board_place_list
                    
        
    def get_arrange_point(self, left_point, get):
        """
        アレンジするポイントを探す
        
        Parameters
        -----
        left_point : int 
            残りポイント数
        get : list of int
            取得ポイント数
        
        Returns
        -----
        arrange_point : int
            アレンジで目指すポイント
        """
        #探索する得点の範囲
        p_range = self._get_point_range(left_point-sum(get))
        #ポイントの範囲で絞る
        arrange_point_list = self.arrange_score_master[self.arrange_score_master.point.map(lambda x : p_range[0] <= x <= p_range[1])]
        if arrange_point_list.shape[0] == 0:
            return None
        else :
            #残りトス数で絞る
            arrange_point_list = arrange_point_list[arrange_point_list.n_throw==(3-len(get))]
            if arrange_point_list.shape[0] == 0:
                return None
            else :
                #アレンジのための点数を取得できるか
                for arrange_point in arrange_point_list.point.values:
                    #残りのトス数で取れるポイントの一覧を取得
                    candidate_point_list = self.all_score_master[self.all_score_master.n_throw==(3-len(get))].point.values
                    if left_point - sum(get) - arrange_point in candidate_point_list:
                        return int(arrange_point)
                else:
                    return None
        
    def _get_point_range(self, left_point):
        """
        探索するポイントの範囲を計算
        Parameters
        -----
        left_point : int
            残りポイント数
        
        Returns
        -----
        p_range : range
            探索するポイントの範囲
        """
        if left_point > 180 :
            p_range = [max(left_point-180, 0), 181]
        else :
            p_range = [1, left_point+1]
        return p_range
    
#ダブルアウトの場合ブルは最終手段なのでsepa, fat関係ない
def _sort_func_of_double(point):
    if point == 50:
        return 0.1
    if point%2 == 0 and point <= 40:
        return 1
    else :
        return 0

def _sort_func_of_sepa_master(point):
    if point%2 != 0 and point%3 != 0:
        return 0
    if point in [25, 50]:
        return 0.1
    if point%2 == 0 and point <= 40:
        return 1
    if point%2 == 3:
        return 0.5


def _sort_func_of_fat_master(point):
    if point%2 != 0 and point%3 != 0:
        return 0
    if point == 50:
        return 1.5
    if point%2 == 0 and point <= 40:
        return 1
    if point%3 == 0:
        return 0.5
    