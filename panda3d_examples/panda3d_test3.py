# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 01:01:34 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, TextNode, Vec4, CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerQueue
from panda3d.core import Vec3, CollisionRay  # 추가된 import
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import math

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cam_distance = 20
        self.cam_pitch = 45
        self.cam_yaw = 0
        self.updateCameraPosition()
        
        self.cubes = []
        self.textNodes = []
        for i in range(9):
            cube = self.loader.loadModel("models/box")
            cube.reparentTo(self.render)
            cube.setScale(0.5)
            cube.setColor(0.2, 0.3, 0.8, 1)  # 파란색 큐브
            cube.setTag('cube_id', str(i))
            
            # 충돌 감지를 위한 CollisionNode 추가
            collider = cube.attachNewNode(CollisionNode(f'cubeCollider{i}'))
            collider.node().addSolid(CollisionSphere(0, 0, 0, 0.5))
            
            text = TextNode(f'cube-text-{i}')
            text.setText(str(i+1))
            text.setAlign(TextNode.ACenter)
            text.setTextColor(Vec4(1, 1, 1, 1))  # 흰색 텍스트
            textNP = cube.attachNewNode(text)
            textNP.setScale(0.3)
            textNP.setPos(0, 0, 0)
            textNP.setBillboardPointEye()
            textNP.setDepthTest(False)
            textNP.setDepthWrite(False)
            
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
        self.addInstructions(0.65, "Click and Drag: Rotate camera")
        self.addInstructions(0.55, "Click on cube: Move cube")
        
        self.accept("arrow_up", self.increaseAmplitude)
        self.accept("arrow_down", self.decreaseAmplitude)
        self.accept("arrow_left", self.decreaseSpeed)
        self.accept("arrow_right", self.increaseSpeed)
        
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        
        self.disableMouse()  # 기본 마우스 컨트롤 비활성화
        self.mouseControlTask = taskMgr.add(self.mouseControlTask, "MouseControlTask")
        
        # 충돌 감지 설정
        self.picker = CollisionTraverser()
        self.pq = CollisionHandlerQueue()
        pickerNode = CollisionNode('mouseRay')
        pickerNP = self.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(1)
        self.pickerRay = pickerNode.addSolid(CollisionSphere(0, 0, 0, 1))
        self.picker.addCollider(pickerNP, self.pq)
        
        self.selected_cube = None
        self.accept('mouse1', self.selectCube)
        self.accept('mouse1-up', self.deselectCube)
        
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
        rad_pitch = math.radians(self.cam_pitch)
        rad_yaw = math.radians(self.cam_yaw)
        x = self.cam_distance * math.sin(rad_yaw) * math.cos(rad_pitch)
        y = -self.cam_distance * math.cos(rad_yaw) * math.cos(rad_pitch)
        z = self.cam_distance * math.sin(rad_pitch)
        self.cam.setPos(x, y, z)
        self.cam.lookAt(Point3(0, 0, 0))
        
    def mouseControlTask(self, task):
        if self.mouseWatcherNode.hasMouse():
            x, y = self.mouseWatcherNode.getMouse()
            if self.mouseWatcherNode.isButtonDown(1) and not self.selected_cube:  # 좌클릭 & 큐브 미선택
                self.cam_yaw -= x * 50  # 감도 조절
                self.cam_pitch += y * 50
                self.cam_pitch = min(max(self.cam_pitch, -90), 90)
                self.updateCameraPosition()
            elif self.selected_cube:
                # 선택된 큐브를 마우스 위치로 이동
                nearPoint = Point3()
                farPoint = Point3()
                self.camLens.extrude(x, y, nearPoint, farPoint)
                plane_point = Point3(0, 0, self.selected_cube.getZ())
                plane_normal = Vec3(0, 0, 1)
                t = (plane_point - nearPoint).dot(plane_normal) / (farPoint - nearPoint).dot(plane_normal)
                hitPos = nearPoint + (farPoint - nearPoint) * t
                self.selected_cube.setPos(hitPos.x, hitPos.y, self.selected_cube.getZ())
        return Task.cont
        
    def selectCube(self):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(self.camNode, mpos.x, mpos.y)
            self.picker.traverse(self.render)
            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('cube_id')
                if not pickedObj.isEmpty():
                    self.selected_cube = pickedObj
                    self.selected_cube.setColorScale(1, 1, 0, 1)  # 선택된 큐브를 노란색으로 변경
    
    def deselectCube(self):
        if self.selected_cube:
            self.selected_cube.setColorScale(1, 1, 1, 1)  # 원래 색상으로 복귀
            self.selected_cube = None
        
    def animateCubes(self, task):
        time = task.time
        for i, cube in enumerate(self.cubes):
            if cube != self.selected_cube:  # 선택되지 않은 큐브만 애니메이션
                offset_time = time - (i * self.cube_spacing / self.movement_speed)
                if offset_time < 0:
                    continue
                
                x = i * 1.5 - 6
                y = 0
                z = math.sin(offset_time * self.movement_speed) * self.vertical_amplitude
                
                cube.setPos(x, y, z)
        
        return Task.cont

app = MyApp()
app.run()