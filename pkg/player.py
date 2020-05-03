#!/usr/bin/env python3

from pkg import strategy
from pkg.board import Board
from pkg.throw import Throw

from logging import getLogger

class Player(Throw, Board):
    
    """
    Playerクラス
    
    Attributes
    -----
    sigma : float
        命中精度（標準偏差）
    score : int
        ユーザのスコア
    strategy : Strategy
        行動管理クラス
    logger : logger
        ロガー
    aim_points : list
        狙う場所を管理する配列
        
    See Also
    ----- 
    pkg.board : ボードクラス
    pkg.throw : トスクラス
    """
    
    def __init__(self, score, sigma, game_type, logger=None, **game_params):
        """
        Parameters
        -----
        score : int
            スコア
        sigma : float
            命中精度(標準偏差)
        game_type : str (01 or cricket)
            ゲームの種類 
        game_params : dict of parameters of strategy class
            戦略クラスのパラメーター
        logger : logger
            ロガー
        """
        #親クラスの初期化
        Throw.__init__(self, sigma)
        
        #==変数の初期化
        #スコア
        self._score = score
        #ロガー
        self._logger = getLogger("darts") if logger is None else logger
        #Strategyクラス
        if game_type == "01":
            #TODO : strategy_parameter不正の処理
            self._strategy = strategy.zeroone.ZeroOne(**game_params)
            Board.__init__(self, game_params["bull_type"])
        else :
            raise ValueError("game_type must be 01 only.")
        #狙う場所
        self._aim_points = []
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score

    def calc_aims(self, hit_point_list=[]):
        """
        狙う場所を計算する
        
        Parameters
        -----
        hit_point_list : list of int
            同ラウンドで獲得したポイント数
        """
        #ロガー
        self._logger.info("Calclate aim points")
        #狙う場所を計算
        self._aim_points[len(hit_point_list):] = self._strategy.get_aims(self._score, hit_point_list)
        
        
    def play(self):
        """
        1ラウンドを行う関数。
        yieldを使ってgeneratorを返す
        
        Returns
        -----
        hit_result : bool
            狙った場所に当たったかどうか
        throw_result : dict 
           throwの結果
        """
            
        for n_throw in range(3):
            # 狙う場所を計算(ボード上の狙う座標)
            r, theta = self.get_aim_coordinate(self._aim_points[n_throw][2], self._aim_points[n_throw][1])
            #狙った結果、当たる場所を計算(当たる座標)
            r, theta = self.aim(r, theta)
            #当たる座標の情報を取得
            point, mark, place = self.calc_throw_result(r=r, theta=theta)
            throw_result = dict(point=point, mark=mark, place=place)
            
            #狙った場所に当たったかどうかの判定
            hit_result = (point == self._aim_points[n_throw][0])
                
            yield hit_result, throw_result

            