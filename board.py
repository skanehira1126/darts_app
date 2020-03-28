#!/usr/bin/env python3

import numpy as np

class Board(object):
    """
    ダーツボード寸法
    
    Attributes
    -----
    bull : dict
        ブルの種類に対応したpoint
    total : int
        ボード半径
    Notes
    -----
        単位(mm)
        inner_bull = 18/2 = 9
        outer_bull = 44/2 = 22 
        inner_single = 84
        triple = 20
        outer_single = 52
        duble = 20
        totla = 198
    """
    total = 198

    def __init__(self, bull_type="fat"):
        """
        Parameters
        -----
        bull_type : str
            bullの種類
        """
        self.bull = {"inner_bull":50}
        if bull_type == "sepa":
            self.bull["outer_bull"] = 25
        elif bull_type == "fat":
            self.bull["outer_bull"] = 50
        else:
            raise ValueError("bull_type must be fat or sepa")
        
    def get_aim_coordinate(self, point, place):
        """ 
        狙う場所の座標を取得
        
        Parameters
        ----- 
        place : str
            どこを狙うか(inner_single, outer_single, double, triple, inner_bull outer_bull)
        point : int
            基礎ポイント(1~20, 25)
            
        Returns
        -----
        radious : float
            狙う座標の距離部分
        theta : float
            狙う座標の角度部分
        """
        
        radious = self._get_radious(place)
        theta = self._get_theta(point)
        
        return radious, theta
    
    def throw(self, r, theta):
        """
        ポイント計算
        
        Parameters
        -----
        r : float
            当たった座標の距離成分
        theta : float
            当たった座標の角度成分
            
        Returns
        -----
        point : int
            当たった場所に応じたポイント
        """
        
        place = self._get_place(r)
        if "bull" in place:
            return self.bull[place]
        elif place == "out_board":
            return 0
        else:
            return self._get_point(theta)
    
    
    def _get_place(self, r):
        """
        距離からbull, single, duble, tripleを判定
        
        Parameters
        -----
        r : float
            座標の距離成分
            
        Returns
        -----
        place : str
            inner_bull, outer_bull, single, double, triple, out_board
        """
        
        if 0 <= r <= 9:
            return "inner_bull"
        elif 9 < r <= 22:
            return "outer_bull"
        elif 22 < r <= 106 or 126 < r <= 178:
            return "single"
        elif 106 < r <= 126:
            return "triple"
        elif 178 < r <= 198:
            return "double"
        else:
            return "out board"
    
    def _get_point(self, theta):
        """
        距離からbull, single, duble, tripleを判定
        
        Parameters
        -----
        theta : float 
            座標の角度成分
            
        Returns
        -----
        point : int
            0 ~ 20の整数
            
        Notes
        -----
        一つのピザの角度はπ/10
        """
        
        if 0 <= theta <= np.pi/20 or 39*np.pi/20 < theta <= 2*np.pi:
            return 20
        elif 1*np.pi/20 < theta <= 3*np.pi/20:
            return 1
        elif 3*np.pi/20 < theta <= 5*np.pi/20:
            return 18
        elif 5*np.pi/20 < theta <= 7*np.pi/20:
            return 4
        elif 7*np.pi/20 < theta <= 9*np.pi/20:
            return 13
        elif 9*np.pi/20 < theta <= 11*np.pi/20:
            return 6
        elif 11*np.pi/20 < theta <= 13*np.pi/20:
            return 10
        elif 13*np.pi/20 < theta <= 15*np.pi/20:
            return 15
        elif 15*np.pi/20 < theta <= 17*np.pi/20:
            return 2
        elif 17*np.pi/20 < theta <= 19*np.pi/20:
            return 17
        elif 19*np.pi/20 < theta <= 21*np.pi/20:
            return 3
        elif 21*np.pi/20 < theta <= 23*np.pi/20:
            return 19
        elif 23*np.pi/20 < theta <= 25*np.pi/20:
            return 7
        elif 25*np.pi/20 < theta <= 27*np.pi/20:
            return 16
        elif 27*np.pi/20 < theta <= 29*np.pi/20:
            return 8
        elif 29*np.pi/20 < theta <= 31*np.pi/20:
            return 11
        elif 31*np.pi/20 < theta <= 33*np.pi/20:
            return 14
        elif 33*np.pi/20 < theta <= 35*np.pi/20:
            return 19
        elif 35*np.pi/20 < theta <= 37*np.pi/20:
            return 12
        elif 37*np.pi/20 < theta <= 39*np.pi/20:
            return 5
        else:
            raise ValueError("theta must be 0 <= theta <= 2*np.pi")
            
    def _get_radious(self, place):
        """
        single or double or triple or bull中心の距離を計算
        
        Parameters
        -----
        place : str
            inner_bull, outer_bull, inner_single, outer_single, double, triple
            
        Returns
        -----
        r : float
            座標の距離成分
            
        Notes
        -----
        セパブルでouter bullを狙うのは現実的ではないのでとりあえず中心を狙う
        """
        
        if place in ["inner_bull", "outer_bull"]: #意図的にsingleを狙うのは現実的ではない
            return 0
        elif place == "inner_single":
            return 22 + 84/2 # bullの外側 + inner_singleの半分 
        elif place == "triple":
            return 106 + 20/10 # inner_singleの外側 + tripleの半分
        elif place == "outer_single":
            return 126 + 52/2 # tripleの外側 + outer_singleの半分
        elif place == "double":
            return 178 + 20/10 # outer_singleの外側 + doubleの半分
        else :
            raise ValueError("place must be inner_bull, outer_bull, inner_single, triple, outer_single or double.")
            
    def _get_theta(self, point):
        """
        pointから角度の取得
        
        Parameters
        -----
        point : int
            0 ~ 20の整数もしくは25
            
        Returns
        -----
        theta : float
            pointの座標の角度成分中心
            
        Notes
        -----
        一つのピザの角度はπ/10
        BULLを狙うときはとりあえず角度0
        """
        
        if point == 20 or point == 25:
            return 0
        elif point == 1:
            return np.pi/10
        elif point == 18:
            return 2*np.pi/10
        elif point == 4:
            return 3*np.pi/10
        elif point == 13:
            return 4*np.pi/10
        elif point == 6:
            return 5*np.pi/10
        elif point == 10:
            return 6*np.pi/10
        elif point == 15:
            return 7*np.pi/10
        elif point == 2:
            return 8*np.pi/10
        elif point == 17:
            return 9*np.pi/10
        elif point == 3:
            return 10*np.pi/10
        elif point == 19:
            return 11*np.pi/10
        elif point == 7:
            return 12*np.pi/10
        elif point == 16:
            return 13*np.pi/10
        elif point == 8:
            return 14*np.pi/10
        elif point == 11:
            return 15*np.pi/10
        elif point == 14:
            return 16*np.pi/10
        elif point == 9:
            return 17*np.pi/10
        elif point == 12:
            return 18*np.pi/10
        elif point == 5:
            return 19*np.pi/10
        else:
            raise ValueError("theta must be 1 <= point <= 20")
            
    