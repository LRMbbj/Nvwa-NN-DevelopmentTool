import re
from enum import Enum


class ActivationFuncs(Enum):
    NoFunc = 0
    ReLU = 1
    LeakyReLU = 2
    Sigmoid = 3
    Tanh = 4


FUNCNAMES = {
    ActivationFuncs.ReLU: "ReLU",
    ActivationFuncs.LeakyReLU: "LeakyReLU",
    ActivationFuncs.Sigmoid: "Sigmoid",
    ActivationFuncs.Tanh: "Tanh"
}


class NNLayer:
    def __init__(self, inputObject=None, outputObject=None):
        self.inputObject = inputObject
        self.outputObject = outputObject

    def SetInputObject(self, obj):
        self.inputObject = obj

    def GetInputObject(self):
        return self.inputObject

    def SetOutputObject(self, obj):
        self.outputObject = obj

    def GetOutputObject(self):
        return self.outputObject


class NNModel(NNLayer):
    def __init__(self, nnInputNum, nnOutputNum):
        super(NNModel, self).__init__()
        self.inputNum = nnOutputNum
        self.outputNum = nnInputNum

        self.nnInputLayer = NNFullConnectedLayer(nnInputNum)
        self.nnOutputLayer = NNFullConnectedLayer(nnOutputNum)
        self.nnInputLayer.SetOutputObject(self.nnOutputLayer)
        self.nnOutputLayer.SetInputObject(self.nnInputLayer)

        self.formatFile = "../Resources/ModelSample.txt"

        self.layers = [self.nnOutputLayer]

    def AppendLayer(self, layer):
        self.layers.append(layer)

    def RemoveLayer(self, layer):
        self.layers.remove(layer)

    def Serialize(self, modelName, filepath):
        layerSerialized = ""

        layer = self.nnInputLayer
        while layer.GetOutputObject() is not None:
            layerSerialized += layer.GetOutputObject().Serialize()
            layer = layer.GetOutputObject()

        srcF = open(self.formatFile, 'r')
        out = str(srcF.read())
        out = re.sub("<name>", modelName, out)
        out = re.sub("<layers>", layerSerialized, out)

        with open(filepath, 'w') as F:
            F.write(out)

        srcF.close()


class NNFullConnectedLayer(NNLayer):
    def __init__(self, nodeNum, activationFunc=ActivationFuncs.NoFunc, inputObject=None, outputObject=None):
        super(NNFullConnectedLayer, self).__init__(inputObject, outputObject)

        self.nodeNum = nodeNum
        self.activationFunc = activationFunc

    def Serialize(self):
        # 线性层输入输出连接性检查
        assert self.inputObject is not None, "inputObject cannot be None"

        out = "            nn.Linear(%d, %d),\n" % (self.inputObject.nodeNum, self.nodeNum)
        if self.activationFunc != ActivationFuncs.NoFunc:
            out += "            nn.%s(inplace=True),\n" % FUNCNAMES[self.activationFunc]

        return out
