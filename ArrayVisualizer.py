#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:20:08 2024

@author: won
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class ArrayVisualizer(QWidget):
    def __init__(self, grid):
        super().__init__()
        self.array = np.array(grid)  # 일반 리스트를 numpy 배열로 변환
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        tab_widget = QTabWidget()

        for d in range(self.array.shape[0]):
            tab = QWidget()
            grid_layout = QGridLayout()

            for h in range(self.array.shape[1]):
                for w in range(self.array.shape[2]):
                    value = self.array[d, h, w]
                    label = QLabel(f"{value[0]}\n{value[1]}")
                    label.setStyleSheet("border: 1px solid black; padding: 10px;")
                    label.setAlignment(Qt.AlignCenter)
                    grid_layout.addWidget(label, h, w)

            tab.setLayout(grid_layout)
            tab_widget.addTab(tab, f"Depth {d}")

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        self.setWindowTitle('3D Array Visualizer')
        self.setGeometry(300, 300, 400, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 예시 데이터
    grid = [[
        [("load1", 1), ("load2", 2), ("load3", 3)],
        [("load4", 4), ("load5", 5), ("load6", 6)]
    ] for _ in range(3)]  # 3개의 깊이 레벨을 가정
    
    ex = ArrayVisualizer(grid)
    sys.exit(app.exec_())