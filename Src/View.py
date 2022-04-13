from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow

import Components

uiPath = "Resources/UI/MainWindow.ui"

layerTypes = {
    "InputLayer": (Components.InputLayerWidget, QSize(150, 50)),
    "OutputLayer": (Components.OutputLayerWidgt, QSize(150, 50)),
    "FullConnectedLayer": (Components.FullConnectedLayerWidget, QSize(250, 50))
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(uiPath)

        self.nnContainer = self.ui.nnContainer
        self.propertyContainer = self.ui.propertyBar

        self.layers = []
        self.connections = []

    def DisplayNewLayer(self, layerType):
        layerInstance = layerTypes[layerType][0](self.nnContainer, layerTypes[layerType][1])

        layerInstance.move(300, self.layers.__len__()*350)
        layerInstance.show()

        self.layers.append(layerInstance)
        return layerInstance
