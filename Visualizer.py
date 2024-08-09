# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 02:55:47 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, TextNode, Vec4, loadPrcFileData, TransparencyAttrib, ColorBlendAttrib
from panda3d.core import CardMaker, GeomNode, NodePath
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import math

from WorkDq import WorkDq
from GridEditer import GridEditer

loadPrcFileData("", "window-title tmb: edit_view")

class Visualizer(ShowBase):
    def __init__(self, gridEditer:GridEditer()):
        ShowBase.__init__(self)
        
        workDq = WorkDq(gridEditer)
        
        #background
        self.setBackgroundColor(0.8, 0.8, 0.8, 1)
        
        # camera set
        self.cam_distance = 20
        self.cam.setPos(7, -10, 7)
        self.cam.lookAt(Point3(1, 1, 0))
        
        # WorkDq define
        grEd = workDq.gridEditer
        grid = grEd.grid
        
        # extract vals
        x_len = len(grid)
        y_len = len(grid[0])
        
        self.robot_pose = grEd.config_dic["robot_pose"]
        self.home = grEd.config_dic["pick_up_pose"]
        
        order = workDq.str
        
        # object define
        self.goods_list = []
        self.textNodes = []
        
        self.highlight_plate = self.create_plane(0.9, 0.9)
        self.highlight_plate.reparentTo(self.render)
        self.highlight_plate.setColor(1, 0, 0, 0.7)  # 반투명 빨간색
        self.highlight_plate.setPos(0.35, 0.35, 0)  # 바닥에서 살짝 위에
        self.highlight_plate.setHpr(0, 270, 90)
        self.highlight_plate.setTransparency(TransparencyAttrib.MAlpha)
        
        self.ground = self.create_plane(10, 10)
        self.ground.reparentTo(self.render)
        self.ground.setColor(0.5, 0.5, 0.5, 1)
        self.ground.setPos(0.35, 0.35, -0.1)
        self.ground.setHpr(0, 270, 90)
        
        for x in range(x_len):
            for y in range(y_len):
                level_len = len(grid[x][y])
                for level in range(level_len):
                    goods = self.loader.loadModel("models/box")
                    goods.reparentTo(self.render)
                    goods.setScale(0.7)
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
        robot = self.loader.loadModel("models/box")
        robot.reparentTo(self.render)
        robot.setScale(0.7)
        robot.setColor(Vec4(0, 1, 0, 1))
        
        robot.setPos(self.robot_pose[0], self.robot_pose[1], 3)
        
        text = TextNode(f'cube-text-{self.robot_pose}')
        text.setText("robot")
        text.setAlign(TextNode.ACenter)
        
        text.setTextColor(Vec4(1, 1, 1, 1))
        textNP = robot.attachNewNode(text)
        textNP.setScale(1)
        textNP.setPos(0.5, 0.5, 0.5)
        textNP.setBillboardPointEye()
        textNP.setDepthTest(False)
        textNP.setDepthWrite(False)
        
        self.amplitude_text = self.addInstructions(-0.95, f"robot_pose: {self.robot_pose}")
        
        # val define
        
        # event handler define(base on keyboard or mouse)
        
        # taskMgr add(add frame graph callback)
        # base on Task
        
        # 마우스 휠 이벤트 추가
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
    
    # fun for make plane
    def create_plane(self, width, height):
        cm = CardMaker("plane")
        cm.setFrame(-width/2, width/2, -height/2, height/2)
        return NodePath(cm.generate())
    
    # callback def
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(0, 0, 0, 1), pos=(-1.3, pos), align=TextNode.ALeft, scale=.1)
    
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
# if __name__ == "__main__":
#     visualizer = Visualizer(WorkDq())
#     visualizer.run()
    