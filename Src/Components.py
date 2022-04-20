from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QSize, QLine, QRectF, QPointF, QSizeF
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, \
    QGraphicsPathItem


# 神经网络场景
class NNGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(NNGraphicsScene, self).__init__(parent)

        self.layers = []
        self.pipes = []

    def AddLayer(self, layer):
        self.layers.append(layer)
        self.addItem(layer)

    def RemoveLayer(self, layer):
        self.layers.remove(layer)
        self.removeItem(layer)

    def AddPipe(self, pipe):
        self.pipes.append(pipe)
        self.addItem(pipe)

    def RemovePipe(self, pipe):
        self.pipes.remove(pipe)
        self.removeItem(pipe)


# 神经网络场景视图
class NNGraphicsView(QGraphicsView):
    def __init__(self, parent):
        super(NNGraphicsView, self).__init__(parent)
        self.scene = NNGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(self.RubberBandDrag)

        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def DisplayNewLayer(self, pos, layer):
        layer.setPos(pos)
        self.scene.AddLayer(layer)


# 神经网络层组件
class NNLayerWidget(QGraphicsRectItem):
    def __init__(self, size, parent=None):
        super(NNLayerWidget, self).__init__(parent)
        self.setRect(QRectF(QPointF(0, 0), size))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.nodeNum = 0
        self.nodeNumWidget = QGraphicsTextItem(str(self.nodeNum), self)

    def SetNodeNum(self, nodeNum):
        self.nodeNum = nodeNum
        self.nodeNumWidget.setPlainText(str(self.nodeNum))


class InputLayerWidget(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(InputLayerWidget, self).__init__(size, parent)


class OutputLayerWidgt(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(OutputLayerWidgt, self).__init__(size, parent)


class FullConnectedLayerWidget(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(FullConnectedLayerWidget, self).__init__(size, parent)


# 神经网络数据管道组件
class NNPipe(QGraphicsPathItem):
    def __init__(self, parent=None):
        super(NNPipe, self).__init__(parent)

        self.width = 3.0

        self._pen = QPen(QColor("#000"))
        self._pen.setWidthF(self.width)

        self._penDrag = QPen(QColor("#000"))
        self._penDrag.setStyle(Qt.DashDotLine)
        self._penDrag.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.pointSource = QPointF(0, 0)
        self.pointDestination = QPointF(0, 0)

    def CalcuPath(self):
        path = QPainterPath(self.pointSource)
        path.lineTo(self.pointDestination)
        return path

    def boundingRect(self) -> QtCore.QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QtGui.QPainterPath:
        return self.CalcuPath()

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget=None) -> None:
        self.setPath(self.CalcuPath())
        path = self.path()

        if self.edge.destObject is None:
            # 绘制拖拽线
            painter.setPen(self._penDrag)
            painter.drawPath(path)
        else:
            # 绘制连接线
            painter.setPen(self._pen)
            painter.drawPath(path)

# TODO 添加pipe管理类
