
		
#SET PATH=%PATH%;C:\Users\Иванова\Desktop\НУЖНОЕ\1\We\source\p\fd\fd\myq
#python main.py

from PyQt5.QtWidgets import (QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,
QListView,QLabel,QPushButton,QGraphicsView,
QSpinBox)
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication,QLayout
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsEllipseItem,QGraphicsLineItem,QListWidget ,QSizePolicy , QGraphicsRectItem,QListWidgetItem
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QColor,QBrush,QPen,QTransform ,QPixmap,QCursor,QIcon

class Cell(QGraphicsRectItem):
	def __init__(self,row,col):
		QGraphicsRectItem.__init__(self)
		self.row=row
		self.col=col
		self.setRect(0, 0, 20, 20)
		
		self.setBrush(QColor(0,128,0))
		
		self.setX(self.row*20)
		self.setY(self.col*20)
		#self.setAcceptHoverEvents(True)
		self.color=QColor(0,128,0);
	def mousePressEvent(self,event):
		if event.button() ==Qt.LeftButton:
			self.color=self.scene().activeColor;
			self.setBrush(self.color)
		
	def hoverEnterEvent(self ,event):
		self.setBrush(self.scene().activeColor)
		
	def hoverLeaveEvent(self,event):
		self.setBrush(self.color)
		
class Scene(QGraphicsScene):
	defaultColor=QColor(128,0,0);
	def __init__(self):
		QGraphicsScene.__init__(self)
		self.table=[]
		self.activeColor=Scene.defaultColor;
		self.isClickLeftButtonMouse=False;
		self.lastItem=None
	def MyClear(self):
		self.table.clear()
	def MyInit(self,rows,columns):
		for row in range(rows):
			for col in range(columns):
				cell=Cell(row,col)
				self.addItem(cell)
				
	def mousePressEvent(self, event):
		self.isClickLeftButtonMouse=True;
		
		item=self.itemAt(event.scenePos().x(),event.scenePos().y(),QTransform())
		if None==item:
			return
		item.setBrush(self.activeColor)
		item.color=self.activeColor
		
		
	def mouseReleaseEvent(self,event):
		self.isClickLeftButtonMouse=False;
		
		item=self.itemAt(event.scenePos().x(),event.scenePos().y(),QTransform())
		if None==item:
			return
		item.setBrush(self.activeColor)
		item.color=self.activeColor
		
	def mouseMoveEvent(self,event):
		item=self.itemAt(event.scenePos().x(),event.scenePos().y(),QTransform())
		if None==item:
			return
		if self.isClickLeftButtonMouse:
			item.setBrush(self.activeColor)
			item.color=self.activeColor
		else:
			if self.lastItem==None:
				self.lastItem=item
				item.setBrush(self.activeColor)
			elif self.lastItem!=item:
				self.lastItem.setBrush(self.lastItem.color)
				self.lastItem=item
				item.setBrush(self.activeColor)
		
class List(QListWidget):
	def __init__(self,scene):
		QListWidget.__init__(self)
		self.itemClicked.connect(self.clicked)
		self.scene=scene
		self.lastItem=None;
		
	def clicked(self,item):
		self.updateLastItem(item)
		
	def updateLastItem(self,item):
		if None==self.lastItem:
			self.lastItem=item
			self.scene.activeColor=item.background().color()
		elif item==self.lastItem:
			self.lastItem=None
			self.scene.activeColor=Scene.defaultColor
		else:
			self.lastItem=item
			self.scene.activeColor=item.background().color()
			
			
class MainWindow(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		
		self.setWindowTitle("Map Editor")
		self.setWindowIcon(QIcon("tree.png"));

			
		mainLayout=QHBoxLayout(self)
		rightLayout=QVBoxLayout()
		
		rightLayout.setAlignment(Qt.AlignTop)
		
		clearButton=QPushButton("Очистить")
		downloadButton=QPushButton("Выгрузить")
		

		
		self.view=QGraphicsView()
		self.view.setMouseTracking(True)
		mainLayout.addWidget(self.view)
		mainLayout.addLayout(rightLayout)
		
		self.rowsEdit=QSpinBox();
		self.rowsEdit.setSingleStep(5);
		self.rowsEdit.setValue(20);
		self.rowsEdit.setMinimum(3);
		self.rowsEdit.setSuffix(" rows");
		
		self.columnsEdit=QSpinBox();
		self.columnsEdit.setSingleStep(5);
		self.columnsEdit.setValue(20);
		self.columnsEdit.setMinimum(3);
		self.columnsEdit.setSuffix(" columns");
		
		
		self.scene=Scene()
		self.view.setScene(self.scene)
		
		self.list=List(self.scene)
		
		
		rightLayout.setSpacing(5)
		rightLayout.setSizeConstraint(QLayout.SetMinimumSize)
		
		rightWidgets=[
			clearButton,
			downloadButton,
			self.rowsEdit,
			self.columnsEdit,
		]
		Alignment=Qt.AlignLeft | Qt.AlignTop
		for rightWidget in rightWidgets:
			rightWidget.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
			rightLayout.addWidget(rightWidget,Alignment)
			
		self.list.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)
		rightLayout.addWidget(self.list,Alignment)
		
		colors=[
			QColor(50, 205, 50),
			QColor(255, 20, 147),
			QColor(0, 128, 0),
			QColor(128, 128, 0),
			QColor(0, 128, 128),
			QColor(0, 0, 139),
			QColor(138, 43, 226),
			QColor(147, 112, 219),
			QColor(128, 0, 128),
			QColor(75, 0, 130),
			QColor(106, 90, 205),
			QColor(218, 165, 32),
			QColor(205, 133, 63),
			QColor(139, 69, 19),
			QColor(160, 82, 45),
		]
		for color in colors:
			item=QListWidgetItem();
			item.setBackground(color)
			self.list.addItem(item)
		
		

		
		clearButton.clicked.connect(self.clear_trigger)    
		
	def clear_trigger(self):
		maxRow=self.rowsEdit.value()+2
		maxColumns=self.columnsEdit.value()+2
		self.scene.MyClear()
		self.scene.MyInit(maxRow,maxColumns)
		

app = QApplication([])
livePleaseDontDelete=MainWindow()
livePleaseDontDelete.show()
app.exec_()
