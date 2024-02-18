#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:28:13 2024

@author: min
"""
import matplotlib.pyplot as plt
import numpy as np
from sort_pts import sort_points_ccw

class interface():
    def __init__(self,x0,y0,x1,y1,f = np.sin):
        self.type ='curve'
        self.tangent = [x1-x0,y1-y0]
        self.start = [x0,y0]
        self.end = [x1,y1]
        self.f=f
        self.center = 0.5*(np.array(self.start)+np.array(self.end))

    def gamma(self,f):
        n2 =self.end[0]-self.start[0]
        n1 = self.start[1] - self.end[1]
        t = np.linspace(0, 1, 1000) 
        q = 0.12*f(2*np.pi*t)
        x = self.start[0] +t*n2+q*n1
        y = self.start[1] -t*n1+q*n2
        return x,y
    def plot_gamma(self):
        self.x,self.y = self.gamma(self.f)
        plt.plot(self.x,self.y,color = "forestgreen",linewidth=3)
        
    def determin_sides(self,x,y):
        return(self.end[0] - self.start[0])*(y - self.start[1]) - (self.end[1] - self.start[1])*(x - self.start[0]) > 0;
    
    def determine_omega(self,box_corners_x,box_corners_y):
        omega1 =[self.start,  self.end]
        omega2 =[self.start,  self.end]
        
        for (x,y) in zip(box_corners_x,box_corners_y):
            pts =[x,y]
            if (self.determin_sides(pts[0],pts[1])):
                omega1.append(pts)
            else:
                omega2.append(pts)
        omega1 = np.array(omega1) 
        omega2 = np.array(omega2)        

        omega1 = sort_points_ccw(omega1, self.start)      
        omega2 = sort_points_ccw(omega2, self.start)  
        gamma_pts = np.transpose(np.concatenate([[self.x],[self.y]]))
        omega1 = self.supplement_omega(omega1,gamma_pts)
        omega2 = self.supplement_omega(omega2,gamma_pts)
        return omega1,omega2

       
    def fill_domain(self,box_corners_x,box_corners_y):
        self.omega1,self.omega2 = self.determine_omega(box_corners_x,box_corners_y)
        plt.fill(self.omega1[:,0], self.omega1[:,1],color = "gold")
        plt.fill(self.omega2[:,0], self.omega2[:,1],color = "lightskyblue")
    def supplement_omega(self,omega,gamma_pts):
        if (np.array_equal(omega[1],self.end)):
            omega = np.insert(omega,1,gamma_pts,axis=0)
        else:
            gamma_pts = np.flip(gamma_pts,axis = 0)
            omega = np.concatenate([omega, gamma_pts])
        return omega
    def mark_domain(self):
        loc_a  = self.center+[0.25,-0.3]
        loc_b  = self.center-[0.35,-0.2]
        if not(self.determin_sides(loc_a[0],loc_a[1])):
            loc = loc_b
            loc_b = loc_a
            loc_a = loc
            
        plt.text(loc_a[0],loc_a[1], r'$\Omega_1$',fontsize=22)
        plt.text(loc_b[0],loc_b[1], r'$\Omega_2$',fontsize=22)
        plt.text(self.center[0]+0.02,self.center[1]-0.05, r'$\Gamma$',fontsize=16)
    def check_crossing(self,x0,x1,y0,y1):
        crossing = False
        for (x_gamma,y_gamma)in zip(self.x,self.y):
            if(x_gamma<=x1 and x_gamma>=x0 and y_gamma<=y1 and y_gamma>=y0):
                crossing = True
                break
            
        return crossing
    


        
       
        
        
class line_interface():
    def __init__(self,x0,y0,x1,y1):
        self.type ='line'
        self.tangent = [x1-x0,y1-y0]
        self.start = [x0,y0]
        self.end = [x1,y1]
    def determin_sides(self,x,y):
        return(self.end[0] - self.start[0])*(y - self.start[1]) - (self.end[1] - self.start[1])*(x - self.start[0]) > 0;
    def plot_gamma(self):
        plt.plot([self.start[0], self.end[0]], [self.start[1], self.end[1]],color = "forestgreen",linewidth=3)
        self.center = 0.5*(np.array(self.start)+np.array(self.end))
        plt.text(self.center[0]+0.02,self.center[1]-0.05, r'$\Gamma$',fontsize=16)
    
    def fill_domain(self,box_corners_x,box_corners_y):
        omega1 =[self.start,  self.end]
        omega2 =[self.start,  self.end]
        
        for (x,y) in zip(box_corners_x,box_corners_y):
            pts =[x,y]
            if (self.determin_sides(pts[0],pts[1])):
                omega1.append(pts)
            else:
                omega2.append(pts)
        omega1 = np.array(omega1) 
        omega2 = np.array(omega2)        

        omega1 = sort_points_ccw(omega1, self.start)      
        omega2 = sort_points_ccw(omega2, self.start)      

        plt.fill(omega1[:,0], omega1[:,1],color = "gold")
        plt.fill(omega2[:,0], omega2[:,1],color = "lightskyblue")
    def mark_domain(self):
        loc_a  = self.center+[0.25,0.2]
        loc_b  = self.center-[0.35,0.2]
        if not(self.determin_sides(loc_a[0],loc_a[1])):
            loc = loc_b
            loc_b = loc_a
            loc_a = loc
            
        plt.text(loc_a[0],loc_a[1], r'$\Omega_1$',fontsize=22)
        plt.text(loc_b[0],loc_b[1], r'$\Omega_2$',fontsize=22)



       