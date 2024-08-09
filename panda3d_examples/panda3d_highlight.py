# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 04:20:48 2024

@author: admin
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, loadPrcFileData, TransparencyAttrib, ColorBlendAttrib
from panda3d.core import CardMaker, GeomNode, NodePath
from panda3d.core import GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, Geom
from direct.task import Task
import math

loadPrcFileData("", "win-size 800 600")
loadPrcFileData("", "window-title Panda3D: 위치 강조 예제 (판과 빛 기둥)")

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cam.setPos(0, -20, 10)
        self.cam.lookAt(0, 0, 0)
        
        # 바닥 평면 생성
        self.ground = self.create_plane(10, 10)
        self.ground.reparentTo(self.render)
        self.ground.setColor(0.5, 0.5, 0.5, 1)
        
        # 얇은 판으로 위치 강조
        self.highlight_plate = self.create_plane(1, 1)
        self.highlight_plate.reparentTo(self.render)
        self.highlight_plate.setColor(1, 0, 0, 0.7)  # 반투명 빨간색
        self.highlight_plate.setPos(2, 2, 0.01)  # 바닥에서 살짝 위에
        self.highlight_plate.setTransparency(TransparencyAttrib.MAlpha)
        
        # 투명한 빛의 기둥 생성
        self.light_column = self.create_cylinder(0.2, 5, 16)
        self.light_column.reparentTo(self.render)
        self.light_column.setColor(0, 1, 1, 0.3)  # 반투명 시안색
        self.light_column.setPos(-2, -2, 2.5)  # 중심이 지면에서 2.5 유닛 위에
        self.light_column.setTransparency(TransparencyAttrib.MAlpha)
        self.light_column.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))  # 가산 블렌딩
        
        # 판과 기둥을 움직이는 태스크 추가
        self.taskMgr.add(self.moveHighlights, "MoveHighlightsTask")

    def create_plane(self, width, height):
        cm = CardMaker("plane")
        cm.setFrame(-width/2, width/2, -height/2, height/2)
        return NodePath(cm.generate())

    def create_cylinder(self, radius, height, segments):
        vdata = GeomVertexData("cylinder", GeomVertexFormat.getV3n3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")

        # 원기둥의 옆면 생성
        for i in range(segments + 1):
            angle = i * 2 * math.pi / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            
            vertex.addData3(x, y, 0)
            vertex.addData3(x, y, height)
            normal.addData3(x, y, 0)
            normal.addData3(x, y, 0)
            color.addData4(1, 1, 1, 1)
            color.addData4(1, 1, 1, 1)

        prim = GeomTriangles(Geom.UHStatic)
        for i in range(segments):
            prim.addVertices(i*2, i*2+1, (i*2+2) % (segments*2))
            prim.addVertices(i*2+1, (i*2+3) % (segments*2), (i*2+2) % (segments*2))

        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode("cylinder")
        node.addGeom(geom)
        return NodePath(node)
        
    def moveHighlights(self, task):
        time = self.taskMgr.globalClock.getFrameTime()
        
        # 판을 위아래로 움직임
        z = 0.01 + 0.1 * abs(math.sin(time))
        self.highlight_plate.setZ(z)
        
        # 기둥을 회전시킴
        self.light_column.setH(time * 30)  # 초당 30도 회전
        
        return Task.cont

app = MyApp()
app.run()