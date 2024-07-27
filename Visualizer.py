# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 02:55:47 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, TextNode, Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import math

from WorkDq import WorkDq
from GridEditer import GridEditer

class Visualizer(ShowBase):
    def __init__(self, workDq:WorkDq):
        ShowBase.__init__(self)
        
        #background
        self.setBackgroundColor(0.8, 0.8, 0.8, 1)
        
        # camera set
        self.cam_distance = 20
        self.cam.setPos(7, -7, 7)
        self.cam.lookAt(Point3(1, 1, 0))
        
        # WorkDq define
        grEd = workDq.gridEditer
        grid = grEd.grid
        
        x_len = len(grid)
        y_len = len(grid[0])
        
        order = workDq.str
        
        # object define
        self.goods_list = []
        self.textNodes = []
        
        self.base = (0, 0, 0)
        
        for x in range(x_len):
            for y in range(y_len):
                level_len = len(grid[x][y])
                for level in range(level_len):
                    goods = self.loader.loadModel("models/box")
                    goods.reparentTo(self.render)
                    goods.setScale(0.5)
                    goods.setColor(Vec4(0.5*level, 0.5*level, 0.5*level, 0.5*level))  # 파란색 큐브
                    
                    goods.setPos(x, y, level)
                    
                    text = TextNode(f'cube-text-{(x,y,level)}')
                    text.setText(grid[x][y][level][0])
                    text.setAlign(TextNode.ACenter)
                    text.setTextColor(Vec4(1, 1, 1, 1))  # 흰색 텍스트
                    textNP = goods.attachNewNode(text)
                    textNP.setScale(1)
                    textNP.setPos(0.5, 0.5, 0.5)
                    textNP.setBillboardPointEye()
                    textNP.setDepthTest(False)
                    textNP.setDepthWrite(False)
                    
                    self.goods_list.append(goods)
                    self.textNodes.append(textNP)
        
        
        
        # robot define
        ## find how to import solidworks model
        
        # val define
        
        # event handler define(base on keyboard or mouse)
        
        # taskMgr add(add frame graph callback)
        # base on Task
        
        # 마우스 휠 이벤트 추가
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        
    # callback def
    def zoom_in(self):
        self.cam_distance = max(5, self.cam_distance - 1)
        self.updateCameraPosition()
        
    def zoom_out(self):
        self.cam_distance = min(40, self.cam_distance + 1)
        self.updateCameraPosition()
        
    def updateCameraPosition(self):
        self.cam.setPos(0, -self.cam_distance, self.cam_distance * 0.5)
        self.cam.lookAt(Point3(0, 0, 0))
    
    # fun for get str
    
    # fun for analyze str_order to object's movement
    
    # object's movement to 
if __name__ == "__main__":
    visualizer = Visualizer(WorkDq())
    visualizer.run()
    