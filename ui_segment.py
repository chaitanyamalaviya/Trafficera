# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_segment.ui'
#
# Created: Fri Apr 17 11:47:00 2015
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Segment(object):
    def setupUi(self, Segment):
        Segment.setObjectName(_fromUtf8("Segment"))
        Segment.setEnabled(True)
        Segment.resize(484, 340)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        Segment.setFont(font)
        Segment.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Segment.setWindowTitle(_fromUtf8("iSimGis Converter"))
        Segment.setWindowOpacity(4.0)
        Segment.setToolTip(_fromUtf8(""))
        Segment.setStatusTip(_fromUtf8(""))
        Segment.setSizeGripEnabled(False)
        self.tabWidget_2 = QtGui.QTabWidget(Segment)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 491, 341))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.titleLabel = QtGui.QLabel(self.tab_2)
        self.titleLabel.setGeometry(QtCore.QRect(130, -40, 91, 17))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.errorMessage_2 = QtGui.QLabel(self.tab_2)
        self.errorMessage_2.setGeometry(QtCore.QRect(-50, 230, 6, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        font.setItalic(True)
        self.errorMessage_2.setFont(font)
        self.errorMessage_2.setStyleSheet(_fromUtf8("color: rgb(255, 20, 27)"))
        self.errorMessage_2.setText(_fromUtf8(""))
        self.errorMessage_2.setObjectName(_fromUtf8("errorMessage_2"))
        self.linkGroupBox = QtGui.QGroupBox(self.tab_2)
        self.linkGroupBox.setGeometry(QtCore.QRect(20, 10, 461, 39))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.linkGroupBox.setFont(font)
        self.linkGroupBox.setTitle(_fromUtf8(""))
        self.linkGroupBox.setObjectName(_fromUtf8("linkGroupBox"))
        self.linkIdLabel = QtGui.QLabel(self.linkGroupBox)
        self.linkIdLabel.setGeometry(QtCore.QRect(6, 6, 53, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.linkIdLabel.setFont(font)
        self.linkIdLabel.setObjectName(_fromUtf8("linkIdLabel"))
        self.linkidcomboBox = QtGui.QComboBox(self.linkGroupBox)
        self.linkidcomboBox.setGeometry(QtCore.QRect(70, 10, 371, 21))
        self.linkidcomboBox.setObjectName(_fromUtf8("linkidcomboBox"))
        self.actionButton = QtGui.QPushButton(self.tab_2)
        self.actionButton.setGeometry(QtCore.QRect(30, 250, 91, 25))
        self.actionButton.setMaximumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.actionButton.setFont(font)
        self.actionButton.setObjectName(_fromUtf8("actionButton"))
        self.attributeGroup_2 = QtGui.QGroupBox(self.tab_2)
        self.attributeGroup_2.setGeometry(QtCore.QRect(20, 70, 461, 145))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.attributeGroup_2.setFont(font)
        self.attributeGroup_2.setTitle(_fromUtf8(""))
        self.attributeGroup_2.setObjectName(_fromUtf8("attributeGroup_2"))
        self.categorylabel = QtGui.QLabel(self.attributeGroup_2)
        self.categorylabel.setGeometry(QtCore.QRect(250, 110, 75, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.categorylabel.setFont(font)
        self.categorylabel.setObjectName(_fromUtf8("categorylabel"))
        self.category = QtGui.QComboBox(self.attributeGroup_2)
        self.category.setGeometry(QtCore.QRect(320, 110, 131, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.category.setFont(font)
        self.category.setObjectName(_fromUtf8("category"))
        self.sequenceno = QtGui.QLineEdit(self.attributeGroup_2)
        self.sequenceno.setGeometry(QtCore.QRect(120, 40, 111, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.sequenceno.setFont(font)
        self.sequenceno.setObjectName(_fromUtf8("sequenceno"))
        self.capacity = QtGui.QLineEdit(self.attributeGroup_2)
        self.capacity.setGeometry(QtCore.QRect(320, 80, 131, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.capacity.setFont(font)
        self.capacity.setObjectName(_fromUtf8("capacity"))
        self.maxSpeed = QtGui.QLineEdit(self.attributeGroup_2)
        self.maxSpeed.setGeometry(QtCore.QRect(117, 77, 111, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.maxSpeed.setFont(font)
        self.maxSpeed.setObjectName(_fromUtf8("maxSpeed"))
        self.roadType = QtGui.QComboBox(self.attributeGroup_2)
        self.roadType.setGeometry(QtCore.QRect(118, 112, 111, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.roadType.setFont(font)
        self.roadType.setObjectName(_fromUtf8("roadType"))
        self.roadType.addItem(_fromUtf8(""))
        self.roadType.addItem(_fromUtf8(""))
        self.roadType.addItem(_fromUtf8(""))
        self.roadType.addItem(_fromUtf8(""))
        self.maxSpeedLabel = QtGui.QLabel(self.attributeGroup_2)
        self.maxSpeedLabel.setGeometry(QtCore.QRect(7, 77, 84, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.maxSpeedLabel.setFont(font)
        self.maxSpeedLabel.setObjectName(_fromUtf8("maxSpeedLabel"))
        self.sequencenoLabel = QtGui.QLabel(self.attributeGroup_2)
        self.sequencenoLabel.setGeometry(QtCore.QRect(7, 42, 91, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.sequencenoLabel.setFont(font)
        self.sequencenoLabel.setObjectName(_fromUtf8("sequencenoLabel"))
        self.lengthLabel = QtGui.QLabel(self.attributeGroup_2)
        self.lengthLabel.setGeometry(QtCore.QRect(250, 80, 63, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.lengthLabel.setFont(font)
        self.lengthLabel.setObjectName(_fromUtf8("lengthLabel"))
        self.roadTypeLabel = QtGui.QLabel(self.attributeGroup_2)
        self.roadTypeLabel.setGeometry(QtCore.QRect(7, 112, 91, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.roadTypeLabel.setFont(font)
        self.roadTypeLabel.setObjectName(_fromUtf8("roadTypeLabel"))
        self.idLabel = QtGui.QLabel(self.attributeGroup_2)
        self.idLabel.setGeometry(QtCore.QRect(7, 3, 20, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.idLabel.setFont(font)
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.id = QtGui.QLineEdit(self.attributeGroup_2)
        self.id.setGeometry(QtCore.QRect(40, 0, 150, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.id.setFont(font)
        self.id.setObjectName(_fromUtf8("id"))
        self.aimsunIdLabel_2 = QtGui.QLabel(self.attributeGroup_2)
        self.aimsunIdLabel_2.setGeometry(QtCore.QRect(209, 4, 68, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.aimsunIdLabel_2.setFont(font)
        self.aimsunIdLabel_2.setObjectName(_fromUtf8("aimsunIdLabel_2"))
        self.aimsunId_2 = QtGui.QLineEdit(self.attributeGroup_2)
        self.aimsunId_2.setGeometry(QtCore.QRect(290, 0, 161, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.aimsunId_2.setFont(font)
        self.aimsunId_2.setObjectName(_fromUtf8("aimsunId_2"))
        self.linkIdComboBox = QtGui.QComboBox(self.attributeGroup_2)
        self.linkIdComboBox.setGeometry(QtCore.QRect(-380, 150, 381, 27))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(12)
        self.linkIdComboBox.setFont(font)
        self.linkIdComboBox.setObjectName(_fromUtf8("linkIdComboBox"))
        self.tabWidget_2.addTab(self.tab_2, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.label = QtGui.QLabel(self.tab_4)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.laneID = QtGui.QLineEdit(self.tab_4)
        self.laneID.setGeometry(QtCore.QRect(150, 49, 201, 21))
        self.laneID.setObjectName(_fromUtf8("laneID"))
        self.laneidlabel = QtGui.QLabel(self.tab_4)
        self.laneidlabel.setGeometry(QtCore.QRect(20, 50, 121, 20))
        self.laneidlabel.setObjectName(_fromUtf8("laneidlabel"))
        self.fromSectionlabel = QtGui.QLabel(self.tab_4)
        self.fromSectionlabel.setGeometry(QtCore.QRect(50, 90, 81, 20))
        self.fromSectionlabel.setObjectName(_fromUtf8("fromSectionlabel"))
        self.fromSectioncomboBox = QtGui.QComboBox(self.tab_4)
        self.fromSectioncomboBox.setGeometry(QtCore.QRect(130, 90, 121, 22))
        self.fromSectioncomboBox.setObjectName(_fromUtf8("fromSectioncomboBox"))
        self.toSectionlabel = QtGui.QLabel(self.tab_4)
        self.toSectionlabel.setGeometry(QtCore.QRect(270, 90, 61, 20))
        self.toSectionlabel.setObjectName(_fromUtf8("toSectionlabel"))
        self.toSectioncomboBox = QtGui.QComboBox(self.tab_4)
        self.toSectioncomboBox.setGeometry(QtCore.QRect(340, 90, 121, 22))
        self.toSectioncomboBox.setObjectName(_fromUtf8("toSectioncomboBox"))
        self.fromLanelabel = QtGui.QLabel(self.tab_4)
        self.fromLanelabel.setGeometry(QtCore.QRect(50, 120, 81, 20))
        self.fromLanelabel.setObjectName(_fromUtf8("fromLanelabel"))
        self.toLanelabel = QtGui.QLabel(self.tab_4)
        self.toLanelabel.setGeometry(QtCore.QRect(270, 120, 61, 20))
        self.toLanelabel.setObjectName(_fromUtf8("toLanelabel"))
        self.toLanecomboBox = QtGui.QComboBox(self.tab_4)
        self.toLanecomboBox.setGeometry(QtCore.QRect(340, 120, 121, 22))
        self.toLanecomboBox.setObjectName(_fromUtf8("toLanecomboBox"))
        self.fromLanecomboBox = QtGui.QComboBox(self.tab_4)
        self.fromLanecomboBox.setGeometry(QtCore.QRect(130, 120, 121, 22))
        self.fromLanecomboBox.setObjectName(_fromUtf8("fromLanecomboBox"))
        self.laneConnectorTable = QtGui.QTableWidget(self.tab_4)
        self.laneConnectorTable.setGeometry(QtCore.QRect(30, 170, 431, 111))
        self.laneConnectorTable.setObjectName(_fromUtf8("laneConnectorTable"))
        self.laneConnectorTable.setColumnCount(0)
        self.laneConnectorTable.setRowCount(0)
        self.pushButton = QtGui.QPushButton(self.tab_4)
        self.pushButton.setGeometry(QtCore.QRect(364, 50, 91, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.tabWidget_2.addTab(self.tab_4, _fromUtf8(""))

        self.retranslateUi(Segment)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Segment)

    def retranslateUi(self, Segment):
        self.titleLabel.setText(_translate("Segment", "SEGMENT", None))
        self.linkIdLabel.setText(_translate("Segment", "LinkId*", None))
        self.actionButton.setText(_translate("Segment", "ADD", None))
        self.categorylabel.setText(_translate("Segment", "Category*", None))
        self.roadType.setItemText(0, _translate("Segment", "Default", None))
        self.roadType.setItemText(1, _translate("Segment", "Freeway", None))
        self.roadType.setItemText(2, _translate("Segment", "Ramp", None))
        self.roadType.setItemText(3, _translate("Segment", "Urban Road", None))
        self.maxSpeedLabel.setText(_translate("Segment", "MaxSpeed*", None))
        self.sequencenoLabel.setText(_translate("Segment", "SequenceNo*", None))
        self.lengthLabel.setText(_translate("Segment", "Capacity*", None))
        self.roadTypeLabel.setText(_translate("Segment", "Road Type*", None))
        self.idLabel.setText(_translate("Segment", "Id*", None))
        self.aimsunIdLabel_2.setText(_translate("Segment", "Aimsun Id*", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("Segment", "Section", None))
        self.label.setText(_translate("Segment", "Lane Connectors", None))
        self.laneidlabel.setText(_translate("Segment", "Lane Connector ID", None))
        self.fromSectionlabel.setText(_translate("Segment", "fromSection", None))
        self.toSectionlabel.setText(_translate("Segment", "toSection", None))
        self.fromLanelabel.setText(_translate("Segment", "fromLane", None))
        self.toLanelabel.setText(_translate("Segment", "toLane", None))
        self.pushButton.setText(_translate("Segment", "Add New", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("Segment", "Connectors", None))

