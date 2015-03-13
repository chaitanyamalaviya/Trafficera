# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_busstop.ui'
#
# Created: Thu May  8 13:07:52 2014
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

class Ui_Busstop(object):
    def setupUi(self, Busstop):
        Busstop.setObjectName(_fromUtf8("Busstop"))
        Busstop.setEnabled(True)
        Busstop.resize(512, 296)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        Busstop.setFont(font)
        Busstop.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Busstop.setWindowTitle(_fromUtf8("iSimGis Converter"))
        Busstop.setWindowOpacity(4.0)
        Busstop.setToolTip(_fromUtf8(""))
        Busstop.setStatusTip(_fromUtf8(""))
        Busstop.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(Busstop)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(Busstop)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.SegmentGroupBox = QtGui.QGroupBox(Busstop)
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
        self.attributeGroup = QtGui.QGroupBox(Busstop)
        self.attributeGroup.setTitle(_fromUtf8(""))
        self.attributeGroup.setObjectName(_fromUtf8("attributeGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.attributeGroup)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.busCapacityLabel = QtGui.QLabel(self.attributeGroup)
        self.busCapacityLabel.setObjectName(_fromUtf8("busCapacityLabel"))
        self.horizontalLayout_2.addWidget(self.busCapacityLabel)
        self.busCapacity = QtGui.QLineEdit(self.attributeGroup)
        self.busCapacity.setObjectName(_fromUtf8("busCapacity"))
        self.horizontalLayout_2.addWidget(self.busCapacity)
        self.busstopNoLabel = QtGui.QLabel(self.attributeGroup)
        self.busstopNoLabel.setObjectName(_fromUtf8("busstopNoLabel"))
        self.horizontalLayout_2.addWidget(self.busstopNoLabel)
        self.busstopNo = QtGui.QLineEdit(self.attributeGroup)
        self.busstopNo.setObjectName(_fromUtf8("busstopNo"))
        self.horizontalLayout_2.addWidget(self.busstopNo)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.isTerminal = QtGui.QCheckBox(self.attributeGroup)
        self.isTerminal.setObjectName(_fromUtf8("isTerminal"))
        self.horizontalLayout_3.addWidget(self.isTerminal)
        self.isBay = QtGui.QCheckBox(self.attributeGroup)
        self.isBay.setObjectName(_fromUtf8("isBay"))
        self.horizontalLayout_3.addWidget(self.isBay)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.hasShelter = QtGui.QCheckBox(self.attributeGroup)
        self.hasShelter.setObjectName(_fromUtf8("hasShelter"))
        self.gridLayout_2.addWidget(self.hasShelter, 3, 0, 1, 1)
        self.verticalLayout.addWidget(self.attributeGroup)
        self.splitter = QtGui.QSplitter(Busstop)
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

        self.retranslateUi(Busstop)
        QtCore.QMetaObject.connectSlotsByName(Busstop)

    def retranslateUi(self, Busstop):

        #handles the translation of the string properties of the form

        self.titleLabel.setText(_translate("Busstop", "BUS STOP", None))
        self.SegmentGroupBox.setTitle(_translate("Busstop", "Segment", None))
        self.segmentIdLabel.setText(_translate("Busstop", "SegmentId*", None))
        self.idLabel.setText(_translate("Busstop", "Id*", None))
        self.OffsetLabel.setText(_translate("Busstop", "Offset*", None))
        self.busCapacityLabel.setText(_translate("Busstop", "BusCapacity*", None))
        self.busstopNoLabel.setText(_translate("Busstop", "BusStopNo*", None))
        self.isTerminal.setText(_translate("Busstop", "Terminal", None))
        self.isBay.setText(_translate("Busstop", "Bay", None))
        self.hasShelter.setText(_translate("Busstop", "Has Shelter", None))
        self.actionButton.setText(_translate("Busstop", "ADD", None))