from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton

import Components

uiPath = "Resources/UI/MainWindow.ui"

LayerType = {
    "InputLayer": Components.InputLayerWidget,
    "OutputLayer": Components.OutputLayerWidgt,
    "FullConnectedLayer": Components.FullConnectedLayerWidget
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
        layerInstance = LayerType[layerType](self.nnContainer)

        layerInstance.setParent(self.nnContainer)
        layerInstance.move(300, self.layers.__len__()*350)
        layerInstance.show()

        self.layers.append(layerInstance)
        return layerInstance
