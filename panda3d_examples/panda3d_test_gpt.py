# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 02:10:19 2024

@author: jonwo
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import LPoint3
import math

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 팬더 모델을 로드하고 렌더 노드에 추가합니다.
        self.panda_model = self.loader.loadModel("models/panda-model")
        self.panda_model.reparentTo(self.render)
        self.panda_model.setScale(0.005)
        self.panda_model.setPos(0, 10, 0)

        # 두 개의 태스크를 추가합니다.
        self.taskMgr.add(self.rotate_camera_task, "RotateCameraTask")
        self.taskMgr.add(self.move_panda_task, "MovePandaTask")

    def rotate_camera_task(self, task):
        # 경과 시간을 사용하여 카메라를 회전시킵니다.
        angle_degrees = task.time * 10.0
        angle_radians = angle_degrees * (math.pi / 180.0)
        self.camera.setPos(20 * math.sin(angle_radians), -20 * math.cos(angle_radians), 3)
        self.camera.lookAt(0, 0, 0)
        
        # 태스크가 계속 실행되도록 Task.cont를 반환합니다.
        return Task.cont

    def move_panda_task(self, task):
        # 경과 시간을 사용하여 모델의 위치를 변경합니다.
        z = 1.0 + 0.5 * math.sin(task.time * 2.0)
        self.panda_model.setPos(0, 10, z)
        
        # 태스크가 계속 실행되도록 Task.cont를 반환합니다.
        return Task.cont

if __name__ == "__main__":
    app = MyApp()
    app.run()
