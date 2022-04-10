from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QWidget


# 神经网络层组件
class InputLayerWidget(QWidget):
    def __init__(self, parent):
        super(InputLayerWidget, self).__init__(parent)

        self.nodeNum = 0
        self.outputLayer = None

        self.resize(250, 100)

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


class OutputLayerWidgt(QWidget):
    def __init__(self, parent):
        super(OutputLayerWidgt, self).__init__(parent)

        self.nodeNum = 0
        self.inputLayer = None

        self.resize(250, 100)

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


class FullConnectedLayerWidget(QWidget):
    def __init__(self, parent):
        super(FullConnectedLayerWidget, self).__init__(parent)

        self.nodeNum = 0
        self.inputLayer = None
        self.outputLayer = None

        self.resize(500, 100)

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
