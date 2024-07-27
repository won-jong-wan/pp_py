# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 02:19:19 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, TextureStage, Texture
from direct.task import Task
import random

# 설정 파일 데이터 로드
loadPrcFileData("", "win-size 800 600")
loadPrcFileData("", "window-title Panda3D Textured Boxes")

class TexturedBoxes(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 배경색 설정 (밝은 회색)
        self.setBackgroundColor(0.8, 0.8, 0.8, 1)
        
        # 카메라 위치 설정
        self.cam.setPos(10, -10, 8)
        self.cam.lookAt(0, 0, 0)
        
        # 텍스처 생성
        self.textures = self.createTextures()
        
        # 박스 생성
        self.boxes = []
        self.createMultipleBoxes(5)  # 5개의 박스 생성
        
        # 박스 회전 태스크 추가
        self.taskMgr.add(self.spinBoxesTask, "SpinBoxesTask")
    
    def createTextures(self):
        textures = []
        colors = [(173, 216, 230), (255, 182, 193), (144, 238, 144), (255, 255, 224), (221, 160, 221)]
        
        for color in colors:
            tex = Texture()
            tex.setup2dTexture(1, 1, Texture.T_unsigned_byte, Texture.F_rgb)
            tex.setRamImage(bytes(color))
            textures.append(tex)
        
        return textures
    
    def createBox(self, pos, texture):
        # 모델 로드
        box = self.loader.loadModel("models/box")
        box.setPos(pos)
        box.setScale(0.5)  # 크기 조절
        
        # 텍스처 적용
        ts = TextureStage('ts')
        box.setTexture(ts, texture)
        
        box.reparentTo(self.render)
        return box
    
    def createMultipleBoxes(self, num_boxes):
        for i in range(num_boxes):
            pos = (random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(-3, 3))
            texture = random.choice(self.textures)
            box = self.createBox(pos, texture)
            self.boxes.append(box)
    
    def spinBoxesTask(self, task):
        for i, box in enumerate(self.boxes):
            angleDegrees = task.time * (30 + i * 10)  # 각 박스마다 다른 회전 속도
            box.setHpr(angleDegrees, angleDegrees * 0.8, angleDegrees * 0.5)
        return Task.cont

app = TexturedBoxes()
app.run()