
		
#SET PATH=%PATH%;C:\Users\Иванова\Desktop\НУЖНОЕ\1\We\source\p\fd\fd\myq
#python main.py

from PyQt5.QtWidgets import (QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,
QListView,QLabel,QPushButton,QGraphicsView,
QSpinBox)
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication,QLayout
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsEllipseItem,QGraphicsLineItem,QListWidget ,QSizePolicy , QGraphicsRectItem,QListWidgetItem
from PyQt5.QtCore import QTimer,Qt,QMimeData
from PyQt5.QtGui import QColor,QBrush,QPen,QTransform ,QPixmap,QCursor,QIcon
import json
class Colors():
	fileName="conf.json"
	fileError="log.txt"
	KeyColors="COLORS"
	def __init__(self):	
		self.colors=[]
		
		self.clearLog()
		try:
			with open(Colors.fileName,"r") as file:
				json_string=file.read()
				data={}
				try:
					data = json.loads(json_string)
				except Exception  as e:
					textError=str( type(e) ) +" | " + str(e)
					self.log(textError)
				colors=data.get( Colors.KeyColors, None)
				if None==colors:
					self.createDefaultValue()
					return;
				if type(colors) == list:
					self.colors=colors
				else:
					self.createDefaultValue()
		except IOError as e:
			self.createDefaultValue()
			
	def createDefaultValue(self):
		jsonObj={}
		self.colors=[
			{"r":50,"g":205,"b":50},
			{"r":255,"g":20,"b":147},
			{"r":0,"g":128,"b":0},
			{"r":128,"g":128,"b":0},
			{"r":0,"g":128,"b":128},
			{"r":0,"g":0,"b":139},
			{"r":138,"g":43,"b":226},
			{"r":147,"g":112,"b":219},
			{"r":128,"g":0,"b":128},
			{"r":75,"g":0,"b":130},
			{"r":106,"g":90,"b":205},
			{"r":218,"g":165,"b":32},
			{"r":205,"g":133,"b":63},
			{"r":139,"g":69,"b":19},
			{"r":160,"g":82,"b":45},
		]
		jsonObj[Colors.KeyColors]=self.colors
		
		
		with open(Colors.fileName,"w") as file:
			json_string = json.dumps(jsonObj,indent=4)
			file.write(json_string)
			
	def log(self,textError):
		with open(Colors.fileError,"w") as file:
			file.write(textError)
			
	def clearLog(self):
		with open(Colors.fileError,"w") as file:
			file.write("")
			
	def saveColors(self,QColorsList):
		self.colors=[]
		
		for qcolor in QColorsList:
			c={}
			c["r"]=qcolor.red()
			c["g"]=qcolor.green()
			c["b"]=qcolor.blue()
			self.colors.append(c)
			
		jsonObj={}
		jsonObj[Colors.KeyColors]=self.colors
		with open(Colors.fileName,"w") as file:
			json_string = json.dumps(jsonObj,indent=4)
			file.write(json_string)
		
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
			
	def getColors(self):
	
		ListWidgetItems =[]
		QColorsList=[]
		for i in range(self.count()) :
			ListWidgetItems.append( self.item(i))
		for item in ListWidgetItems:
			QColorsList.append( item.background().color() )
		
		print(len(QColorsList))
		return QColorsList
		
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
		
		# colors=[
			# QColor(50, 205, 50),
			# QColor(255, 20, 147),
			# QColor(0, 128, 0),
			# QColor(128, 128, 0),
			# QColor(0, 128, 128),
			# QColor(0, 0, 139),
			# QColor(138, 43, 226),
			# QColor(147, 112, 219),
			# QColor(128, 0, 128),
			# QColor(75, 0, 130),
			# QColor(106, 90, 205),
			# QColor(218, 165, 32),
			# QColor(205, 133, 63),
			# QColor(139, 69, 19),
			# QColor(160, 82, 45),
		# ]
		self.colors=Colors();
		for colorObj in self.colors.colors:
		
			color=QColor( colorObj["r"],colorObj["g"],colorObj["b"])
			item=QListWidgetItem();
			item.setBackground(color)
			self.list.addItem(item)
		
		

		self.saveColors()
		clearButton.clicked.connect(self.clear_trigger)    
		
	def saveColors(self):
		colors=self.list.getColors()
		self.colors.saveColors(colors)
	def clear_trigger(self):
		maxRow=self.rowsEdit.value()+2
		maxColumns=self.columnsEdit.value()+2
		self.scene.MyClear()
		self.scene.MyInit(maxRow,maxColumns)
		

app = QApplication([])
livePleaseDontDelete=MainWindow()
livePleaseDontDelete.show()
app.exec_()
