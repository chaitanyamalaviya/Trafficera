# -*- coding: utf-8 -*-
"""
/***************************************************************************
 iSimGisDialog
                                 A QGIS plugin
 iSim converter
                             -------------------
        begin                : 2015-03-30
        copyright            : (C) 2015 by chaitanyamalaviya
        email                : chaitanyamalaviya@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtCore, QtGui
from ui_linkmanager import Ui_LinkManager
import os
# create the dialog for zoom to point


class LinkManagerDialog(QtGui.QDialog, Ui_LinkManager):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.info = None
        self.listLinks = None
        self.isModified = False



    def setLinkList(self, links):
        self.listLinks = links
        self.linkIdComboBox.clear()
        self.linkIdComboBox.addItem("add new link")
        for linkId in links.iterkeys():
            self.linkIdComboBox.addItem(str(linkId))
        self.linkIdComboBox.setCurrentIndex(0)
        self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)
        QtCore.QObject.connect(self.linkIdComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.updateLinkName)

    def updateLinkName(self, textLinkId):
        if textLinkId == "add new link":
            self.actionButton.setText("ADD")
            self.id.setText("")
            self.roadName.setText("")
            self.startNode.setText("")
            self.endNode.setText("")
            self.tagsLink.setPlainText("")
        else:
            linkId = int(textLinkId)
            self.id.setText(textLinkId)
            self.roadName.setText(self.listLinks[linkId][1])
            self.startNode.setText(str(self.listLinks[linkId][2]))
            self.endNode.setText(str(self.listLinks[linkId][3]))
            self.tagsLink.setPlainText(str(self.listLinks[linkId][4]))
            self.actionButton.setText("SAVE")

    def update(self):
        self.errorMessage.setText("")
        self.info = {}
        msgBox = QtGui.QMessageBox()
        oldLinkId = 0
        #get linkid
        linkIdStr = self.linkIdComboBox.currentText()
        if linkIdStr != "add new link":
            oldLinkId = int(linkIdStr)
        self.info["oldId"] = oldLinkId   

        id = self.id.text()
        if id.isdigit() is False or int(id) < 1:
            msgBox.setText("id is invalid. It must be a positive number.")
            msgBox.exec_()
            return

        self.info["id"] = int(id)
        if self.info["id"] < 1 or self.info["id"] != oldLinkId:
            if self.info["id"] in self.listLinks:
                msgBox.setText("The linkID already exists. Please enter a new linkID")
                msgBox.exec_()
                return

        roadName = self.roadName.text()
        if roadName == "":
            msgBox.setText("roadName can not be empty.")
            msgBox.exec_()
            return

        self.info["roadName"] = roadName

        startNode = self.startNode.text()
        if startNode.isdigit() is False:
            msgBox.setText("startNode is invalid. It must be a number.")
            msgBox.exec_()
            return

        self.info["startingNode"] = int(startNode)       

        endNode = self.endNode.text()
        if endNode.isdigit() is False:
            msgBox.setText("endNode is invalid. It must be a number.")
            msgBox.exec_()
            return

        self.info["endingNode"] = int(endNode)


        self.info["roadType"] = self.roadType.currentText()

        self.info["category"] = self.category.currentText()

        self.info["tags"] = self.tagsLink.toPlainText()

        self.isModified = True
        self.accept()
