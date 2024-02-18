#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 23:02:54 2024

@author: min
"""
import math 
import numpy as np
def distance_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def angle_with_reference(p, reference_point):
    dx = p[0] - reference_point[0]
    dy = p[1] - reference_point[1]
    return math.atan2(dy, dx)

def sort_points_ccw(points, reference_point):
    return np.array(sorted(points, key=lambda p: angle_with_reference(p, reference_point)))