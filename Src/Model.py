import NNStructureParts
from NNStructureParts import ActivationFuncs


class Model:
    def __init__(self):
        self.nn = None

    def CreateNN(self, inputNum, OutputNum):
        self.nn = NNStructureParts.NNModel(inputNum, OutputNum)

    def CreateFullConnectedLayer(self, nodeNum, activationFunc=ActivationFuncs.NoFunc):
        layer = NNStructureParts.NNFullConnectedLayer(nodeNum, activationFunc)
        self.nn.AppendLayer(layer)
        return layer

    def InsertBetweenLayers(self, inputLayer, outputLayer, pluginLayer):
        pluginLayer.SetInputObject(inputLayer)
        inputLayer.SetOutputObject(pluginLayer)

        pluginLayer.SetOutputObject(outputLayer)
        outputLayer.SetInputObject(pluginLayer)

    def RemoveLayer(self, removingLayer):
        removingLayer.inputObject.SetOutputObject(removingLayer.outputObject)
        removingLayer.outputObject.SetInputObject(removingLayer.inputObject)

        self.nn.RemoveLayer(removingLayer)

    def ConnectLayer(self, sourceLayer, destinationLayer):
        sourceLayer.SetOutputObject(destinationLayer)
        destinationLayer.SetInputObject(sourceLayer)

    def DisconnectLayer(self, sourceLayer, destinationLayer):
        sourceLayer.SetInputObject(None)
        destinationLayer.SetInputObject(None)

    def SerializeModel(self, modelName, filepath):
        self.nn.Serialize(modelName, filepath)


if __name__ == '__main__':
    model = Model()
    model.CreateNN(5,3)
    newlayer1 = model.CreateFullConnectedLayer(7, ActivationFuncs.ReLU)
    model.InsertBetweenLayers(newlayer1, model.nn.nnInputLayer, model.nn.nnOutputLayer)
    newlayer2 = model.CreateFullConnectedLayer(20, ActivationFuncs.ReLU)
    model.InsertBetweenLayers(newlayer2, newlayer1, model.nn.nnOutputLayer)

    model.SerializeModel("myModel", "MyModel.py")
