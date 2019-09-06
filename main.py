
		
#SET PATH=%PATH%;C:\Users\Иванова\Desktop\НУЖНОЕ\1\We\source\p\fd\fd\myq
#python main.py

from PyQt5.QtWidgets import (QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,
QListView,QLabel,QPushButton,QGraphicsView,
QSpinBox)
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsEllipseItem,QGraphicsLineItem,QListWidget ,QSizePolicy , QGraphicsRectItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor,QBrush,QPen,QTransform

class Cell(QGraphicsRectItem):
	def __init__(self,row,col):
		QGraphicsRectItem.__init__(self)
		self.row=row
		self.col=col
		self.setRect(0, 0, 20, 20)
		
		self.setBrush(QColor(0,128,0))
		
		self.setX(self.row*20)
		self.setY(self.col*20)
		
class Scene(QGraphicsScene):
	def __init__(self):
		QGraphicsScene.__init__(self)
		self.table=[]
	def MyClear(self):
		self.table.clear()
	def MyInit(self,rows,columns):
		for row in range(rows):
			for col in range(columns):
				cell=Cell(row,col)
				self.addItem(cell)
		
class MainWindow(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		
		mainLayout=QHBoxLayout(self)
		rightLayout=QVBoxLayout()
		
		clearButton=QPushButton("Очистить")
		downloadButton=QPushButton("Выгрузить")
		rightLayout.addWidget(clearButton)
		rightLayout.addWidget(downloadButton)
		
		self.view=QGraphicsView()
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
		
		rightLayout.addWidget(self.rowsEdit)
		rightLayout.addWidget(self.columnsEdit)
		
		self.scene=Scene()
		self.view.setScene(self.scene)
		
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
