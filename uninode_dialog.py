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
from ui_uninode import Ui_UniNode
import os
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *
# create the dialog for zoom to point


class UniNodeDialog(QtGui.QDialog, Ui_UniNode):
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


    def setInfo(self, info):
        self.info = info
        if self.info is not None:
            self.actionButton.setText("SAVE")
            self.nodeId.setText(str(self.info["id"]))
            self.aimsunId.setText(str(self.info["aimsunId"]))
            if self.info["firstPair"] is not None:
                self.firstPair.setText("%s,%s"%(self.info["firstPair"][0],self.info["firstPair"][1]))
            if self.info["secondPair"] is not None:
                self.secondPair.setText("%s,%s"%(self.info["secondPair"][0],self.info["secondPair"][1]))
            connectors = []
            for connector in self.info["connectors"]:
                connectors.append("%s,%s"%(connector[0],connector[1]))
            self.connectorEdit.setPlainText("\n".join(connectors))
        else:
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    
    def parsePairField(self, pairText):
        if pairText == "":
            return 0
        pairs = pairText.split(",")
        if len(pairs) != 2:
            return None
        if pairs[0].isdigit() is False or pairs[1].isdigit() is False:
            return None
        return [int(pairs[0]), int(pairs[1])]

    def parseConnectors(self, connectorsText):
        result = []
        connectors = connectorsText.split("\n")
        for connectorStr in connectors:
            connector = connectorStr.split(",")
            if len(connector) != 2:
                return None
            if connector[0].isdigit() is False or connector[1].isdigit() is False:
                return None
            result.append([int(connector[0]), int(connector[1])])
        return result

    def update(self):
        self.errorMessage.setText("")
        self.info = {}
        nodeList = []
        lanelist = []
        lanepairlist = []


        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for uniNode in root.iter('UniNode'):
            nodeList.append(uniNode.find('nodeID').text)

        for mulNode in root.iter('Intersection'):
            nodeList.append(mulNode.find('nodeID').text)

        nodeId = self.nodeId.text()
        if nodeId.isdigit() is False:
            self.errorMessage.setText("nodeId is invalid. It must be a number.")
            return

        if nodeId in nodeList :
            self.errorMessage.setText("Node ID exists. Please enter another ID.")
            return

        self.info["id"] = int(nodeId)

        aimsunId = self.aimsunId.text()
        if aimsunId.isdigit() is False:
            self.errorMessage.setText("aimsunId is invalid. It must be a number.")
            return
        self.info["aimsunId"] = int(aimsunId)

        firstPair = self.firstPair.text()
        self.info["firstPair"] = self.parsePairField(firstPair)
        if self.info["firstPair"] is None:
            self.errorMessage.setText("firstPair is invalid. It must be: number,number")
            return

        secondPair = self.secondPair.text()
        self.info["secondPair"] = self.parsePairField(secondPair)
        if self.info["secondPair"] is None:
            self.errorMessage.setText("secondPair is invalid. It must be: number,number")
            return      

        connectors = self.connectorEdit.toPlainText()
        if not connectors:
            self.errorMessage.setText("the connectors can not be empty.")
            return

        self.info["connectors"] = self.parseConnectors(connectors)
        if self.info["connectors"] is None:
            self.errorMessage.setText("The connectors are in invalid format. Please enter in format 'laneFrom, laneTo'.")
            return

        for con in root.iter('Connector'):
            lf = int(con.find('laneFrom').text)
            lt = int(con.find('laneTo').text)
            lanepairlist.append([lf,lt])

        for lane in root.iter('Lane'):
            lanelist.append(lane.find('laneID').text)


        for connector in self.info["connectors"]:
            if connector in lanepairlist :
                self.errorMessage.setText("A turning already exists between these lanes ")
                return
            if str(connector[0]) not in lanelist or str(connector[1]) not in lanelist :
                self.errorMessage.setText("The laneid does not exist.")
                return
            if connector[0] == connector[1] :
                self.errorMessage.setText("Lanefrom id and Laneto id cannot be the same.")
                return

        self.isModified = True
        self.accept()
