# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_crossing.ui'
#
# Created: Thu May  8 12:58:57 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Crossing(object):
    def setupUi(self, Crossing):
        Crossing.setObjectName(_fromUtf8("Crossing"))
        Crossing.setEnabled(True)
        Crossing.resize(483, 196)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        Crossing.setFont(font)
        Crossing.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Crossing.setWindowTitle(_fromUtf8("iSimGis Converter"))
        Crossing.setWindowOpacity(4.0)
        Crossing.setToolTip(_fromUtf8(""))
        Crossing.setStatusTip(_fromUtf8(""))
        Crossing.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(Crossing)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(Crossing)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.SegmentGroupBox = QtGui.QGroupBox(Crossing)
        self.SegmentGroupBox.setObjectName(_fromUtf8("SegmentGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.SegmentGroupBox)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.segmentIdLabel = QtGui.QLabel(self.SegmentGroupBox)
        self.segmentIdLabel.setObjectName(_fromUtf8("segmentIdLabel"))
        self.gridLayout.addWidget(self.segmentIdLabel, 0, 0, 1, 1)
        self.segmentId = QtGui.QLabel(self.SegmentGroupBox)
        self.segmentId.setText(_fromUtf8(""))
        self.segmentId.setObjectName(_fromUtf8("segmentId"))
        self.gridLayout.addWidget(self.segmentId, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.SegmentGroupBox)
        self.attributeGroup = QtGui.QGroupBox(Crossing)
        self.attributeGroup.setTitle(_fromUtf8(""))
        self.attributeGroup.setObjectName(_fromUtf8("attributeGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.attributeGroup)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.idLabel = QtGui.QLabel(self.attributeGroup)
        self.idLabel.setObjectName(_fromUtf8("idLabel"))
        self.horizontalLayout.addWidget(self.idLabel)
        self.id = QtGui.QLineEdit(self.attributeGroup)
        self.id.setObjectName(_fromUtf8("id"))
        self.horizontalLayout.addWidget(self.id)
        self.OffsetLabel = QtGui.QLabel(self.attributeGroup)
        self.OffsetLabel.setObjectName(_fromUtf8("OffsetLabel"))
        self.horizontalLayout.addWidget(self.OffsetLabel)
        self.offset = QtGui.QLineEdit(self.attributeGroup)
        self.offset.setObjectName(_fromUtf8("offset"))
        self.horizontalLayout.addWidget(self.offset)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.attributeGroup)
        self.splitter = QtGui.QSplitter(Crossing)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.errorMessage = QtGui.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setItalic(True)
        self.errorMessage.setFont(font)
        self.errorMessage.setStyleSheet(_fromUtf8("color: rgb(255, 20, 27)"))
        self.errorMessage.setText(_fromUtf8(""))
        self.errorMessage.setObjectName(_fromUtf8("errorMessage"))
        self.actionButton = QtGui.QPushButton(self.splitter)
        self.actionButton.setMaximumSize(QtCore.QSize(100, 100))
        self.actionButton.setObjectName(_fromUtf8("actionButton"))
        self.verticalLayout.addWidget(self.splitter)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Crossing)
        QtCore.QMetaObject.connectSlotsByName(Crossing)

    def retranslateUi(self, Crossing):
        self.titleLabel.setText(_translate("Crossing", "CROSSING", None))
        self.SegmentGroupBox.setTitle(_translate("Crossing", "Segment", None))
        self.segmentIdLabel.setText(_translate("Crossing", "SegmentId*", None))
        self.idLabel.setText(_translate("Crossing", "Id*", None))
        self.OffsetLabel.setText(_translate("Crossing", "Offset*", None))
        self.actionButton.setText(_translate("Crossing", "ADD", None))

