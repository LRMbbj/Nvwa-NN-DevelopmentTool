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


class NNModel:
    def __init__(self, inputNum, outputNum):
        self.inputNum = inputNum
        self.outputNum = outputNum

        self.formatFile = "../Resources/ModelSample.txt"

        self.hiddenLayers = []

    def AppendLayer(self, layer):
        self.hiddenLayers.append(layer)

    def Serialize(self, name, filepath):
        layerSerialized = ""

        for layer in self.hiddenLayers:
            layerSerialized += layer.Serialize()

        srcF = open(self.formatFile, 'r')
        out = str(srcF.read())
        out = re.sub("<name>", name, out)
        out = re.sub("<layers>", layerSerialized, out)

        with open(filepath, 'w') as F:
            F.write(out)

        srcF.close()


class NNLayer:
    def __init__(self, inputObject, outputObject):
        self.inputObject = inputObject
        self.outputObject = outputObject

    def SetInputObject(self, obj):
        self.inputObject = obj

    def SetOutputObject(self, obj):
        self.outputObject = obj


class NNFullConnectedLayer(NNLayer):
    def __init__(self, nodeNum, inputObject=None, outputObject=None, activationFunc=ActivationFuncs.NoFunc):
        super(NNFullConnectedLayer, self).__init__(inputObject, outputObject)

        self.nodeNum = nodeNum
        self.activationFunc = activationFunc

    def Serialize(self):
        # 线性层输入输出连接性检查
        assert self.inputObject is not None, "inputObject cannot be None"
        assert self.outputObject is not None, "outputObject cannot be None"

        out = "            nn.Linear(%d, %d),\n" % (self.inputObject.inputNum, self.nodeNum)
        if self.activationFunc != ActivationFuncs.NoFunc:
            out += "            nn.%s(inplace=True),\n" % FUNCNAMES[self.activationFunc]

        return out


if __name__ == '__main__':
    model = NNModel(3, 1)
    model.AppendLayer(NNFullConnectedLayer(model, ActivationFuncs.ReLU))
    model.hiddenLayers[0].outputObject = model

    model.Serialize("myModel", "MyModel.py")
