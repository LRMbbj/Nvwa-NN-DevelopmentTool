import NNStructureParts


class Model:
    def __init__(self):
        self.nn = None

    def CreateNN(self, inputNum, OutputNum):
        self.nn = NNStructureParts.NNModel(inputNum, OutputNum)

    def CreateFullConnectedLayer(self, nodeNum, layerInputObject, layerOutputObject):
        # TODO 修改为类型判断
        layer = NNStructureParts.NNFullConnectedLayer(nodeNum, layerInputObject, layerOutputObject)
        self.nn.AppendLayer(layer)
