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
        self.TurningGroupTable.setColumnCount(7)
        TableHeader = ['ID','fromLink','toLink','Phases','Rules','Visibility','Tags']
        self.TurningGroupTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningGroupTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningGroupTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


        self.TurningPathTable.setRowCount(0)
        self.TurningPathTable.setColumnCount(5)
        TableHeader = ['Turning Path ID', 'fromLane', 'toLane','Max Speed','Tags']
        self.TurningPathTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningPathTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningPathTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


        if self.info is not None:               # updating existing element
            self.isModified = True
            self.actionButton.setText("SAVE")
            self.nodeId.setText(str(self.info["id"]))
            original_id = self.info["id"]
            # self.aimsunId.setText(str(self.info["aimsunId"]))
            self.nodeType.setCurrentIndex(int(self.info["nodeType"]))
            self.trafficLightID.setText(self.info["trafficLightID"])
            self.tags_node.setPlainText(self.info["tags"])

            if self.info["turningGroup"]:
                for group in self.info["turningGroup"]:
                    ridx = self.info["turningGroup"].index(group)
                    self.TurningGroupTable.insertRow(ridx)
                    for cidx in range(7):
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
        QtCore.QObject.connect(self.delturninggroupButton, QtCore.SIGNAL('clicked(bool'), self.deleteTurningGroup)
        QtCore.QObject.connect(self.delturningpathButton, QtCore.SIGNAL('clicked(bool'), self.deleteTurningPath)
        QtCore.QObject.connect(self.TurningGroupTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayturninggroup)
        QtCore.QObject.connect(self.TurningPathTable, QtCore.SIGNAL('itemSelectionChanged()'), self.displayturningpath)

        # QtCore.QObject.connect(self.genconflictbutton, QtCore.SIGNAL('clicked(bool'), self.genturningConflicts)

        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def addTurningGroup(self):
        #self.info = {}
        msgBox = QtGui.QMessageBox()
        turningGroupID = self.turningGroupID.text()
        if turningGroupID.isdigit() is False:
            msgBox.setText("Turning Group ID is invalid. It must be a number.")
            msgBox.exec_()
            return
        elif len(turningGroupID)>6:
            msgBox.setText("Turning Group ID is beyond range. Please enter a shorter Turning Group ID.")
            msgBox.exec_()
            return

        for turningGroup in self.info["turningGroup"]:
            if turningGroup[0]==turningGroupID:
                msgBox.setText("Turning Group ID exists. Please enter a different ID.")
                msgBox.exec_()
                return

        if self.fromLink.currentText()==self.toLink.currentText():
            msgBox.setText("fromLink cannot be same as toLink. Please enter different link IDs.")
            msgBox.exec_()
            return

        if len(self.Phases.text())>5:
            msgBox.setText("Phase information cannot be longer than 5 characters. Please enter an appropriate value.")
            msgBox.exec_()
            return
        elif not self.Phases.text():
            msgBox.setText("Phases field cannot be empty. Please enter an appropriate value.")
            msgBox.exec_()
            return

        if len(self.visibility_distance.text())>5:
            msgBox.setText("Visibility distance cannot be longer than 5 characters. Please enter an appropriate value.")
            msgBox.exec_()
            return
        elif not self.visibility_distance.text():
            msgBox.setText("Visibility Distance cannot be empty. Please enter an appropriate value.")
            msgBox.exec_()
            return

        ridx = len(self.info["turningGroup"])
        self.info["turningGroup"].append([turningGroupID, self.fromLink.currentText(), self.toLink.currentText(), self.Phases.text(), self.Rules.currentText(),self.visibility_distance.text(),self.tags_turninggroup.toPlainText()])

        self.TurningGroupTable.insertRow(ridx)
        for cidx in range(7) :
                self.TurningGroupTable.setItem(ridx,cidx,QtGui.QTableWidgetItem(self.info["turningGroup"][ridx][cidx]))


    def addTurningPath(self):
        #self.info = {}
        msgBox = QtGui.QMessageBox()

        turningPathID = self.TurningPath.text()
        if turningPathID.isdigit() is False:
            msgBox.setText("Turning Path ID is invalid. It must be a number.")
            msgBox.exec_()
            return
        for id in range(self.TurningPathTable.rowCount()):
            if self.TurningPathTable.item(id,0).text() == turningPathID:
                msgBox.setText("Turning Path ID exists. Please enter a different ID.")
                msgBox.exec_()
                return

        if self.fromLane.currentText() == self.toLane.currentText():
            msgBox.setText("fromLane cannot be same as toLane. Please enter different lane IDs.")
            msgBox.exec_()
            return

        group_id = self.turningGroupID.text()

        maxSpeed = self.maxSpeed.text()
        if maxSpeed.isdigit() is False:
            msgBox.setText("maxSpeed is invalid. It must be a number.")
            msgBox.exec_()
            return

        elif len(maxSpeed) > 3:
            msgBox.setText("maxSpeed is beyond range. Enter a shorter value for speed.")
            msgBox.exec_()
            return

        ridx = self.TurningPathTable.rowCount()
        self.info["turningPath"].append([group_id, turningPathID, self.fromLane.currentText(), self.toLane.currentText(),self.maxSpeed.text(),self.tags_turningpath.toPlainText()])

        self.TurningPathTable.insertRow(ridx)
        self.TurningPathTable.setItem(ridx,0,QtGui.QTableWidgetItem(turningPathID))
        self.TurningPathTable.setItem(ridx,1,QtGui.QTableWidgetItem(self.fromLane.currentText()))
        self.TurningPathTable.setItem(ridx,2,QtGui.QTableWidgetItem(self.toLane.currentText()))
        self.TurningPathTable.setItem(ridx,3,QtGui.QTableWidgetItem(self.visibility_distance.text()))
        self.TurningPathTable.setItem(ridx,4,QtGui.QTableWidgetItem(self.tags_turningpath.toPlainText()))

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
        self.visibility_distance.setText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),5).text())
        self.tags_turninggroup.setPlainText(self.TurningGroupTable.item(self.TurningGroupTable.currentRow(),6).text())
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
        TableHeader = ['Turning Path ID', 'fromLane', 'toLane','Max Speed','Tags']
        self.TurningPathTable.setHorizontalHeaderLabels(TableHeader)
        self.TurningPathTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TurningPathTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.TurningPathTable.setRowCount(0)
        self.TurningPathTable.setColumnCount(5)

        i = 0

        for path in self.info["turningPath"]:
            # msgBox = QtGui.QMessageBox()
            # msgBox.setText("Lopop")
            # msgBox.exec_()
            # return
            if self.turningGroupID.text() == str(path[0]):
                self.TurningPathTable.insertRow(i)
                for cidx in range(5):
                    self.TurningPathTable.setItem(i,cidx,QtGui.QTableWidgetItem(path[cidx+1]))
                i+=1



    def displayturningpath(self):
        ridx = self.TurningPathTable.currentRow()
        self.TurningPath.setText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),0).text())       #groupid is index 0
        #self.fromLane.setEditText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),1).text())
        self.fromLane.setCurrentIndex(self.fromLane.findText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),1).text()))
        self.toLane.setCurrentIndex(self.toLane.findText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),2).text()))
        self.maxSpeed.setText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),3).text())
        self.tags_turningpath.setPlainText(self.TurningPathTable.item(self.TurningPathTable.currentRow(),4).text())



    def setLinklist(self):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for link in root.iter('link'):
            self.fromLink.addItem(link.find('id').text)
            self.toLink.addItem(link.find('id').text)
        self.fromLink.setCurrentIndex(0)
        self.toLink.setCurrentIndex(0)

    def setLanelist(self):
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for lane in root.iter('lane'):
            self.fromLane.addItem(lane.find('id').text)
            self.toLane.addItem(lane.find('id').text)
        self.fromLane.setCurrentIndex(0)
        self.toLane.setCurrentIndex(0)

    def addnewid(self):
        nodeList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for node in root.iter('node'):
            nodeList.append(int(node.find('id').text))

        self.nodeId.setText(str(max(nodeList)+1))

        return

    def deleteTurningGroup(self):
        ridx = self.TurningGroupTable.currentRow()
        self.TurningGroupTable.clear(ridx)
        self.info["turningGroup"].pop(ridx)
        for tP in self.info["turningPath"]:
            if tP[0] == self.info["turningGroup"][ridx][0]:
                self.info["turningPath"].pop(ridx)


        self.TurningPathTable.clear()


    def deleteTurningPath(self):
        ridx = self.TurningPathTable.currentRow()
        self.info["turningPath"].pop(ridx)
        self.TurningPathTable.clear(ridx)


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
        msgBox = QtGui.QMessageBox()
        nodeList = []
        #self.info = {}
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for node in root.iter('node'):
            nodeList.append(node.find('id').text)

        nodeId = self.nodeId.text()
        if nodeId.isdigit() is False:
            msgBox.setText("NodeId is invalid. It must be a number.")
            msgBox.exec_()
            return


        if len(nodeId) > 5 :
            msgBox.setText("NodeId is beyond range. Enter a shorter NodeID.")
            msgBox.exec_()
            return

        if nodeId in nodeList and nodeId != original_id :
            msgBox.setText("Node ID exists. Please enter another ID.")
            msgBox.exec_()
            return

        self.info["id"] = int(nodeId)

        self.info["nodeType"]= self.nodeType.currentIndex()


        trafficLightID = self.trafficLightID.text()
        if trafficLightID:
            if trafficLightID.isdigit() is False:
                msgBox.setText("Traffic Light ID is invalid. It must be a number.")
                msgBox.exec_()
                return
            else:
                self.info["trafficLightID"] = int(trafficLightID)
        else:
            self.info["trafficLightID"] = trafficLightID

        self.info["tags"] = self.tags_node.toPlainText()

        self.isModified = True

        self.accept()
