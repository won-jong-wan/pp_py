# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 02:10:41 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec4
from direct.task import Task
from panda3d.core import CardMaker

# 설정 파일 데이터 로드
loadPrcFileData("", "win-size 800 600")
loadPrcFileData("", "window-title Panda3D Simple Colored Cube")

class SimpleCube(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 배경색 설정 (밝은 회색)
        self.setBackgroundColor(0.8, 0.8, 0.8, 1)
        
        # 카메라 위치 설정
        self.cam.setPos(5, -5, 3)
        self.cam.lookAt(0, 0, 0)
        
        # 큐브 생성
        cm = CardMaker('card')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        
        # 큐브의 6면 생성
        cube = self.render.attachNewNode("Cube")
        for i in range(6):
            card = cube.attachNewNode(cm.generate())
            if i == 0:
                card.setPos(0, 0.5, 0)
            elif i == 1:
                card.setPos(0, -0.5, 0)
                card.setH(180)
            elif i == 2:
                card.setPos(0.5, 0, 0)
                card.setH(90)
            elif i == 3:
                card.setPos(-0.5, 0, 0)
                card.setH(-90)
            elif i == 4:
                card.setPos(0, 0, 0.5)
                card.setP(-90)
            else:
                card.setPos(0, 0, -0.5)
                card.setP(90)
            
            # 각 면에 단색 설정 (파스텔 블루)
            card.setColor(Vec4(0.68, 0.85, 0.9, 1))
        
        # 큐브 회전 태스크 추가
        self.taskMgr.add(self.spinCubeTask, "SpinCubeTask")
    
    def spinCubeTask(self, task):
        angleDegrees = task.time * 60.0
        self.render.find("Cube").setHpr(angleDegrees, angleDegrees, 0)
        return Task.cont

app = SimpleCube()
app.run()