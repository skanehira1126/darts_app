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
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score
        
    def play(self, round_num = 0):
        """
        1ラウンドを行う関数。
        yieldを使ってgeneratorを返す
        Parameters 
        -----
        round_num : int default 0
            ラウンド数
        """
        #狙う場所を計算
        aim_points = self._strategy.get_aims(self._score)
        
        self._logger.info(f"===== Start Round　 {int(round_num)}")
        self._logger.info(f"aim points : {str(aim_points)}")
        
        #当たった場所を記録するリスト
        hit_point_list = []
        for n_throw in range(3):
            # 狙う場所を計算(ボード上の狙う座標)
            r, theta = self.get_aim_coordinate(aim_points[n_throw][0], aim_points[n_throw][1])
            #狙った結果、当たる場所を計算(当たる座標)
            r, theta = self.aim(r, theta)
            #当たる座標の情報を取得
            hit_point, place, base_point = self.calc_throw_result(r=r, theta=theta)
            hit_point_list.append(hit_point)
                
            yield hit_point, place, base_point

            #狙った場所から外した場合、再計算
            if n_throw != 2 and hit_point != aim_points[n_throw][2]:
                #狙う点を計算し直す
                aim_points[n_throw+1:] = self._strategy.get_aims(hit_point, hit_point_list)
                # ログ出力
                self._logger.info("Miss...")
                self._logger.debug(f"aim point : {aim_points[n_throw][2]}")
                self._logger.debug(f"hit_point : {hit_point}")
                self._logger.info(f"Update aim points : {str(aim_points)}")