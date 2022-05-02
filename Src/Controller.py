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
        self.nnView = self.ui.nnView

        # 绑定处理函数
        self.SignalInit()

        self.ui.show()

    def SignalInit(self):
        self.ui.createNN.triggered.connect(self.OnCreateNNClicked)
        self.ui.createFullConnectedLayer.clicked.connect(self.OnCreateFullConnectedLayerClicked)
        self.nnView.signalConnectLayer.connect(self.OnConnectLayer)
        self.nnView.signalInsertLayer.connect(self.OnInsertLayer)
        self.nnView.signalDisconnectLayer.connect(self.OnDisconnectLayer)

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

        outputLayerWidget = self.view.DisplayNewLayer("OutputLayer", nnOutputNum)

    def OnCreateFullConnectedLayerClicked(self):
        print("Create FC Layer")
        nodeNum = 0

        layerItems = self.model.nn.layers

        value, ok = QInputDialog.getInt(self.ui, "输入", "节点数", min=1)
        if ok:
            nodeNum = value

        assert nodeNum > 0

        fullConnectedLayerWidget = self.view.DisplayNewLayer("FullConnectedLayer", nodeNum)

    def OnConnectLayer(self, inputLayer, outputLayer):
        print("Connect Layer {} -> {}".format(inputLayer, outputLayer))

    def OnInsertLayer(self, sourceLayer, destinationLayer, insertLayer):
        print("{}->\\{}/->{}".format(sourceLayer, destinationLayer, insertLayer))

    def OnDisconnectLayer(self, sourceLayer, destinationLayer):
        print("Disconnect Layer {} -X-> {}".format(sourceLayer, destinationLayer))
