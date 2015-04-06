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
        self.laneconnectorlist = None


    def setLinkList(self, links):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        # for Link in root.iter('Link'):
        #     linkid = Link.find('linkID').text
        #     self.listLinks.append(linkid)

        self.listLinks = links
        self.linkidcomboBox.clear()
        for linkId in self.listLinks.iterkeys():
            self.linkidcomboBox.addItem(str(linkId))


        self.fromSectioncomboBox.clear()
        self.toSectioncomboBox.clear()
        self.fromLanecomboBox.clear()
        self.toLanecomboBox.clear()

        for segment in root.iter('Segment'):
            segmentID = segment.find('segmentID').text
            self.fromSectioncomboBox.addItem(str(segmentID))
            self.toSectioncomboBox.addItem(str(segmentID))

        for lane in root.iter('Lane'):
            laneID = lane.find('laneID').text
            self.fromLanecomboBox.addItem(str(laneID))
            self.toLanecomboBox.addItem(str(laneID))



    def setInfo(self, info):
        self.info = info
        global original_id

        if self.info is not None:
            linkId = int(self.info["linkId"])
            self.linkidcomboBox.setCurrentIndex(self.listLinks.keys().index(linkId))
            #self.linkName.setText(self.listLinks[linkId])                  linkname is in linkmanager
            self.actionButton.setText("SAVE")
            self.id.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.aimsunId.setText(str(self.info["aimsunId"]))
            self.sequenceno.setText(str(self.info["sequenceno"]))
            self.capacity.setText(str(self.info["capacity"]))
            self.maxSpeed.setText(str(self.info["maxSpeed"]))
            self.roadType.setEditText(str(self.self.info["roadType"]))
            self.category.setEditText(str(self.info["category"]))

            if self.info["connectors"] is not none:
                self.TurningGroupTable.setRowCount(10)
                self.TurningGroupTable.setColumnCount(4)
                TableHeader = ['ID','fromSection','toSection','fromLane','toLane']
                self.TurningGroupTable.setHorizontalHeaderLabels(TableHeader)
                #self.TurningGroupTable.verticalHeader().setVisible(false)
                self.TurningGroupTable.setSelectionBehavior(SelectRows)
                self.TurningGroupTable.setSelectionMode(SingleSelection)
                for connector in self.info["connectors"]:
                    ridx = self.info["connectors"].index(connector)
                    for cidx in range(0,4) :
                        self.TurningGroupTable.setItem(ridx,cidx,connector[cidx])
            #QtCore.QObject.connect(self.linkidcomboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.updateLinkName)
        else:
            self.addnewid()
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked(bool)'), self.addlaneconnector)
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)
        QtCore.QObject.connect(self.laneConnectorTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayconnector)

    # def updateLinkName(self, textLinkId):
    #     self.linkName.setText(self.listLinks[int(textLinkId)])


    def addnewid(self):
        seglist = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for laneconnector in root.iter('Connector'):
            if laneconnector is not None:
                self.laneconnectorlist.append(int(laneconnector.find('ID').text))

        if self.laneconnectorlist is not None:
            self.laneID.setText(str(max(self.laneconnectorlist)+1))

        for segment in root.iter('Segment'):
            seglist.append(int(segment.find('segmentID').text))

        self.id.setText(str(max(seglist)+1))

        return




    def addlaneconnector(self):

        laneconnectorid = self.laneID.text()
        if laneconnectorid.isdigit() is False:
            self.errorMessage.setText("Connector ID is invalid. It must be a number.")
            return

        self.laneconnectorlist.append([laneconnectorid, self.fromSectioncomboBox.currentText(), self.toSectioncomboBox.currentText(), self.fromLanecomboBox.text(), self.toLanecomboBox.currentText()])


        ridx = self.info["connectors"].length() + 1

        for cidx in range(0,4) :
            self.laneConnectorTable.setItem(ridx,cidx,self.laneconnectorlist[cidx])

        self.info["connectors"].append(self.laneconnectorlist)


    def displayconnector(self):

        ridx = self.laneConnectorTable.currentRow()
        self.laneID.setText(self.info["connector"][ridx][0])
        self.fromSectioncomboBox.setText(self.info["connector"][ridx][1])
        self.toSectioncomboBox.setText(self.info["connector"][ridx][2])
        self.fromLanecomboBox.setText(self.info["connector"][ridx][3])
        self.toLanecomboBox.setText(self.info["connector"][ridx][4])




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
        linkIdStr = self.linkidcomboBox.currentText()
        self.info["linkId"] = int(linkIdStr)

        id = self.id.text()
        if id.isdigit() is False:
            self.errorMessage.setText("id is invalid. It must be a number.")
            return

        if len(id) > 10 :                                                                                   # unsigned long in data structure
            self.errorMessage.setText("SegmentId is beyond range. Enter a shorter SegmentID.")
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

        # startNode = self.startNode.text()
        # if startNode.isdigit() is False:
        #     self.errorMessage.setText("startNode is invalid. It must be a number.")
        #     return
        #
        # endNode = self.endNode.text()
        # if endNode.isdigit() is False:
        #     self.errorMessage.setText("endNode is invalid. It must be a number.")
        #     return

        sequenceno = self.sequenceno.text()
        if sequenceno.isdigit() is False:
            self.errorMessage.setText("Sequence No is invalid. It must be a number.")
            return
        self.info["sequenceno"] = int(sequenceno)

        roadType = self.roadType.currentText()
        self.info["roadType"] = int(roadType)

        category = self.category.currentText()
        self.info["category"] = int(category)

        capacity = self.capacity.text()
        if capacity.isdigit() is False:
            self.errorMessage.setText("Capacity is invalid. It must be a number.")
            return
        self.info["capacity"] = int(capacity)



        # if id != original_id:
        #     for Segment in root.iter('Segment'):
        #         startingNode = Segment.find('startingNode').text
        #         endingNode = Segment.find('endingNode').text
        #         if startingNode == startNode and endingNode == endNode:
        #             self.errorMessage.setText("Segment with identical starting node/ending node pair exists. \nPlease enter different node IDs.")
        #             return
        #
        # nodeList = []
        #
        # for uniNode in root.iter('UniNode'):
        #     nodeList.append(uniNode.find('nodeID').text)
        #
        # for mulNode in root.iter('Intersection'):
        #     nodeList.append(mulNode.find('nodeID').text)
        #
        # if startNode not in nodeList or endNode not in nodeList:
        #     self.errorMessage.setText("The node ID doesn't exist. \nPlease enter different node ID.")
        #     return
        #
        # if startNode == endNode :
        #     self.errorMessage.setText("The start and end node are the same. \nPlease enter different node IDs.")
        #     return
        #
        # self.info["startingNode"] = int(startNode)
        # self.info["endingNode"] = int(endNode)

        maxSpeed = self.maxSpeed.text()
        if maxSpeed.isdigit() is False:
            self.errorMessage.setText("maxSpeed is invalid. It must be a number.")
            return
        self.info["maxSpeed"] = int(maxSpeed)




        # length = self.length.text()
        # if length.isdigit() is False:
        #     self.errorMessage.setText("length is invalid. It must be a number.")
        #     return
        # self.info["length"] = int(length)
        #
        # width = self.length.text()
        # if width.isdigit() is False:
        #     self.errorMessage.setText("width is invalid. It must be a number.")
        #     return
        # self.info["width"] = int(width)

        seglist.append(id)

        self.isModified = True

        self.accept()
