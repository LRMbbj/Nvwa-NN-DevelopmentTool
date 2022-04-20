from PyQt5.QtWidgets import QInputDialog

import View
import Components
import Model


inputLayerName = "inputLayer"
outputLayerName = "outputLayer"
ioLayerNames = [inputLayerName, outputLayerName]


class Controller:
    def __init__(self):
        self.model = Model.Model()
        self.view = View.MainWindow()
        self.ui = self.view.ui

        # 绑定处理函数
        self.ui.createNN.triggered.connect(self.OnCreateNNClicked)
        self.ui.createFullConnectedLayer.clicked.connect(self.OnCreateFullConnectedLayerClicked)

        self.ui.show()

    def OnCreateNNClicked(self):
        print("Press createNN")

        nnInputNum = 0
        nnOutputNum = 0

        value, ok = QInputDialog.getInt(self.view, "输入", "输入层节点数", min=1)
        if ok:
            nnInputNum = value

        value, ok = QInputDialog.getInt(self.view, "输入", "输出层节点数", min=1)
        if ok:
            nnOutputNum = value

        assert nnInputNum != 0 and nnOutputNum != 0, "Network IO layer cannot be empty"

        self.model.CreateNN(nnInputNum, nnOutputNum)

        inputLayerWidget = self.view.DisplayNewLayer("InputLayer", nnInputNum)

        outputLayerWidget = self.view.DisplayNewLayer("OutputLayer", nnOutputNum)

    def OnCreateFullConnectedLayerClicked(self):
        layerInputObject = None
        layerOutputObject = None
        nodeNum = 0

        layerItems = self.model.nn.layers

        value, ok = QInputDialog.getItem(self.view, "输入", "输入层对象", [str(x) for x in layerItems] + [inputLayerName])
        if ok:
            layerInputObject = (value, self.model)[value not in ioLayerNames]

        value, ok = QInputDialog.getItem(self.view, "输入", "输出层对象", [str(x) for x in layerItems] + [outputLayerName])
        if ok:
            layerOutputObject = (value, self.model)[value not in ioLayerNames]

        value, ok = QInputDialog.getInt(self.view, "输入", "节点数", min=1)
        if ok:
            nodeNum = value

        assert layerInputObject is not None and layerOutputObject is not None and nodeNum > 0
        "Layer IO layer cannot be empty"

        # model处理
        self.model.CreateFullConnectedLayer(nodeNum, layerInputObject, layerOutputObject)

        # view处理
        fullConnectedLayerWidget = self.view.DisplayNewLayer("FullConnectedLayer")
        fullConnectedLayerWidget.SetInputLayer(layerInputObject)
        fullConnectedLayerWidget.SetOutputLayer(layerOutputObject)
        fullConnectedLayerWidget.SetNodeNum(nodeNum)
