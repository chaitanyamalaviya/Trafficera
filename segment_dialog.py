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
        self.laneconnectorlist = []


    def setLinkList(self, links):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        # for Link in root.iter('Link'):
        #     linkid = Link.find('linkID').text
        #     self.listLinks.append(linkid)
        sortedList = []
        segList = []
        laneList = []
        self.listLinks = links
        self.linkidcomboBox.clear()
        for linkId in self.listLinks.iterkeys():
            sortedList.append(int(linkId))
        for id in sorted(sortedList):
            self.linkIdComboBox.addItem(str(id))

        self.fromSectioncomboBox.clear()
        self.toSectioncomboBox.clear()
        self.fromLanecomboBox.clear()
        self.toLanecomboBox.clear()

        for segment in root.iter('segment'):
            segList.append(int(segment.find('id').text))
        for id in sorted(segList):
            self.fromSectioncomboBox.addItem(str(id))
            self.toSectioncomboBox.addItem(str(id))

        for lane in root.iter('lane'):
            laneList.append(int(lane.find('id').text))
        for id in sorted(laneList):
            self.fromLanecomboBox.addItem(str(id))
            self.toLanecomboBox.addItem(str(id))


    def setInfo(self, info):
        self.info = info
        global original_id

        self.laneConnectorTable.setRowCount(0)
        self.laneConnectorTable.setColumnCount(5)
        TableHeader = ['ID','fromSegment','toSegment','fromLane','toLane']
        self.laneConnectorTable.setHorizontalHeaderLabels(TableHeader)
        self.laneConnectorTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.laneConnectorTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        if self.info is not None:
            linkId = int(self.info["linkId"])
            self.linkidcomboBox.setCurrentIndex(self.listLinks.keys().index(linkId))
            #self.linkName.setText(self.listLinks[linkId])                  linkname is in linkmanager
            self.actionButton.setText("SAVE")
            self.id.setText(str(self.info["id"]))
            original_id = self.info["id"]
            # self.aimsunId.setText(str(self.info["aimsunId"]))
            self.sequenceno.setText(str(self.info["sequence_no"]))
            self.capacity.setText(str(self.info["capacity"]))
            self.maxSpeed.setText(str(self.info["max_speed"]))
            self.Tags.setText(str(self.info["tags"]))
            # msgBox = QtGui.QMessageBox()
            # msgBox.setText(str(self.info["connectors"]))
            # msgBox.exec_()
            # return

            if self.info["connectors"]:

                for connector in self.info["connectors"]:
                    ridx = self.info["connectors"].index(connector)
                    self.laneConnectorTable.insertRow(ridx)
                    for cidx in range(5):
                        self.laneConnectorTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(connector[cidx]))
            #QtCore.QObject.connect(self.linkidcomboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.updateLinkName)
        else:
            self.addnewid()
            original_id = 0
            self.info = {}
            self.info["connectors"]=[]
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked(bool)'), self.addlaneconnector)
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)
        QtCore.QObject.connect(self.laneConnectorTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayconnector)
        QtCore.QObject.connect(self.delButton, QtCore.SIGNAL('clicked(bool)'),self.deleteconnector)

    # def updateLinkName(self, textLinkId):
    #     self.linkName.setText(self.listLinks[int(textLinkId)])

    def deleteconnector(self):
        ridx = self.laneConnectorTable.currentRow()
        self.info["connectors"].pop(ridx)
        self.laneConnectorTable.removeRow(ridx)
        if ridx == len(self.info["connectors"]):
            self.laneID.clear()
            self.fromSectioncomboBox.setCurrentIndex(0)
            self.toSectioncomboBox.setCurrentIndex(0)
            self.fromLanecomboBox.setCurrentIndex(0)
            self.toLanecomboBox.setCurrentIndex(0)
        else:
            self.laneID.setText(self.laneConnectorTable.item(ridx,0).text())
            self.fromSectioncomboBox.setCurrentIndex(self.fromSectioncomboBox.findText(self.laneConnectorTable.item(ridx,1).text()))
            self.toSectioncomboBox.setCurrentIndex(self.toSectioncomboBox.findText(self.laneConnectorTable.item(ridx,2).text()))
            self.fromLanecomboBox.setCurrentIndex(self.fromLanecomboBox.findText(self.laneConnectorTable.item(ridx,3).text()))
            self.toLanecomboBox.setCurrentIndex(self.toLanecomboBox.findText(self.laneConnectorTable.item(ridx,4).text()))




    def addnewid(self):
        seglist = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for laneconnector in root.iter('connector'):
            if laneconnector:
                self.laneconnectorlist.append(int(laneconnector.find('id').text))

        if self.laneconnectorlist:
            self.laneID.setText(str(max(self.laneconnectorlist)+1))
        else:
            self.laneID.setText(str(1))

        for segment in root.iter('segment'):
            seglist.append(int(segment.find('id').text))

        self.id.setText(str(max(seglist)+1))

        return




    def addlaneconnector(self):

        msgBox = QtGui.QMessageBox()

        laneconnectorid = self.laneID.text()
        if laneconnectorid.isdigit() is False:
            msgBox.setText("Connector ID is invalid. It must be a number.")
            msgBox.exec_()
            return
            # self.errorMessage.setText("Connector ID is invalid. It must be a number.")
            # return
        for conn in self.info["connectors"]:
            if conn[0]==laneconnectorid:
                msgBox.setText("Connector ID already exists. Please enter another ID.")
                msgBox.exec_()
                return
                # self.errorMessage.setText("Connector ID already exists. Please enter another ID.")
                # return
            if conn[3]==self.fromLanecomboBox.currentText() and conn[4]==self.toLanecomboBox.currentText():
                msgBox.setText("Connector with same fromLane and toLane already exists. Please enter different fromLane or toLane.")
                msgBox.exec_()
                return
                # self.errorMessage.setText("Connector with same fromLane and toLane already exists. Please enter different fromLane or toLane.")
                # return

        ridx = len(self.info["connectors"])
        self.info["connectors"].append([laneconnectorid, self.fromSectioncomboBox.currentText(), self.toSectioncomboBox.currentText(), self.fromLanecomboBox.currentText(), self.toLanecomboBox.currentText()])

        self.laneConnectorTable.insertRow(ridx)
        for cidx in range(5):
            self.laneConnectorTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(self.info["connectors"][ridx][cidx]))


    def displayconnector(self):

        ridx = self.laneConnectorTable.currentRow()
        if ridx>=0:
            self.laneID.setText(self.laneConnectorTable.item(self.laneConnectorTable.currentRow(),0).text())
            self.fromSectioncomboBox.setCurrentIndex(self.fromSectioncomboBox.findText(self.laneConnectorTable.item(self.laneConnectorTable.currentRow(),1).text()))
            self.toSectioncomboBox.setCurrentIndex(self.toSectioncomboBox.findText(self.laneConnectorTable.item(self.laneConnectorTable.currentRow(),2).text()))
            self.fromLanecomboBox.setCurrentIndex(self.fromLanecomboBox.findText(self.laneConnectorTable.item(self.laneConnectorTable.currentRow(),3).text()))
            self.toLanecomboBox.setCurrentIndex(self.toLanecomboBox.findText(self.laneConnectorTable.item(self.laneConnectorTable.currentRow(),4).text()))



    def update(self):
        global original_id
        #self.errorMessage.setText("")
        msgBox = QtGui.QMessageBox()
        seglist = []

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for segment in root.iter('segment'):
            segmentid = segment.find('id').text
            seglist.append(segmentid)


        # get linkid
        linkIdStr = self.linkidcomboBox.currentText()
        self.info["linkId"] = int(linkIdStr)

        id = self.id.text()
        if id.isdigit() is False:
            msgBox.setText("id is invalid. It must be a number.")
            msgBox.exec_()
            return


        elif len(id) > 10:
            msgBox.setText("SegmentId is beyond range. Enter a shorter SegmentID.")
            msgBox.exec_()
            return                                                                         # unsigned long in data structure

        elif id in seglist and id != original_id:
            msgBox.setText("Segment ID exists. Please enter another ID.")
            msgBox.exec_()
            return

        self.info["id"] = int(id)

        sequence_no = self.sequenceno.text()
        if sequence_no.isdigit() is False:
            self.errorMessage.setText("Sequence No is invalid. It must be a number.")
            return

        elif len(sequence_no) > 3:
            msgBox.setText("SequenceNo is beyond range. Enter a shorter sequence number.")
            msgBox.exec_()
            return

        self.info["sequence_no"] = int(sequence_no)


        tags = self.Tags.text()
        self.info["tags"] = tags

        capacity = self.capacity.text()
        if capacity.isdigit() is False:
            self.errorMessage.setText("Capacity is invalid. It must be a number.")
            return

        elif len(capacity) > 3:
            msgBox.setText("Capacity is beyond range. Enter a shorter value for capacity.")
            msgBox.exec_()
            return
        self.info["capacity"] = int(capacity)



        # if id != original_id:
        #     for segment in root.iter('segment'):
        #         startingNode = segment.find('startingNode').text
        #         endingNode = segment.find('endingNode').text
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

        elif len(maxSpeed) > 3:
            msgBox.setText("maxSpeed is beyond range. Enter a shorter value for speed.")
            msgBox.exec_()
            return
        self.info["max_speed"] = int(maxSpeed)




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
