# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 00:34:38 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, TextNode, Vec4, ColorAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import math

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cam.setPos(0, -20, 10)
        self.cam.lookAt(Point3(0, 0, 0))
        
        self.cubes = []
        self.textNodes = []
        for i in range(9):
            cube = self.loader.loadModel("models/box")
            cube.reparentTo(self.render)
            cube.setScale(0.5)
            
            # 큐브 색상 설정 (예: 파란색)
            cube.setColor(0.2, 0.3, 0.8, 1)
            
            # 큐브에 번호 추가
            text = TextNode(f'cube-text-{i}')
            text.setText(str(i+1))
            text.setAlign(TextNode.ACenter)
            text.setTextColor(Vec4(1, 1, 1, 1))  # 흰색 텍스트
            textNP = cube.attachNewNode(text)
            textNP.setScale(1)  # 텍스트 크기 조정
            textNP.setPos(0.5, 0.5, 0.3)  # 큐브 중앙에 위치
            textNP.setBillboardPointEye()  # 텍스트가 항상 카메라를 향하도록 설정
            textNP.setDepthTest(False)  # 텍스트가 항상 큐브 앞에 보이도록 설정
            textNP.setDepthWrite(False)
            
            self.cubes.append(cube)
            self.textNodes.append(textNP)
        
        self.rotation_speed = 60
        self.vertical_amplitude = 2
        
        self.speed_text = self.addInstructions(-0.95, f"Rotation Speed: {self.rotation_speed}")
        self.amplitude_text = self.addInstructions(-0.85, f"Vertical Amplitude: {self.vertical_amplitude}")
        self.addInstructions(0.95, "Up/Down: Change rotation speed")
        self.addInstructions(0.85, "Left/Right: Change vertical amplitude")
        
        self.accept("arrow_up", self.increaseSpeed)
        self.accept("arrow_down", self.decreaseSpeed)
        self.accept("arrow_left", self.decreaseAmplitude)
        self.accept("arrow_right", self.increaseAmplitude)
        
        self.taskMgr.add(self.animateCubes, "AnimateCubes")
        
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)
        
    def increaseSpeed(self):
        self.rotation_speed += 10
        self.speed_text.setText(f"Rotation Speed: {self.rotation_speed}")
        
    def decreaseSpeed(self):
        self.rotation_speed = max(10, self.rotation_speed - 10)
        self.speed_text.setText(f"Rotation Speed: {self.rotation_speed}")
        
    def increaseAmplitude(self):
        self.vertical_amplitude += 0.5
        self.amplitude_text.setText(f"Vertical Amplitude: {self.vertical_amplitude:.1f}")
        
    def decreaseAmplitude(self):
        self.vertical_amplitude = max(0.5, self.vertical_amplitude - 0.5)
        self.amplitude_text.setText(f"Vertical Amplitude: {self.vertical_amplitude:.1f}")
        
    def animateCubes(self, task):
        time = task.time
        for i, cube in enumerate(self.cubes):
            angle = (i / 9.0 * 360 + time * self.rotation_speed) % 360
            x = 3 * math.cos(math.radians(angle))
            y = 3 * math.sin(math.radians(angle))
            
            z = math.sin(time * 2 + i * 0.5) * self.vertical_amplitude
            
            cube.setPos(x, y, z)
            cube.setHpr(angle, 0, 0)
        
        return Task.cont

app = MyApp()
app.run()