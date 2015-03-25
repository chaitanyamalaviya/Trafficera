# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_uninode.ui'
#
# Created: Mon Mar 23 17:00:39 2015
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

class Ui_UniNode(object):
    def setupUi(self, UniNode):
        UniNode.setObjectName(_fromUtf8("UniNode"))
        UniNode.setEnabled(True)
        UniNode.resize(511, 439)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        UniNode.setFont(font)
        UniNode.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        UniNode.setWindowTitle(_fromUtf8("iSimGis Converter"))
        UniNode.setWindowOpacity(4.0)
        UniNode.setToolTip(_fromUtf8(""))
        UniNode.setStatusTip(_fromUtf8(""))
        UniNode.setSizeGripEnabled(False)
        self.gridLayout_4 = QtGui.QGridLayout(UniNode)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.titleLabel = QtGui.QLabel(UniNode)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout_3.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.attributeGroup = QtGui.QGroupBox(UniNode)
        self.attributeGroup.setTitle(_fromUtf8(""))
        self.attributeGroup.setObjectName(_fromUtf8("attributeGroup"))
        self.gridLayout = QtGui.QGridLayout(self.attributeGroup)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.firstPairLabel = QtGui.QLabel(self.attributeGroup)
        self.firstPairLabel.setObjectName(_fromUtf8("firstPairLabel"))
        self.horizontalLayout_2.addWidget(self.firstPairLabel)
        self.firstPair = QtGui.QLineEdit(self.attributeGroup)
        self.firstPair.setObjectName(_fromUtf8("firstPair"))
        self.horizontalLayout_2.addWidget(self.firstPair)
        self.secondPairLabel = QtGui.QLabel(self.attributeGroup)
        self.secondPairLabel.setObjectName(_fromUtf8("secondPairLabel"))
        self.horizontalLayout_2.addWidget(self.secondPairLabel)
        self.secondPair = QtGui.QLineEdit(self.attributeGroup)
        self.secondPair.setObjectName(_fromUtf8("secondPair"))
        self.horizontalLayout_2.addWidget(self.secondPair)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.attributeGroup, 1, 0, 1, 1)
        self.connectorGroup = QtGui.QGroupBox(UniNode)
        self.connectorGroup.setObjectName(_fromUtf8("connectorGroup"))
        self.gridLayout_2 = QtGui.QGridLayout(self.connectorGroup)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.connectorEdit = QtGui.QTextEdit(self.connectorGroup)
        self.connectorEdit.setObjectName(_fromUtf8("connectorEdit"))
        self.gridLayout_2.addWidget(self.connectorEdit, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.connectorGroup, 2, 0, 1, 1)
        self.splitter = QtGui.QSplitter(UniNode)
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
        self.gridLayout_3.addWidget(self.splitter, 3, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(UniNode)
        QtCore.QMetaObject.connectSlotsByName(UniNode)

    def retranslateUi(self, UniNode):
        self.titleLabel.setText(_translate("UniNode", "UNINODE", None))
        self.nodeIdLabel.setText(_translate("UniNode", "Node Id*", None))
        self.aimsunIdLabel.setText(_translate("UniNode", "Aimsun Id*", None))
        self.firstPairLabel.setText(_translate("UniNode", "FirstPair ", None))
        self.secondPairLabel.setText(_translate("UniNode", "SecondPair", None))
        self.connectorGroup.setTitle(_translate("UniNode", "Connectors", None))
        self.actionButton.setText(_translate("UniNode", "ADD", None))

