#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:27:33 2024

@author: min
"""
import numpy as np
import math
import matplotlib.pyplot as plt

class Mesh_z():
    def __init__(self, center_z,H,x0=0,x1=1,y0=0,y1=1,if_merge = True):
        self.z = center_z
        self.H = H
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        
        self.nx0 = math.ceil((self.x0-self.z[0])/self.H)
        self.nx1 = math.ceil((self.x1-self.z[0])/self.H)
        self.ny0 = math.ceil((self.y0-self.z[1])/self.H)
        self.ny1 = math.ceil((self.y1-self.z[1])/self.H)
        self.Generate_mesh(if_merge)
        
    def Generate_mesh(self,if_merge):
        x_s = self.z[0]+np.arange(self.nx0,self.nx1)*self.H
        y_s = self.z[1]+np.arange(self.ny0,self.ny1)*self.H
        self.x_s = x_s
        self.y_s = y_s
        self.x_c, self.y_c = np.meshgrid(x_s , y_s)
        if((x_s[0]- self.x0)<0.5*self.H):
            self.x_mesh = x_s + 0.5*self.H
            if(if_merge):
                self.x_mesh  = self.x_mesh[:-1]
        else:
            self.x_mesh = x_s - 0.5*self.H
            if(if_merge):
                self.x_mesh  = self.x_mesh[1:]
        if((y_s[0]- self.y0)<0.5*self.H):
            self.y_mesh = y_s + 0.5*self.H
            if(if_merge):
                self.y_mesh  = self.y_mesh[:-1]

        else:
            self.y_mesh = y_s - 0.5*self.H
            if(if_merge):
                self.y_mesh  = self.y_mesh[1:]
        self.x_mesh_f = np.insert(self.x_mesh,0,self.x0)
        self.x_mesh_f = np.append(self.x_mesh_f,self.x1)
        self.y_mesh_f = np.insert(self.y_mesh,0,self.y0)
        self.y_mesh_f = np.append(self.y_mesh_f,self.y1)
                                  
    def oversample(self,i,j,He,k,color = 'darkorchid',fill=False):
        plt.vlines(self.x_mesh[i]-k*He,self.y_mesh[j]-k*He,self.y_mesh[j+1]+k*He,color = color)
        plt.vlines(self.x_mesh[i+1]+k*He,self.y_mesh[j]-k*He,self.y_mesh[j+1]+k*He,color = color)
        plt.hlines(self.y_mesh[j]-k*He,self.x_mesh[i]-k*He,self.x_mesh[i+1]+k*He,color = color)
        plt.hlines(self.y_mesh[j+1]+k*He,self.x_mesh[i]-k*He,self.x_mesh[i+1]+k*He,color = color)
        center_x  = 0.5*(self.x_mesh[i+1]+self.x_mesh[i])
        center_y  = 0.5*(self.y_mesh[j+1]+self.y_mesh[j])
        if(fill):
            print("fill the block")
            pts_x= [self.x_mesh[i]-k*He, self.x_mesh[i+1]+k*He,self.x_mesh[i+1]+k*He,self.x_mesh[i]-k*He,self.x_mesh[i]-k*He]
            pts_y = [self.y_mesh[j]-k*He, self.y_mesh[j]-k*He, self.y_mesh[j+1]+k*He,self.y_mesh[j+1]+k*He,self.y_mesh[j]-k*He]

            plt.fill(pts_x, pts_y,color = color)
            
        return center_x,center_y
        
    def blocks_cross_gamma(self,gamma_check,k,He,color = 'darkseagreen'):
        n = np.shape(self.x_mesh_f)[0]
        m = np.shape(self.y_mesh_f)[0]
        self.blocks = {}
        self.gamma_blocks = {}
        count =0
        for i in range (n-1):
            for j in range(m-1):
                x0 = self.x_mesh_f[i]-k*He
                x0K = self.x_mesh_f[i]
                if(x0<self.x0):
                    x0 = self.x0
                    
                x1 = self.x_mesh_f[i+1]+k*He
                x1K = self.x_mesh_f[i+1]
                if(x1>self.x1):
                    x1 = self.x1
                y0 = self.y_mesh_f[j]-k*He
                y0K = self.y_mesh_f[j]
                if(y0<self.y0):
                    y0 = self.y0
                y1 = self.y_mesh_f[j+1]+k*He
                y1K = self.y_mesh_f[j+1]
                if(y1>self.y1):
                    y1 = self.y1
                pts_x = [x0,x1,x1,x0]
                pts_y = [y0,y0,y1,y1]
                pts_x_K = [x0K,x1K,x1K,x0K]
                pts_y_K = [y0K,y0K,y1K,y1K]
                self.blocks[count] ={'x':pts_x_K, 'y': pts_y_K, 'x_c':self.x_s[i],'y_c':self.y_s[j] }
                if(gamma_check(x0,x1,y0,y1)):
                    self.gamma_blocks[count] ={'x':pts_x_K, 'y': pts_y_K, 'x_c':self.x_s[i],'y_c':self.y_s[j]}
                    plt.fill(pts_x_K, pts_y_K,color = color)
                count = count +1
        

    def block_side(self,which_side,coarse_blocks):
        for block in self.blocks:
            block_center_x = self.blocks[block]['x_c']
            block_center_y = self.blocks[block]['y_c']
            for c_block in coarse_blocks:
                x_0 = coarse_blocks[c_block]['x'][0]
                x_1 = coarse_blocks[c_block]['x'][1]
                y_0 = coarse_blocks[c_block]['y'][0]
                y_1 = coarse_blocks[c_block]['y'][2]
                if(block_center_x<x_1 and block_center_x>x_0 and block_center_y>y_0 and block_center_y<y_1):
                    plt.plot(block_center_x,block_center_y,marker = '.',color = 'green',linewidth = 0.3)
                    break
                
        for block in self.gamma_blocks:
            block_center_x = self.gamma_blocks[block]['x_c']
            block_center_y = self.gamma_blocks[block]['y_c']

            if which_side(block_center_x,block_center_y):
                plt.fill(self.gamma_blocks[block]['x'], self.gamma_blocks[block]['y'],color = 'cornsilk')
                plt.plot(block_center_x,block_center_y,marker = '.',color = 'orange',linewidth = 0.3)

            else:
                plt.fill(self.gamma_blocks[block]['x'], self.gamma_blocks[block]['y'],color = 'lightblue')
                plt.plot(block_center_x,block_center_y,marker = '.',color = 'blue',linewidth = 0.3)
                
        
            
                
                    
                    
            
        
    
   
        
        