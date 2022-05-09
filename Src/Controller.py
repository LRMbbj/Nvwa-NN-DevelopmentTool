from PyQt5.QtWidgets import QInputDialog

import View
import Model
from Components import NNLayerWidget

from NNStructureParts import *

inputLayerName = "inputLayer"
outputLayerName = "outputLayer"
ioLayerNames = [inputLayerName, outputLayerName]


class Controller:
    def __init__(self):
        self.model = Model.Model()
        self.view = View.MainWindow()
        self.ui = self.view.ui
        self.nnView = self.ui.nnView

        self.layerMap = {}

        # 绑定处理函数
        self.SignalInit()

        self.ui.show()

    def SignalInit(self):
        self.ui.createNN.triggered.connect(self.OnCreateNNClicked)
        self.ui.createFullConnectedLayer.clicked.connect(self.OnCreateFullConnectedLayerClicked)
        self.nnView.signalConnectLayer.connect(self.OnConnectLayer)
        self.nnView.signalInsertLayer.connect(self.OnInsertLayer)
        self.nnView.signalDisconnectLayer.connect(self.OnDisconnectLayer)

    def PackLayer(self, layer, widget:NNLayerWidget):
        self.layerMap[layer.GetUUID()] = (layer, widget)
        widget.SetUUID(layer.GetUUID())

    def OnCreateNNClicked(self):
        print("Create NN")

        nnInputNum = 0
        nnOutputNum = 0

        value, ok = QInputDialog.getInt(self.ui, "输入", "输入层节点数", min=1)
        if ok:
            nnInputNum = value

        value, ok = QInputDialog.getInt(self.ui, "输入", "输出层节点数", min=1)
        if ok:
            nnOutputNum = value

        assert nnInputNum != 0 and nnOutputNum != 0, "Network IO layer cannot be empty"

        self.model.CreateNN(nnInputNum, nnOutputNum)

        inputLayerWidget = self.view.DisplayNewLayer("InputLayer", nnInputNum)
        self.PackLayer(self.model.nn.nnInputLayer, inputLayerWidget)

        outputLayerWidget = self.view.DisplayNewLayer("OutputLayer", nnOutputNum)
        self.PackLayer(self.model.nn.nnOutputLayer, outputLayerWidget)

    def OnCreateFullConnectedLayerClicked(self):
        print("Create FC Layer")
        nodeNum = 0

        value, ok = QInputDialog.getInt(self.ui, "输入", "节点数", min=1)
        if ok:
            nodeNum = value

        assert nodeNum > 0

        newlayer = NNFullConnectedLayer(nodeNum)
        newLayerWidget = self.view.DisplayNewLayer("FullConnectedLayer", nodeNum)
        self.PackLayer(newlayer, newLayerWidget)

    def OnConnectLayer(self, inputLayerWidget, outputLayerWidget):
        print("Connect Layer {} -> {}".format(inputLayerWidget, outputLayerWidget))
        # Model动作
        inputLayer = self.layerMap[inputLayerWidget.GetUUID()][0]
        outputLayer = self.layerMap[outputLayerWidget.GetUUID()][0]

        self.model.ConnectLayer(inputLayer, outputLayer)

        # View 动作
        self.view.DisplayNewPipe(inputLayerWidget, outputLayerWidget)

    def OnInsertLayer(self, sourceLayerWidget, destinationLayerWidget, insertLayerWidget):
        print("{}->\\{}/->{}".format(sourceLayerWidget, destinationLayerWidget, insertLayerWidget))
        # Model动作

        sourceLayer = self.layerMap[sourceLayerWidget.GetUUID()][0]
        destinationLayer = self.layerMap[destinationLayerWidget.GetUUID()][0]
        insertLayer = self.layerMap[insertLayerWidget.GetUUID()][0]

        self.model.InsertBetweenLayers(sourceLayer, destinationLayer, insertLayer)

    def OnDisconnectLayer(self, sourceLayerWidget, destinationLayerWidget):
        print("Disconnect Layer {} -X-> {}".format(sourceLayerWidget, destinationLayerWidget))
        # Model动作

        sourceLayer = self.layerMap[sourceLayerWidget.GetUUID()]
        destinationLayer = self.layerMap[destinationLayerWidget.GetUUID()]

        self.model.DisconnectLayer(sourceLayer, destinationLayer)
