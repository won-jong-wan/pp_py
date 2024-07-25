# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 00:43:50 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, TextNode, Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import math

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cam_distance = 20
        self.cam.setPos(0, -20, 10)
        self.cam.lookAt(Point3(0, 0, 0))
        
        self.cubes = []
        self.textNodes = []
        for i in range(9):
            cube = self.loader.loadModel("models/box")
            cube.reparentTo(self.render)
            cube.setScale(0.5)
            cube.setColor(0.2, 0.3, 0.8, 1)  # 파란색 큐브
            
            x = i * 1.5 - 6  # 큐브를 x축을 따라 일렬로 배치
            y = 0
            z = 0
            
            cube.setPos(x, y, z)
            
            text = TextNode(f'cube-text-{i}')
            text.setText(str(i+1))
            text.setAlign(TextNode.ACenter)
            text.setTextColor(Vec4(1, 1, 1, 1))  # 흰색 텍스트
            textNP = cube.attachNewNode(text)
            textNP.setScale(1)
            textNP.setPos(0.5, 0.5, 0.5)
            textNP.setBillboardPointEye()
            textNP.setDepthTest(False)
            # textNP.setDepthWrite(False)
            
            self.cubes.append(cube)
            self.textNodes.append(textNP)
        
        self.vertical_amplitude = 2
        self.movement_speed = 1
        self.cube_spacing = 1  # 큐브 간 간격
        
        self.amplitude_text = self.addInstructions(-0.95, f"Vertical Amplitude: {self.vertical_amplitude}")
        self.speed_text = self.addInstructions(-0.85, f"Movement Speed: {self.movement_speed}")
        self.addInstructions(0.95, "Up/Down: Change vertical amplitude")
        self.addInstructions(0.85, "Left/Right: Change movement speed")
        self.addInstructions(0.75, "Mouse Wheel: Zoom in/out")
        
        self.accept("arrow_up", self.increaseAmplitude)
        self.accept("arrow_down", self.decreaseAmplitude)
        self.accept("arrow_left", self.decreaseSpeed)
        self.accept("arrow_right", self.increaseSpeed)
        
        # 마우스 휠 이벤트 추가
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        
        self.taskMgr.add(self.animateCubes, "AnimateCubes")
        
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)
        
    def increaseAmplitude(self):
        self.vertical_amplitude += 0.5
        self.amplitude_text.setText(f"Vertical Amplitude: {self.vertical_amplitude:.1f}")
        
    def decreaseAmplitude(self):
        self.vertical_amplitude = max(0.5, self.vertical_amplitude - 0.5)
        self.amplitude_text.setText(f"Vertical Amplitude: {self.vertical_amplitude:.1f}")
        
    def increaseSpeed(self):
        self.movement_speed += 0.1
        self.speed_text.setText(f"Movement Speed: {self.movement_speed:.1f}")
        
    def decreaseSpeed(self):
        self.movement_speed = max(0.1, self.movement_speed - 0.1)
        self.speed_text.setText(f"Movement Speed: {self.movement_speed:.1f}")
        
    def zoom_in(self):
        self.cam_distance = max(5, self.cam_distance - 1)
        self.updateCameraPosition()
        
    def zoom_out(self):
        self.cam_distance = min(40, self.cam_distance + 1)
        self.updateCameraPosition()
        
    def updateCameraPosition(self):
        self.cam.setPos(0, -self.cam_distance, self.cam_distance * 0.5)
        self.cam.lookAt(Point3(0, 0, 0))
        
    def animateCubes(self, task):
        time = task.time
        for i, cube in enumerate(self.cubes):
            # 각 큐브의 시작 시간을 지연
            offset_time = time - (i * self.cube_spacing / self.movement_speed)
            if offset_time < 0:
                continue  # 아직 시작하지 않은 큐브는 움직이지 않음
            
            x = i * 1.5 - 6  # 큐브를 x축을 따라 일렬로 배치
            y = 0
            z = math.sin(offset_time * self.movement_speed) * self.vertical_amplitude
            
            cube.setPos(x, y, z)
        
        return Task.cont

app = MyApp()
app.run()