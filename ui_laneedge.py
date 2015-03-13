# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_laneedge.ui'
#
# Created: Thu May  8 12:51:40 2014
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

class Ui_LaneEdge(object):
    def setupUi(self, LaneEdge):
        LaneEdge.setObjectName(_fromUtf8("LaneEdge"))
        LaneEdge.setEnabled(True)
        LaneEdge.resize(450, 194)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        LaneEdge.setFont(font)
        LaneEdge.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        LaneEdge.setWindowTitle(_fromUtf8("iSimGis Converter"))
        LaneEdge.setWindowOpacity(4.0)
        LaneEdge.setToolTip(_fromUtf8(""))
        LaneEdge.setStatusTip(_fromUtf8(""))
        LaneEdge.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(LaneEdge)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(LaneEdge)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.SegmentGroupBox = QtGui.QGroupBox(LaneEdge)
        self.SegmentGroupBox.setObjectName(_fromUtf8("SegmentGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.SegmentGroupBox)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.segmentIdLabel = QtGui.QLabel(self.SegmentGroupBox)
        self.segmentIdLabel.setMaximumSize(QtCore.QSize(100, 100))
        self.segmentIdLabel.setObjectName(_fromUtf8("segmentIdLabel"))
        self.gridLayout.addWidget(self.segmentIdLabel, 0, 0, 1, 1)
        self.segmentId = QtGui.QLabel(self.SegmentGroupBox)
        self.segmentId.setText(_fromUtf8(""))
        self.segmentId.setObjectName(_fromUtf8("segmentId"))
        self.gridLayout.addWidget(self.segmentId, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.SegmentGroupBox)
        self.attributeGroup = QtGui.QGroupBox(LaneEdge)
        self.attributeGroup.setTitle(_fromUtf8(""))
        self.attributeGroup.setObjectName(_fromUtf8("attributeGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.attributeGroup)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.laneNumberLabel = QtGui.QLabel(self.attributeGroup)
        self.laneNumberLabel.setObjectName(_fromUtf8("laneNumberLabel"))
        self.gridLayout_2.addWidget(self.laneNumberLabel, 0, 0, 1, 1)
        self.laneNumber = QtGui.QLineEdit(self.attributeGroup)
        self.laneNumber.setObjectName(_fromUtf8("laneNumber"))
        self.gridLayout_2.addWidget(self.laneNumber, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.attributeGroup)
        self.splitter = QtGui.QSplitter(LaneEdge)
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

        self.retranslateUi(LaneEdge)
        QtCore.QMetaObject.connectSlotsByName(LaneEdge)

    def retranslateUi(self, LaneEdge):
        self.titleLabel.setText(_translate("LaneEdge", "Lane Edge", None))
        self.SegmentGroupBox.setTitle(_translate("LaneEdge", "Segment", None))
        self.segmentIdLabel.setText(_translate("LaneEdge", "SegmentId*", None))
        self.laneNumberLabel.setText(_translate("LaneEdge", "lane number*", None))
        self.actionButton.setText(_translate("LaneEdge", "ADD", None))

