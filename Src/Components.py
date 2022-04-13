from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QWidget


# 神经网络层组件
class NNLayerWidget(QWidget):
    def __init__(self, parent, size):
        super(NNLayerWidget, self).__init__(parent)
        self.currentPos = None
        self.resize(size)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        print(e.pos())
        self.currentPos = e.pos()
        e.accept()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        newPos = self.mapTo(self.parent(), self.mapFromGlobal(e.globalPos() - self.currentPos))
        print(newPos)

        self.move(newPos)

        e.accept()


class InputLayerWidget(NNLayerWidget):
    def __init__(self, parent, size):
        super(InputLayerWidget, self).__init__(parent, size)

        self.nodeNum = 0
        self.outputLayer = None

    def SetNodeNum(self, num):
        """
        设置节点数
        :param num: 节点数
        """
        self.nodeNum = num

    def SetOutputObject(self, outputLayer):
        """
        设置输出层对象
        :param outputLayer: 输出层对象
        """
        self.outputLayer = outputLayer

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()

        brush.setColor(QtGui.QColor("red"))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(QPoint(0, 0), QSize(painter.device().width(), painter.device().height()))
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('white'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)

        painter.drawText(rect, Qt.AlignCenter, "node->{}\nOutput->{}".format(self.nodeNum, self.outputLayer))

        painter.end()


class OutputLayerWidgt(NNLayerWidget):
    def __init__(self, parent, size):
        super(OutputLayerWidgt, self).__init__(parent, size)

        self.nodeNum = 0
        self.inputLayer = None

    def SetNodeNum(self, num):
        """
        设置节点数
        :param num: 节点数
        """
        self.nodeNum = num

    def SetInputObject(self, inputLayer):
        """
        设置输入层对象
        :param inputLayer: 输入层对象
        """
        self.inputLayer = inputLayer

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()

        brush.setColor(QtGui.QColor("blue"))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(QPoint(0, 0), QSize(painter.device().width(), painter.device().height()))
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('white'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)

        painter.drawText(rect, Qt.AlignCenter, "Inputput->{}\nnode->{}".format(self.inputLayer, self.nodeNum))

        painter.end()


class FullConnectedLayerWidget(NNLayerWidget):
    def __init__(self, parent, size):
        super(FullConnectedLayerWidget, self).__init__(parent, size)

        self.nodeNum = 0
        self.inputLayer = None
        self.outputLayer = None

    def SetNodeNum(self, num):
        """
        设置节点数
        :param num: 节点数
        """
        self.nodeNum = num

    def SetInputLayer(self, inputLayer):
        """
        设置输入层对象
        :param inputLayer: 输入层对象
        """
        self.inputLayer = inputLayer

    def SetOutputLayer(self, outputLayer):
        """
        设置输出层对象
        :param outputLayer: 输出层对象
        """
        self.outputLayer = outputLayer

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()

        brush.setColor(QtGui.QColor("green"))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(QPoint(0, 0), QSize(painter.device().width(), painter.device().height()))
        painter.fillRect(rect, brush)

        pen = painter.pen()
        pen.setColor(QtGui.QColor('white'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Times')
        font.setPointSize(10)
        painter.setFont(font)

        painter.drawText(rect, Qt.AlignCenter,
                         "Inputput->{}\nnode->{}\nOutput->{}".format(self.inputLayer, self.nodeNum, self.outputLayer))

        painter.end()


# 神经网络数据管道组件
class NNDataPipe(QWidget):
    def __init__(self, parent, inputObject, outputObject):
        super(NNDataPipe, self).__init__(parent)
        self.inputObject = inputObject
        self.outputObject = outputObject

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        # TODO 实现渲染函数
        pass
