from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, \
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

    def mouseMoveEvent(self, event) -> None:
        if self.isSelected():
            for pipe in [x for x in self.scene().pipes if x.pipeWarp.startItem == self or x.pipeWarp.endItem == self]:
                pipe.pipeWarp.UpdatePositions()
        super(NNLayerWidget, self).mouseMoveEvent(event)

    def dropEvent(self, e) -> None:
        print(e)


# 神经网络场景视图
class NNGraphicsView(QGraphicsView):
    signalConnectLayer = pyqtSignal(NNLayerWidget, NNLayerWidget)
    signalInsertLayer = pyqtSignal(NNLayerWidget, NNLayerWidget, NNLayerWidget)
    signalDisconnectLayer = pyqtSignal(NNLayerWidget, NNLayerWidget)

    def __init__(self, parent):
        super(NNGraphicsView, self).__init__(parent)

        self.dragPipe = None
        self.dragStartItem = None

        self.drawPipeEnable = False
        self.insertLayerEnable = False

        self.scene = NNGraphicsScene(self)
        self.scene.setSceneRect(QRectF(0, 0, self.size().width(), self.size().height()))
        self.setScene(self.scene)
        self.setDragMode(self.RubberBandDrag)

        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def DisplayNewLayer(self, pos, layer):
        layer.setPos(pos)
        self.scene.AddLayer(layer)

    def PipeDragStart(self, item):
        self.dragStartItem = item
        self.dragPipe = NNPipe(self.scene, self.dragStartItem, None)

    def PipeDragEnd(self, item):
        # self.signalConnectLayer.emit(self.dragStartItem, item)
        newEdge = NNPipe(self.scene, self.dragStartItem, item)
        self.dragPipe.Remove()
        self.dragPipe = None
        newEdge.Store()
        self.signalConnectLayer.emit(self.dragStartItem, item)
        
    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_E:
            self.drawPipeEnable = ~self.drawPipeEnable
            self.insertLayerEnable = False
        elif event.key() == Qt.Key_R:
            self.insertLayerEnable = ~self.insertLayerEnable
            self.drawPipeEnable = False
            
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        item = self.itemAt(event.pos())
        if item is not None and event.button() == Qt.LeftButton and self.drawPipeEnable:
            # 连接物体
            if isinstance(item, NNLayerWidget):
                self.PipeDragStart(item)
        elif item is not None and event.button() == Qt.RightButton and self.drawPipeEnable :
            # 删除连接
            if isinstance(item, GraphicPipe):
                pipe = item.pipeWarp
                self.signalDisconnectLayer.emit(pipe.startItem, pipe.endItem)
                item.pipeWarp.Remove()
        else:
            super(NNGraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        onItem = self.itemAt(event.pos())
        if self.drawPipeEnable:
            self.drawPipeEnable = False
            if isinstance(onItem, NNLayerWidget) and onItem is not self.dragStartItem:
                self.PipeDragEnd(onItem)
            elif self.dragPipe is not None:
                self.dragPipe.Remove()
                self.dragPipe = None
        elif self.insertLayerEnable and onItem is not None:
            collidingItems = self.scene.collidingItems(onItem)
            pipes = [x for x in collidingItems if isinstance(x, GraphicPipe)]
            if len(pipes) == 1 and not pipes[0].pipeWarp.IsConnected(onItem):
                pipe = pipes[0].pipeWarp
                self.signalInsertLayer.emit(pipe.startItem, pipe.endItem, onItem)
                pipes[0].pipeWarp.Insert(onItem)
            self.insertLayerEnable = False
        super().mouseReleaseEvent(event)
            
    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pos = event.pos()
        if self.drawPipeEnable and self.dragPipe is not None:
            onPos = self.mapToScene(pos)
            self.dragPipe.graphicPipe.SetDestinationPos(onPos)
            self.dragPipe.graphicPipe.update()
        super(NNGraphicsView, self).mouseMoveEvent(event)


class InputLayerWidget(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(InputLayerWidget, self).__init__(size, parent)
        self.setBrush(QBrush(Qt.red))


class OutputLayerWidgt(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(OutputLayerWidgt, self).__init__(size, parent)
        self.setBrush(QBrush(Qt.blue))


class FullConnectedLayerWidget(NNLayerWidget):
    def __init__(self, size, parent=None):
        super(FullConnectedLayerWidget, self).__init__(size, parent)
        self.setBrush(QBrush(Qt.yellow))


# 神经网络数据管道组件
class GraphicPipe(QGraphicsPathItem):
    def __init__(self, pipeWarp, parent=None):
        super(GraphicPipe, self).__init__(parent)

        self.width = 10.0
        self.pipeWarp = pipeWarp

        self._pen = QPen(QColor("#000"))
        self._pen.setWidthF(self.width)

        self._penDrag = QPen(QColor("#000"))
        self._penDrag.setStyle(Qt.DashDotLine)
        self._penDrag.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.pointSource = QPointF(0, 0)
        self.pointDestination = QPointF(0, 0)

        self.setSelected(True)

    def SetSourcePos(self, pos):
        self.pointSource = pos

    def SetDestinationPos(self, pos):
        self.pointDestination = pos

    def CalcuPath(self):
        path = QPainterPath(self.pointSource)
        path.lineTo(self.pointDestination)
        return path

    def boundingRect(self) -> QtCore.QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QtGui.QPainterPath:
        return self.CalcuPath()

    def paint(self, painter: QtGui.QPainter, option, widget=None) -> None:
        self.setPath(self.CalcuPath())
        path = self.path()

        if self.pipeWarp.endItem is None:
            # 绘制拖拽线
            painter.setPen(self._penDrag)
            painter.drawPath(path)
        else:
            # 绘制连接线
            painter.setPen(self._pen)
            painter.drawPath(path)


class NNPipe:
    def __init__(self, scene, startItem, endItem):
        super(NNPipe, self).__init__()
        self.scene = scene
        self.startItem = startItem
        self.endItem = endItem

        # 创建图形
        self.graphicPipe = GraphicPipe(self)
        self.scene.AddPipe(self.graphicPipe)

        if self.startItem is not None:
            self.UpdatePositions()

    def Store(self):
        # self.scene.AddPipe(self.graphicPipe)
        pass

    def UpdatePositions(self):
        sourcePos = self.startItem.pos()
        sourcePatch = self.startItem.rect().size()
        self.graphicPipe.SetSourcePos(
            QPointF(sourcePos.x() + sourcePatch.width() / 2, sourcePos.y() + sourcePatch.height() / 2))

        if self.endItem is not None:
            endPos = self.endItem.pos()
            endPatch = self.endItem.rect().size()
            self.graphicPipe.SetDestinationPos(
                QPointF(endPos.x() + endPatch.width() / 2, endPos.y() + endPatch.height() / 2))
        else:
            self.graphicPipe.SetDestinationPos(
                QPointF(sourcePos.x() + sourcePatch.width() / 2, sourcePos.y() + sourcePatch.height() / 2))

        self.graphicPipe.update()

    def RemoveCurrentItems(self):
        self.startItem = None
        self.endItem = None

    def Remove(self):
        self.RemoveCurrentItems()
        self.scene.RemovePipe(self.graphicPipe)
        self.graphicPipe = None

    def Insert(self, item):
        newPipe = NNPipe(self.scene, item, self.endItem)
        self.endItem = item
        self.UpdatePositions()

    def IsConnected(self, item):
        return self.startItem == item or self.endItem == item
