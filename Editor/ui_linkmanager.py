# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_linkmanager.ui'
#
# Created: Thu May  8 12:47:34 2014
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

class Ui_LinkManager(object):
    def setupUi(self, LinkManager):
        LinkManager.setObjectName(_fromUtf8("LinkManager"))
        LinkManager.setEnabled(True)
        LinkManager.resize(481, 233)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(13)
        LinkManager.setFont(font)
        LinkManager.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        LinkManager.setWindowTitle(_fromUtf8("iSimGis Converter"))
        LinkManager.setWindowOpacity(4.0)
        LinkManager.setToolTip(_fromUtf8(""))
        LinkManager.setStatusTip(_fromUtf8(""))
        LinkManager.setSizeGripEnabled(False)
        self.gridLayout_3 = QtGui.QGridLayout(LinkManager)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(LinkManager)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.linkGroupBox = QtGui.QGroupBox(LinkManager)
        self.linkGroupBox.setObjectName(_fromUtf8("linkGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.linkGroupBox)
        self.gridLayout.setMargin(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.linkIdLabel = QtGui.QLabel(self.linkGroupBox)
        self.linkIdLabel.setObjectName(_fromUtf8("linkIdLabel"))
        self.gridLayout.addWidget(self.linkIdLabel, 0, 0, 1, 1)
        self.linkIdComboBox = QtGui.QComboBox(self.linkGroupBox)
        self.linkIdComboBox.setObjectName(_fromUtf8("linkIdComboBox"))
        self.gridLayout.addWidget(self.linkIdComboBox, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.linkGroupBox)
        self.attributeGroup = QtGui.QGroupBox(LinkManager)
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
        self.roadNameLabel = QtGui.QLabel(self.attributeGroup)
        self.roadNameLabel.setObjectName(_fromUtf8("roadNameLabel"))
        self.horizontalLayout.addWidget(self.roadNameLabel)
        self.roadName = QtGui.QLineEdit(self.attributeGroup)
        self.roadName.setObjectName(_fromUtf8("roadName"))
        self.horizontalLayout.addWidget(self.roadName)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.startNodeLabel = QtGui.QLabel(self.attributeGroup)
        self.startNodeLabel.setObjectName(_fromUtf8("startNodeLabel"))
        self.horizontalLayout_2.addWidget(self.startNodeLabel)
        self.startNode = QtGui.QLineEdit(self.attributeGroup)
        self.startNode.setObjectName(_fromUtf8("startNode"))
        self.horizontalLayout_2.addWidget(self.startNode)
        self.endNodeLabel = QtGui.QLabel(self.attributeGroup)
        self.endNodeLabel.setObjectName(_fromUtf8("endNodeLabel"))
        self.horizontalLayout_2.addWidget(self.endNodeLabel)
        self.endNode = QtGui.QLineEdit(self.attributeGroup)
        self.endNode.setObjectName(_fromUtf8("endNode"))
        self.horizontalLayout_2.addWidget(self.endNode)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.attributeGroup)
        self.splitter = QtGui.QSplitter(LinkManager)
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

        self.retranslateUi(LinkManager)
        QtCore.QMetaObject.connectSlotsByName(LinkManager)

    def retranslateUi(self, LinkManager):
        self.titleLabel.setText(_translate("LinkManager", "LINK MANAGER", None))
        self.linkGroupBox.setTitle(_translate("LinkManager", "Links", None))
        self.linkIdLabel.setText(_translate("LinkManager", "LinkId*", None))
        self.idLabel.setText(_translate("LinkManager", "LinkId*", None))
        self.roadNameLabel.setText(_translate("LinkManager", "roadName*", None))
        self.startNodeLabel.setText(_translate("LinkManager", "StartNode*", None))
        self.endNodeLabel.setText(_translate("LinkManager", "EndNode*", None))
        self.actionButton.setText(_translate("LinkManager", "ADD", None))

