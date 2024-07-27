# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 22:58:11 2024

@author: jonwo
"""
from direct.showbase.ShowBase import ShowBase

class Visualizer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        
        self.robot = self.loader.loadModel("robot.egg")
        
        self.robot.reparentTo(self.render)
        
        self.robot.setScale(10, 10, 10)
        
visualizer = Visualizer()
visualizer.run()