# -*- coding: utf-8 -*-
"""
/***************************************************************************
 iSimGisDialog
                                 A QGIS plugin
 iSim converter
                             -------------------
        begin                : 2014-02-03
        copyright            : (C) 2014 by nhudinhtuan
        email                : nhudinhtuan@gmail.com
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
from ui_segment import Ui_Segment
import os
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *
# create the dialog for zoom to point


class SegmentDialog(QtGui.QDialog, Ui_Segment):

    original_id = 0

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
        for linkId in links.iterkeys():
            self.linkIdComboBox.addItem(str(linkId))

    def setInfo(self, info):
        self.info = info
        global original_id
        if self.info is not None:
            linkId = int(self.info["linkId"])
            self.linkIdComboBox.setCurrentIndex(self.listLinks.keys().index(linkId))
            self.linkName.setText(self.listLinks[linkId])
            self.actionButton.setText("SAVE")
            self.id.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.aimsunId.setText(str(self.info["aimsunId"]))
            self.startNode.setText(str(self.info["startingNode"]))
            self.endNode.setText(str(self.info["endingNode"]))
            self.maxSpeed.setText(str(self.info["maxSpeed"]))
            self.length.setText(str(self.info["length"]))
            self.width.setText(str(self.info["width"]))
            QtCore.QObject.connect(self.linkIdComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'),
                                   self.updateLinkName)
        else:
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def updateLinkName(self, textLinkId):
        self.linkName.setText(self.listLinks[int(textLinkId)])

    def update(self):
        global original_id
        self.errorMessage.setText("")
        self.info = {}
        seglist = []

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for Segment in root.iter('Segment'):
            segmentid = Segment.find('segmentID').text
            seglist.append(segmentid)


        # get linkid
        linkIdStr = self.linkIdComboBox.currentText()
        self.info["linkId"] = int(linkIdStr)

        id = self.id.text()
        if id.isdigit() is False:
            self.errorMessage.setText("id is invalid. It must be a number.")
            return

        if id in seglist and id != original_id:
            self.errorMessage.setText("Segment ID exists. Please enter another ID.")
            return

        self.info["id"] = int(id)

        aimsunId = self.aimsunId.text()
        if aimsunId.isdigit() is False:
            self.errorMessage.setText("aimsunId is invalid. It must be a number.")
            return
        self.info["aimsunId"] = int(aimsunId)

        startNode = self.startNode.text()
        if startNode.isdigit() is False:
            self.errorMessage.setText("startNode is invalid. It must be a number.")
            return

        endNode = self.endNode.text()
        if endNode.isdigit() is False:
            self.errorMessage.setText("endNode is invalid. It must be a number.")
            return

        if id != original_id:
            for Segment in root.iter('Segment'):
                startingNode = Segment.find('startingNode').text
                endingNode = Segment.find('endingNode').text
                if startingNode == startNode and endingNode == endNode:
                    self.errorMessage.setText("Segment with identical starting node/ending node pair exists. \nPlease enter different node IDs.")
                    return

        nodeList = []

        for uniNode in root.iter('UniNode'):
            nodeList.append(uniNode.find('nodeID').text)

        for mulNode in root.iter('Intersection'):
            nodeList.append(mulNode.find('nodeID').text)

        if startNode not in nodeList or endNode not in nodeList:
            self.errorMessage.setText("The node ID doesn't exist. \nPlease enter different node ID.")
            return

        if startNode == endNode :
            self.errorMessage.setText("The start and end node are the same. \nPlease enter different node IDs.")
            return

        self.info["startingNode"] = int(startNode)
        self.info["endingNode"] = int(endNode)

        maxSpeed = self.maxSpeed.text()
        if maxSpeed.isdigit() is False:
            self.errorMessage.setText("maxSpeed is invalid. It must be a number.")
            return
        self.info["maxSpeed"] = int(maxSpeed)

        length = self.length.text()
        if length.isdigit() is False:
            self.errorMessage.setText("length is invalid. It must be a number.")
            return
        self.info["length"] = int(length)

        width = self.length.text()
        if width.isdigit() is False:
            self.errorMessage.setText("width is invalid. It must be a number.")
            return
        self.info["width"] = int(width)

        seglist.append(id)

        self.isModified = True

        self.accept()
