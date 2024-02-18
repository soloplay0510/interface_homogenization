#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:58:05 2024

@author: min
"""

# from fenics import *
import matplotlib.pyplot as plt
import math 
import numpy as np
import sys
# sys.path.append(".")
from mesh import *
from interface import *
    


   
      
        
if __name__ == '__main__': 
   center_z = [0.33,0.57]
   x0=0
   x1=1
   y0=0
   y1=1
   H_ep =0.05
   H =0.25
   print("Plotting a UnitSquareMesh")
   fig = plt.figure()
   ax = fig.add_axes((x0, y0, x1-x0, y1-y0))
   ax.axis('equal')
   # ax.set_xlim([0, 1])
   # ax.set_ylim([0, 1])

   # plt.vlines(center_z[0], y0, y1)
   #plot H_{\epsilon}

   mesh_e = Mesh_z(center_z, H_ep)
   plt.vlines(mesh_e.x_mesh, y0, y1,color = 'lightgrey')
   plt.hlines(mesh_e.y_mesh, x0, x1,color = 'lightgrey')
   
   
   #plot H mesh
   
   mesh = Mesh_z(center_z, H)
   plt.vlines(mesh.x_mesh, y0, y1,color = 'grey')
   plt.hlines(mesh.y_mesh, x0, x1,color = 'grey')
   # center_x,center_y = mesh.oversample(0,1,H_ep,2)
   # plt.text(center_x-0.1,center_y-0.07, r'$K_H^+(x)$',fontsize=16)

   #plot centers
   # plt.plot(mesh.x_c,mesh.y_c,'o',color = 'blue')
   #plot Omega
   plt.vlines(x0, y0, y1,color = 'black')
   plt.vlines(x1, y0, y1,color = 'black')
   plt.hlines(y0, x0, x1,color = 'black')
   plt.hlines(y1, x0, x1,color = 'black')
   #plot center of the mesh

   # plt.plot(center_z[0],center_z[1],'o',color = 'red')
   # plt.text(center_z[0]+0.003,center_z[1]+0.015, r'$x$',fontsize=12)
   
   domain_x,domain_y = np.meshgrid([x0,x1] , [y0,y1])
   domain_x = np.reshape(domain_x,[-1])
   domain_y = np.reshape(domain_y,[-1])

   # Straight line gamma
   # gamma = line_interface(0.28,0.0,0.77,0.99)
   # gamma.plot_gamma()

   # gamma.fill_domain(domain_x,domain_y)
   # gamma.mark_domain()
   
   sin_gamma = interface(0.28,0.0,0.77,0.99)
   sin_gamma.plot_gamma()
   sin_gamma.fill_domain(domain_x,domain_y)
   
   
   mesh.blocks_cross_gamma(sin_gamma.check_crossing,0,H_ep)
   # sin_gamma.mark_domain()
   # fig.tight_layout()
   # plt.legend(frameon=False)
   # plt.close()
   # center_x,center_y  = mesh_e.oversample(4,11,H_ep,0,color = 'orchid',fill = True)            
   # plt.text(center_x-0.035,center_y+0.03, r'$\omega (K)$',fontsize=10)
   ax.set_axis_off()
   plt.savefig('omega_gamma_0.png',bbox_inches='tight',transparent = True, dpi=300)