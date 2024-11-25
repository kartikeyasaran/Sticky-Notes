#GitHub : @CodeYard01
#YouTUbe : @CodeYard
from PyQt5 import QtWidgets, uic,QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
from NotesUI import Ui_MainWindow
import random
import os

def Last_window_id():
    file_path = 'window_id.notes'
    try:
        with open(file_path,'r') as file:
            id = file.read()
            global window_id        
            window_id = id
    except FileNotFoundError:
        with open(file_path,'w') as file_write:
            window_id = 1
            file_write.write(str(window_id))

windows = [1]
Last_window_id()#change icon, 

def Update_window_id():
    file_path = 'window_id.notes'
    with open(file_path,'w') as file:
        global window_id
        window_id = int(window_id)
        file.write(str(window_id))
def del_window_id():
    file_path= 'window_id.notes'
    with open(file_path,'w') as file_del:
        global window_id
        if int(window_id) > 1:
            window_id = int(window_id) - 1
            file_del.write(str(window_id))
        else:
            file_del.write('1')

class Main(QtWidgets.QMainWindow):
    def __init__(self,window_id):
        super().__init__()
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(random.randint(400,900), random.randint(100,500), 260, 360)
        self.Ui.addbtn.clicked.connect(self.addNewWindow)
        self.window_id = window_id
        self.Ui.delbtn.clicked.connect(self.delete)
        self.Ui.pushButton.clicked.connect(self.changeTextEditBackground)
        self.dragging = False
        self.offset = QtCore.QPoint()
        random_color = QtGui.QColor(random.randint(23, 232), random.randint(27, 237), random.randint(29, 235))
        self.Ui.textEdit.setStyleSheet(f"background-color: {random_color.name()};border:transparent;")
        self.loadTextFromFile()  
        self.Ui.textEdit_2.textChanged.connect(self.autoSave)
        
    def addNewWindow(self):
        global window_id
        window_id = int(window_id)+1
        new_window = Main(window_id)
        windows.append(new_window)
        new_window.show()
        Update_window_id()
    def delete(self):
        self.close()
        del_window_id()
        n = 1
        file_path = f'notes_{self.window_id}.notes'
        
        
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')
        
        # Shift remaining note files
        for i in range(int(window_id) + 900):
            source_file = f'notes_{self.window_id + n}.notes'
            target_file = f'notes_{self.window_id + n - 1}.notes'
            try:
                if os.path.exists(target_file):
                    os.remove(target_file)  # Remove to avoid conflicts
                os.rename(source_file, target_file)
                n += 1
            except FileNotFoundError:
                break 
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False

    def changeTextEditBackground(self):
        random_color = QtGui.QColor(random.randint(20, 230), random.randint(20, 230), random.randint(20, 230))

        self.Ui.textEdit.setStyleSheet(f"background-color: {random_color.name()};border:transparent;")
    def autoSave(self):
        file_path = f"notes_{self.window_id}.notes"

        with open(file_path, 'w') as file:
            file.write(self.Ui.textEdit_2.toPlainText())

    def loadTextFromFile(self):
        file_path = f"notes_{self.window_id}.notes"
        try:
            with open(file_path, 'r') as file:
                text_content = file.read()
                self.Ui.textEdit_2.setPlainText(text_content)
        except FileNotFoundError:
            pass

app = QtWidgets.QApplication(sys.argv)
id = 1
for i in range(int(window_id)):
    window = Main(id)
    windows.append(window)
    window.show()
    id += 1
app.exec_()