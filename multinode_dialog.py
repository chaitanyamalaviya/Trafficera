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
from ui_multinode import Ui_MultiNode
from qgis.core import *
import os
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *
# create the dialog for zoom to point


class MultiNodeDialog(QtGui.QDialog, Ui_MultiNode):

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
        self.isModified = False
        self.listSegments = None


    def setInfo(self, info):
        self.info = info
        global original_id
        self.setSegmentlist()
        if self.info is not None:               # updating existing element
            self.isModified = True
            self.actionButton.setText("SAVE")
            self.nodeId.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.aimsunId.setText(str(self.info["aimsunId"]))
            # if self.info["roadSegmentsAt"] is not None:
            #     roadSegmentsAtStr = "\n".join(self.info["roadSegmentsAt"])
            #     self.roadSegmentEdit.setPlainText(roadSegmentsAtStr)
            # if self.info["connectors"] is not None:
            #     connectorStr = []
            #     for multiconnector in self.info["connectors"]:
            #         tempStr = "%s\n%s"%(str(multiconnector[0]), "\n".join(multiconnector[1]))
            #         connectorStr.append(tempStr)
            #     self.mulConnectorEdit.setPlainText("\n".join(connectorStr))
        else:
            self.actionButton.setText("ADD")

        QtCore.QObject.connect(self.generateid, QtCore.SIGNAL('clicked(bool)'), self.addnewid)
        QtCore.QObject.connect(self.segmentIDcomboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.addSegment)
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def addSegment(self):
        roadSegmentsAtStr = str(self.segmentIDcomboBox.currentText())
        self.roadSegmentEdit.append(roadSegmentsAtStr)


    def setSegmentlist(self):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for seg in root.iter('Segment'):
            self.segmentIDcomboBox.addItem(seg.find('segmentID').text)



    def addnewid(self):
        nodeList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for uniNode in root.iter('UniNode'):
            nodeList.append(int(uniNode.find('nodeID').text))

        for mulNode in root.iter('Intersection'):
            nodeList.append(int(mulNode.find('nodeID').text))

        self.nodeId.setText(str(max(nodeList)+1))
        return


    def parseRoadSegments(self, text):
        result = []
        segments = text.split("\n")
        for segmentStr in segments:
            if segmentStr != "":
                result.append(segmentStr)
        return result

    def parseMultiConnectors(self, text):
        ''' Format
        RoadSegment
        laneFrom,laneTo
        laneFrom,laneTo
        '''
        result = []
        lines = text.split("\n")
        currentSegment = None
        currentConnectors = []
        for line in lines:
            parts = line.split(",")

            if len(parts) == 1:
                if currentSegment is not None and len(currentConnectors) > 0:
                    result.append([currentSegment, currentConnectors])
                currentSegment = int(parts[0])
                currentConnectors = []
            elif len(parts) == 2:
                if currentSegment is None:
                    return None # invalid format
                currentConnectors.append([int(parts[0]),int(parts[1])])
        if currentSegment is not None and len(currentConnectors) > 0:
            result.append([currentSegment, currentConnectors])
        return result

    def update(self):
        global original_id
        self.errorMessage.setText("")
        self.info = {}
        nodeList = []
        lanelist = []
        lanepairlist =[]
        seglist = []

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for mulNode in root.iter('Intersection'):
            nodeList.append(mulNode.find('nodeID').text)

        for uniNode in root.iter('UniNode'):
            nodeList.append(uniNode.find('nodeID').text)

        for seg in root.iter('Segment'):
            seglist.append(seg.find('segmentID').text)

        nodeId = self.nodeId.text()
        if nodeId.isdigit() is False:
            self.errorMessage.setText("NodeId is invalid. It must be a number.")
            return

        if len(nodeId) > 5 :
            self.errorMessage.setText("NodeId is beyond range. Enter a shorter NodeID.")
            return

        if nodeId in nodeList and nodeId != original_id :
            self.errorMessage.setText("Node ID exists. Please enter another ID.")
            return

        self.info["id"] = int(nodeId)

        aimsunId = self.aimsunId.text()
        if aimsunId.isdigit() is False:
            self.errorMessage.setText("aimsunId is invalid. It must be a number.")
            return
        self.info["aimsunId"] = int(aimsunId)

        self.info["roadSegments"] = []
        roadSegments = self.roadSegmentEdit.toPlainText()
        if roadSegments:
            self.info["roadSegments"] = self.parseRoadSegments(roadSegments)
            for seg in self.info["roadSegments"] :
                if seg not in seglist :
                    self.errorMessage.setText("Segment id does not exist. Please enter existing segment id.")
                    return



        # self.info["multiConnectors"] = []
        # mulConnectors = self.mulConnectorEdit.toPlainText()
        # if mulConnectors:
        #     self.info["multiConnectors"] = self.parseMultiConnectors(mulConnectors)
        #     if self.info["multiConnectors"] is None:
        #         self.errorMessage.setText("The multiconnectors are in invalid format. Please enter in format 'laneFrom, laneTo'.")
        #         return



        for con in root.iter('Connector'):
            lf = int(con.find('laneFrom').text)
            lt = int(con.find('laneTo').text)
            lanepairlist.append([lf,lt])

        for lane in root.iter('Lane'):
            lanelist.append(lane.find('laneID').text)

        # for multiconnector in self.info["multiConnectors"]:
 #       self.errorMessage.setText(laneFromlist)
  #      return
# and self.info["multiConnectors"][0][1][0][1] in laneTolist)

        for multiconnector in self.info["multiConnectors"]:
            if multiconnector[1][0] in lanepairlist and nodeId != original_id:
                self.errorMessage.setText("A turning already exists between these lanes ")
                return
            if str(multiconnector[0]) not in seglist :
                self.errorMessage.setText("The segmentid in multiconnectors does not exist.")
                return
            if str(multiconnector[1][0][0]) not in lanelist or str(multiconnector[1][0][1]) not in lanelist :
                self.errorMessage.setText("The laneid does not exist.")
                return
            if multiconnector[1][0][0] == multiconnector[1][0][1] :
                self.errorMessage.setText("Lanefrom id and Laneto id cannot be the same.")
                return

        self.isModified = True

        #self.errorMessage.setText(str(self.isModified))
        #return

        self.accept()
