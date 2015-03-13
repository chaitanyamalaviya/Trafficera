# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_multinode.ui'
#
# Created: Tue Mar 10 15:55:09 2015
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

class Ui_MultiNode(object):
    def setupUi(self, MultiNode):
        MultiNode.setObjectName(_fromUtf8("MultiNode"))
        MultiNode.setEnabled(True)
        MultiNode.resize(479, 462)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        MultiNode.setFont(font)
        MultiNode.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MultiNode.setWindowTitle(_fromUtf8("iSimGis Converter"))
        MultiNode.setWindowOpacity(4.0)
        MultiNode.setToolTip(_fromUtf8(""))
        MultiNode.setStatusTip(_fromUtf8(""))
        MultiNode.setSizeGripEnabled(False)
        self.gridLayout_4 = QtGui.QGridLayout(MultiNode)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(MultiNode)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.attributeGroup = QtGui.QGroupBox(MultiNode)
        self.attributeGroup.setTitle(_fromUtf8(""))
        self.attributeGroup.setObjectName(_fromUtf8("attributeGroup"))
        self.gridLayout = QtGui.QGridLayout(self.attributeGroup)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.nodeIdLabel = QtGui.QLabel(self.attributeGroup)
        self.nodeIdLabel.setObjectName(_fromUtf8("nodeIdLabel"))
        self.horizontalLayout.addWidget(self.nodeIdLabel)
        self.nodeId = QtGui.QLineEdit(self.attributeGroup)
        self.nodeId.setObjectName(_fromUtf8("nodeId"))
        self.horizontalLayout.addWidget(self.nodeId)
        self.aimsunIdLabel = QtGui.QLabel(self.attributeGroup)
        self.aimsunIdLabel.setObjectName(_fromUtf8("aimsunIdLabel"))
        self.horizontalLayout.addWidget(self.aimsunIdLabel)
        self.aimsunId = QtGui.QLineEdit(self.attributeGroup)
        self.aimsunId.setObjectName(_fromUtf8("aimsunId"))
        self.horizontalLayout.addWidget(self.aimsunId)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.attributeGroup)
        self.generateid = QtGui.QPushButton(MultiNode)
        self.generateid.setObjectName(_fromUtf8("generateid"))
        self.verticalLayout.addWidget(self.generateid)
        self.roadSegmentGroup = QtGui.QGroupBox(MultiNode)
        self.roadSegmentGroup.setObjectName(_fromUtf8("roadSegmentGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.roadSegmentGroup)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.segmentIDcomboBox = QtGui.QComboBox(self.roadSegmentGroup)
        self.segmentIDcomboBox.setObjectName(_fromUtf8("segmentIDcomboBox"))
        self.gridLayout_2.addWidget(self.segmentIDcomboBox, 0, 0, 1, 1)
        self.roadSegmentEdit = QtGui.QTextEdit(self.roadSegmentGroup)
        self.roadSegmentEdit.setObjectName(_fromUtf8("roadSegmentEdit"))
        self.gridLayout_2.addWidget(self.roadSegmentEdit, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.roadSegmentGroup)
        self.mulConnectorGroup = QtGui.QGroupBox(MultiNode)
        self.mulConnectorGroup.setObjectName(_fromUtf8("mulConnectorGroup"))
        self.gridLayout_3 = QtGui.QGridLayout(self.mulConnectorGroup)
        self.gridLayout_3.setMargin(5)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.mulConnectorEdit = QtGui.QTextEdit(self.mulConnectorGroup)
        self.mulConnectorEdit.setObjectName(_fromUtf8("mulConnectorEdit"))
        self.gridLayout_3.addWidget(self.mulConnectorEdit, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.mulConnectorGroup)
        self.splitter = QtGui.QSplitter(MultiNode)
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
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MultiNode)
        QtCore.QMetaObject.connectSlotsByName(MultiNode)

    def retranslateUi(self, MultiNode):
        self.titleLabel.setText(_translate("MultiNode", "MULTINODE", None))
        self.nodeIdLabel.setText(_translate("MultiNode", "Node Id*", None))
        self.aimsunIdLabel.setText(_translate("MultiNode", "Aimsun Id*", None))
        self.generateid.setText(_translate("MultiNode", "Auto Generate Node ID", None))
        self.roadSegmentGroup.setTitle(_translate("MultiNode", "RoadSegmentsAt", None))
        self.mulConnectorGroup.setTitle(_translate("MultiNode", "MultiConnectors", None))
        self.actionButton.setText(_translate("MultiNode", "ADD", None))

