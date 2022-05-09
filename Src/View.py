from PyQt5 import uic
from PyQt5.QtCore import QSize, QSizeF, QPoint
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene

import Components

uiPath = "Resources/UI/MainWindow.ui"

layerTypes = {
    "InputLayer": (Components.InputLayerWidget, QSizeF(150, 50)),
    "OutputLayer": (Components.OutputLayerWidgt, QSizeF(150, 50)),
    "FullConnectedLayer": (Components.FullConnectedLayerWidget, QSizeF(250, 50))
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(uiPath)

        self.ui.nnView = Components.NNGraphicsView(self.ui.centralwidget)
        self.ui.nnView.setObjectName(u"nnView")
        self.ui.nnView.setMinimumSize(500, 800)
        self.ui.horizontalLayout.addWidget(self.ui.nnView)
        self.nnView = self.ui.nnView

        self.propertyContainer = self.ui.propertyBar
        self.ui.horizontalLayout.addWidget(self.propertyContainer)

        self.layers = []
        self.pipes = []

    def DisplayNewLayer(self, layerType, nodeNum):
        newLayer = layerTypes[layerType][0](layerTypes[layerType][1])
        self.nnView.DisplayNewLayer(QPoint(0, 0), newLayer)
        newLayer.SetNodeNum(nodeNum)
        self.layers.append(newLayer)
        return newLayer

    def DisplayNewPipe(self, obj1, obj2):
        newEdge = Components.NNPipe(self.nnView.scene, obj1, obj2)
        newEdge.Store()
