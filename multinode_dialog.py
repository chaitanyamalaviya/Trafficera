# -*- coding: utf-8 -*-
"""
/***************************************************************************
 iSimGisDialog
                                 A QGIS plugin
 iSim converter
                             -------------------
        begin                : 2015-03-25
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
from ui_multinode import Ui_MultiNode
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
        # self.turninggrouplist = []
        #self.turningpathlist = []

    def setInfo(self, info):
        self.info = info
        global original_id
        self.setLinklist()
        self.setLanelist()

        self.TurningGroupTable.setRowCount(0)
        self.TurningGroupTable.setColumnCount(5)
        TableHeader = ['ID','fromLink','toLink','Phases','Rules']
        self.TurningGroupTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningGroupTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningGroupTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


        self.TurningPathTable.setRowCount(0)
        self.TurningPathTable.setColumnCount(3)
        TableHeader = ['Turning Path ID', 'fromLane', 'toLane']
        self.TurningPathTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningPathTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningPathTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


        if self.info is not None:               # updating existing element
            self.isModified = True
            self.actionButton.setText("SAVE")
            self.nodeId.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.aimsunId.setText(str(self.info["aimsunId"]))
            self.nodeType.setEditText(self.info["nodeType"])
            self.trafficLightID.setText(self.info["trafficLightID"])

            if self.info["turningGroup"]:
                for group in self.info["turningGroup"]:
                    ridx = self.info["turningGroup"].index(group)
                    self.TurningGroupTable.insertRow(ridx)
                    for cidx in range(5):
                        self.TurningGroupTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(group[cidx]))

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
            self.addnewid()
            self.actionButton.setText("ADD")
            self.info = {}
            self.info["turningGroup"] = []
            self.info["turningPath"] = []
        QtCore.QObject.connect(self.newturningGroup, QtCore.SIGNAL('clicked(bool)'), self.addTurningGroup)
        QtCore.QObject.connect(self.newTurningPath, QtCore.SIGNAL('clicked(bool)'), self.addTurningPath)
        QtCore.QObject.connect(self.TurningGroupTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayturninggroup)
        QtCore.QObject.connect(self.TurningPathTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayturningpath)

        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def addTurningGroup(self):
        #self.info = {}

        turningGroupID = self.turningGroupID.text()
        if turningGroupID.isdigit() is False:
            self.errorMessage.setText("Turning Group ID is invalid. It must be a number.")
            return

        ridx = len(self.info["turningGroup"])
        self.info["turningGroup"].append([turningGroupID, self.fromLink.currentText(), self.toLink.currentText(), self.Phases.text(), self.Rules.currentText()])

        self.TurningGroupTable.insertRow(ridx)
        for cidx in range(5) :
                self.TurningGroupTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(self.info["turningGroup"][ridx][cidx]))


    def addTurningPath(self):
        #self.info = {}

        turningPathID = self.TurningPath.text()
        if turningPathID.isdigit() is False:
            self.errorMessage.setText("Turning Path ID is invalid. It must be a number.")
            return
        groupID = self.turningGroupID.text()

        ridx = self.TurningPathTable.rowCount()
        self.info["turningPath"].append([groupID, turningPathID, self.fromLane.currentText(), self.toLane.currentText()])

        self.TurningPathTable.insertRow(ridx)
        self.TurningPathTable.setItem(ridx,0,QtGui.QTableWidgetItem(turningPathID))
        self.TurningPathTable.setItem(ridx,1,QtGui.QTableWidgetItem(self.fromLane.currentText()))
        self.TurningPathTable.setItem(ridx,2,QtGui.QTableWidgetItem(self.toLane.currentText()))

        # for cidx in range(3) :
        #         self.TurningPathTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(self.info["turningPath"][ridx][cidx+1]))

        # self.info["turningPath"].append(self.turningpathlist)


    def displayturninggroup(self):

        #self.info = {}
        # self.errorMessage.setText(''.join(self.info["turningGroup"][ridx][0]))
        # return
        self.turningGroupID.setText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),0).text())
        self.fromLink.setCurrentIndex(self.fromLink.findText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),1).text()))
        self.toLink.setCurrentIndex(self.toLink.findText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),2).text()))
        self.Phases.setText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),3).text())
        self.Rules.setCurrentIndex(self.Rules.findText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),4).text()))

        # display corresponding turning paths in turning path table

            # for tG in root.iter('TurningGroup'):
            #     if self.turningGroupID.currentText() == tG.find('ID').text:
            #         i=0
            #         for tp in tG.findall('TurningPaths'):
            #             self.TurningPathTable.setItem(i,0,tp.find('ID'))
            #             self.TurningPathTable.setItem(i,1,tp.find('fromLane'))
            #             self.TurningPathTable.setItem(i,2,tp.find('toLane'))
            #             i = i+1
        self.TurningPathTable.clear()
        TableHeader = ['Turning Path ID', 'fromLane', 'toLane']
        self.TurningPathTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningPathTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningPathTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.TurningPathTable.setRowCount(0)
        self.TurningPathTable.setColumnCount(3)

        i = 0

        for path in self.info["turningPath"]:
            # msgBox = QtGui.QMessageBox()
            # msgBox.setText("Lopop")
            # msgBox.exec_()
            # return
            if self.turningGroupID.text() == str(path[0]):
                self.TurningPathTable.insertRow(i)
                for cidx in range(3) :
                    self.TurningPathTable.setItem(i,cidx,QtGui.QTableWidgetItem(path[cidx+1]))
                i+=1



    def displayturningpath(self):
        ridx = self.TurningPathTable.currentRow()
        self.TurningPath.setText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),0).text())       #groupid is index 0
        #self.fromLane.setEditText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),1).text())
        self.fromLane.setCurrentIndex(self.fromLane.findText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),1).text()))
        self.toLane.setCurrentIndex(self.toLane.findText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),2).text()))




    def setLinklist(self):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for link in root.iter('Link'):
            self.fromLink.addItem(link.find('linkID').text)
            self.toLink.addItem(link.find('linkID').text)


    def setLanelist(self):
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for lane in root.iter('Lane'):
            self.fromLane.addItem(lane.find('laneID').text)
            self.toLane.addItem(lane.find('laneID').text)

    def addnewid(self):
        nodeList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for mulNode in root.iter('Intersection'):
            nodeList.append(int(mulNode.find('nodeID').text))

        self.nodeId.setText(str(max(nodeList)+1))

        return


    # def genturningConflicts(self):
    #
    #
    #     get all intersections of turning paths
    #     check if phase is same
    #     if yes:
    #         add to turning conflict table
    #     else:
    #         nothing
    # 
    #     turning conflict table attributes : id, first turning, second turning, firstcd, secondcd



    def update(self):
        global original_id
        self.errorMessage.setText("")
        nodeList = []
        #self.info = {}
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for mulNode in root.iter('Intersection'):
            nodeList.append(mulNode.find('nodeID').text)

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

        self.info["nodeType"]= self.nodeType.currentText()

        trafficLightID = self.trafficLightID.text()
        if trafficLightID.isdigit() is False:
            self.errorMessage.setText("Traffic Light ID is invalid. It must be a number.")
            return
        self.info["trafficLightID"] = int(trafficLightID)

        # if not self.info["turningGroup"]:
        #     self.info["turningGroup"] = []
        # if not self.info["turningPath"]:
        #     self.info["turningPath"] = []

        # self.info["multiConnectors"] = []
        # mulConnectors = self.mulConnectorEdit.toPlainText()
        # if mulConnectors:
        #     self.info["multiConnectors"] = self.parseMultiConnectors(mulConnectors)
        #     if self.info["multiConnectors"] is None:
        #         self.errorMessage.setText("The multiconnectors are in invalid format. Please enter in format 'laneFrom, laneTo'.")
        #         return



        # for con in root.iter('Connector'):
        #     lf = int(con.find('laneFrom').text)
        #     lt = int(con.find('laneTo').text)
        #     lanepairlist.append([lf,lt])
        #
        # for lane in root.iter('Lane'):
        #     lanelist.append(lane.find('laneID').text)

        # for multiconnector in self.info["multiConnectors"]:
 #       self.errorMessage.setText(laneFromlist)
  #      return
# and self.info["multiConnectors"][0][1][0][1] in laneTolist)

        # for multiconnector in self.info["multiConnectors"]:
        #     if multiconnector[1][0] in lanepairlist and nodeId != original_id:
        #         self.errorMessage.setText("A turning already exists between these lanes ")
        #         return
        #     if str(multiconnector[0]) not in seglist :
        #         self.errorMessage.setText("The segmentid in multiconnectors does not exist.")
        #         return
        #     if str(multiconnector[1][0][0]) not in lanelist or str(multiconnector[1][0][1]) not in lanelist :
        #         self.errorMessage.setText("The laneid does not exist.")
        #         return
        #     if multiconnector[1][0][0] == multiconnector[1][0][1] :
        #         self.errorMessage.setText("Lanefrom id and Laneto id cannot be the same.")
        #         return

        self.isModified = True

        #self.errorMessage.setText(str(self.isModified))
        #return

        self.accept()
