#!/usr/bin/env python3

import numpy as np

class Throw(object):
    """
    Throwクラス
    
    Attributes
    ----------
    sigma : float
        狙った地点からずれた距離の分散
    """
    def __init__(self, sigma):
        """
        Parameters
        -----
        sigma : float
            狙った地点からずれた距離の分散
        """
        self.sigma = sigma
        
    def aim(self, r, theta):
        """
        当たった地点の座標を求める
        
        Parameters
        -----
        r : float
            狙った地点の座標の距離部分
        theta: float
            狙った地点の座標の角度部分
            
        Returns
        -----
        r_hit : float
            当たった座標の距離部分
        theta_hit : float
            当たった座標の角度部分
        """
        #誤差距離と誤差角度の計算
        r_d = np.abs(np.random.normal(0, self.sigma))
        theta_d = np.random.choice(np.arange(-1, 1, 0.01)) * np.pi
        
        #当たった座標を計算
        #直交座標系で計算する
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        
        #誤差分
        x_d = r_d*np.cos(theta_d)
        y_d = r_d*np.sin(theta_d)
        
        #極座標にもどす
        r_hit = np.sqrt((x+x_d)**2+(y+y_d)**2)
        #np.arctan2(a, b):arctan(a/b)
        #戻り値：[-pi, pi]
        theta_hit = np.arctan2(y+y_d, x+x_d)
        if theta_hit < 0 :
            theta_hit += 2*np.pi
        
        return r_hit,theta_hit
    
