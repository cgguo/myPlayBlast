# *_*coding:utf-8 *_*
try:
    from PySide import QtGui, QtCore
except ImportError:
    from PySide2 import QtWidgets as QtGui
    
class MayaDatas(object):
    def __init__(self, example):
        import maya.cmds as cmds
        self._cmds = cmds
        self._example = example
        
    def choseFile(self):
        s = QtGui.QFileDialog.getOpenFileName(None, u"选择路径", "/", filter="All Files (*.mb *.ma)")
        self._example.name_line_edit_file.setText(s[0])
        return s[0]
        
    def outFile(self):
        out = QtGui.QFileDialog.getSaveFileName(None, u"选择路径", "/")
        self._example.name_line_edit_file1.setText(out[0])
        return out[0]
        
    def getGeoPose(self):
        Listx = []
        Listy = []
        Listz = []
        selection = cmds.ls(tr=True, dag=True, v=True)
        sel_length = len(selection)
        for each in range(0, sel_length, 1):
            sel_pos_tx = cmds.getAttr(selection[each] + ".translateX")
            Listx.append(sel_pos_tx)
            sel_pos_ty = cmds.getAttr(selection[each] + ".translateY")
            Listy.append(sel_pos_ty)
            sel_pos_tz = cmds.getAttr(selection[each] + ".translateZ")
            Listz.append(sel_pos_tz)
        return (Listx, Listy, Listz)
        
    def countPose(self):
        geoPose = self.getGeoPose()
        for eachx in geoPose[0]:
            Listx_length = len(geoPose[0])
            sumx = 0
            sumx += eachx
            average_x = sumx / Listx_length
        for eachy in geoPose[1]:
            Listy_length = len(geoPose[1])
            sumy = 0
            sumy += eachy
            average_y = sumy / Listy_length
        for eachz in geoPose[1]:
            Listz_length = len(geoPose[2])
            sumz = 0
            sumz += eachz
            average_z = sumz / Listz_length
        return (average_x, average_y, average_z)
        
    def OK_button(self):
        input_file_name = self._example.name_line_edit_file.text()
        out_file_name = self._example.name_line_edit_file1.text()
        cmds.file(input_file_name, reference=True)
        currentPose = self.countPose()
        Start_Frame = self._example.name_line_edit_frame.text()
        End_Frame = self._example.name_line_edit_to.text()
        ComboBox_format_name1 = self._example.ComboBox_format.currentText()
        ComboBox_format_name = str(ComboBox_format_name1)
        ComboBox_resolution_value = self._example.ComboBox_resolution.currentText()
        ComboBox_resolution_value1 = ComboBox_resolution_value.split("*", 1)
        width_value = int(ComboBox_resolution_value1[0])
        higth_value = int(ComboBox_resolution_value1[1])
        camera_name = cmds.camera(p=(currentPose[0] * 2 + 5, currentPose[1] * 2 + 5, currentPose[2] * 2 + 5),wci=(0, 0, 0))
        cmds.move(currentPose[0], currentPose[1], currentPose[2], camera_name[0] + ".scalePivot",camera_name[0] + ".rotatePivot")
        cmds.playbackOptions(min=int(Start_Frame), max=int(End_Frame))
        cmds.rotate(0, '0', 0, camera_name[0], pivot=(currentPose[0], currentPose[1], currentPose[2]))
        cmds.setKeyframe(camera_name[0], at='rotateY', t=int(Start_Frame))
        cmds.rotate(0, '360', 0, camera_name[0], pivot=(currentPose[0], currentPose[1], currentPose[2]))
        cmds.setKeyframe(camera_name[0], at='rotateY', t=int(End_Frame))
        cmds.rotate("-17", 0, 0, camera_name[0], pivot=(currentPose[0], currentPose[1], currentPose[2]), ws=1)       
        cmds.lookThru(camera_name[0])
        cmds.playblast(p=60,wh=(width_value,higth_value),v=False,format=ComboBox_format_name, viewer=False,
                 f=out_file_name, cc=1, st=int(Start_Frame), et=int(End_Frame))
    def Cancle_button(self):
        self._example.close()
        
        
class Example(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setGeometry(600, 300, 500, 500)
        self.setWindowTitle('360 Playblast')
        Browse_Button = QtGui.QPushButton("Browse")
        name_label_file = QtGui.QLabel("Open file")
        self.name_line_edit_file = QtGui.QLineEdit()
        name_label_Frame = QtGui.QLabel("From")
        self.name_line_edit_frame = QtGui.QLineEdit()
        name_label_to = QtGui.QLabel("To")
        self.name_line_edit_to = QtGui.QLineEdit()
        name_label_Format = QtGui.QLabel("Format")
        self.ComboBox_format = QtGui.QComboBox()
        self.ComboBox_format.addItems(["avi", "image", "qt", "movie"])
        name_label_resolution = QtGui.QLabel("Resoultion")
        self.ComboBox_resolution = QtGui.QComboBox()
        self.ComboBox_resolution.addItems(["1920*1080", "1080*720", "720*540"])
        Browse_Button_to = QtGui.QPushButton("Browse")
        name_label_to1 = QtGui.QLabel("To")
        self.name_line_edit_file1 = QtGui.QLineEdit()
        name_button_OK = QtGui.QPushButton("OK")
        name_button_Canle = QtGui.QPushButton("Canle")
        baseLayout = QtGui.QGridLayout()
        baseLayout.addWidget(Browse_Button, 0, 2)
        baseLayout.addWidget(name_label_file, 0, 0)
        baseLayout.addWidget(self.name_line_edit_file, 0, 1)
        baseLayout.addWidget(name_label_Frame, 1, 0)
        baseLayout.addWidget(self.name_line_edit_frame, 1, 1)
        baseLayout.addWidget(name_label_to, 1, 2)
        baseLayout.addWidget(self.name_line_edit_to, 1, 3)
        baseLayout.addWidget(name_label_Format, 2, 0)
        baseLayout.addWidget(self.ComboBox_format, 2, 1)
        baseLayout.addWidget(name_label_resolution, 3, 0)
        baseLayout.addWidget(self.ComboBox_resolution, 3, 1)
        baseLayout.addWidget(name_label_to1, 4, 0)
        baseLayout.addWidget(self.name_line_edit_file1, 4, 1)
        baseLayout.addWidget(Browse_Button_to, 4, 2)
        baseLayout.addWidget(name_button_OK, 5, 1)
        baseLayout.addWidget(name_button_Canle, 5, 3)
        self.setLayout(baseLayout)
        self._exampleDatas = MayaDatas(self)
        name_button_OK.clicked.connect(self._exampleDatas.OK_button)
        name_button_Canle.clicked.connect(self._exampleDatas.Cancle_button)
        Browse_Button.clicked.connect(self._exampleDatas.choseFile)
        Browse_Button_to.clicked.connect(self._exampleDatas.outFile)
        
if __name__ == "__main__":
    # app=QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
# app.exec_()
