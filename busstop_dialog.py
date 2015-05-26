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
from __future__ import division
from PyQt4 import QtCore, QtGui
from ui_busstop import Ui_Busstop
import os
import math
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *

# create the dialog for zoom to point


class BusstopDialog(QtGui.QDialog, Ui_Busstop):

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

    def getSegmentList(self):
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        listSegments = []
        for segment in root.iter('segment'):
            listSegments.append(segment.find("id").text)
        return listSegments

    def setSegmentList(self):

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        for segment in root.iter('segment'):
            self.segmentIDcomboBox.addItem(segment.find('id').text)

    def setSegmentId(self, segmentId):
        self.segmentIDcomboBox.setCurrentIndex(self.getSegmentList().index(str(segmentId)))

    def addnewid(self):
        busList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for busstop in root.iter('bus_stop'):
            busList.append(int(busstop.find('id').text))

        if busList is not None:
            self.id.setText(str(max(busList)+1))
        else:
            self.id.setText(str(0))
        return


    def calculateOffset(self, point, segmentId):
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory, nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        x1 = x2 = y1 = y2 = 0.0
        for segment in root.iter('segment'):
            if segment.find('id').text == str(segmentId):
                for pt in segment.iter('point'):
                    if pt.find('seq_id').text == str(0):
                        x1 = float(pt.find('x').text)
                        y1 = float(pt.find('y').text)
                    elif pt.find('seq_id').text == str(1):
                        x2 = float(pt.find('x').text)
                        y2 = float(pt.find('y').text)

        m = (y2-y1)/(x2-x1)
        m1 = -1/m
        c1 = point.y() - m1*point.x()
        c = y1 - m*x1
        x3 = (c1-c)/(m-m1)
        y3 = (m*c1-m1*c)/m-m1
        d = math.sqrt(pow((x2-x1),2)+pow((y2-y1),2))
        d2 = math.sqrt(pow((x3-x1),2)+pow((y3-y1),2))
        offset = (d/d2)*100

        return str(offset)

    def setInfo(self, info):
        self.info = info
        global original_id
        # self.setSegmentList()
        if self.info is not None:
            self.isModified = True
            self.setSegmentList()
            self.actionButton.setText("SAVE")
            self.segmentIDcomboBox.setCurrentIndex(self.getSegmentList().index(str(self.info["segment_id"])))
            self.id.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.offset.setText(str(self.info["offset"]))
            self.length.setText(str(self.info["length"]))
            self.name.setText(str(self.info["name"]))
            self.busstopCode.setText(str(self.info["busstopCode"]))
            if self.info["isTerminal"] == "true" or self.info["isTerminal"] == "True":
                self.isTerminal.setCheckState(QtCore.Qt.Checked)
            if self.info["isBay"] == "true" or self.info["isBay"] == "True":
                self.isBay.setCheckState(QtCore.Qt.Checked)   
            if self.info["hasShelter"] == "true" or self.info["hasShelter"] == "True":
                self.hasShelter.setCheckState(QtCore.Qt.Checked)
            self.busstoptags.setPlainText(str(self.info["tags"]))
        else:
            self.actionButton.setText("ADD")
            self.addnewid()
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def update(self):
        global original_id
        msgBox = QtGui.QMessageBox()
        self.info = {}
        busstopList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory,nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()
        # geom = f.geometry()
        # print geom.asPoint()
        # QgsPoint
        # self.info["segmentId"]

        id = self.id.text()
        if id.isdigit() is False:
            msgBox.setText("BusStop ID is invalid. It must be a number.")
            msgBox.exec_()
            return

        if len(id) > 5 :
            msgBox.setText("BusStop ID is beyond range. Enter a shorter BusStopID.")
            msgBox.exec_()
            return

        for BusStop in root.iter('bus_stop'):
            busstopid = BusStop.find('id').text
            busstopList.append(busstopid)

        if id in busstopList and id != original_id:
            msgBox.setText("BusStop ID exists. Please enter another ID.")
            msgBox.exec_()
            return

        self.info["id"] = int(id)
        busstopList.append(id)

        segmentID = self.segmentIDcomboBox.currentText()
        self.info["segment_id"] = int(segmentID)


        self.info["offset"] = float(self.offset.text())

        length = self.length.text()
        if length.isdigit() is False:
            msgBox.setText("Length is invalid. It must be a number.")
            msgBox.exec_()
            return
        elif int(length)>500:
            msgBox.setText("Length of bus stop is beyond range. Please enter an appropriate value.")
            msgBox.exec_()
            return
        elif length is None:
            msgBox.setText("Length cannot be empty. Please enter an appropriate value.")
            msgBox.exec_()
            return
        self.info["length"] = float(length)

        busstopCode = self.busstopCode.text()
        if busstopCode.isdigit() is False:
            msgBox.setText("Busstop Code is invalid. It must be a number.")
            msgBox.exec_()
            return
        elif len(busstopCode)>10:
            msgBox.setText("Busstop Code cannot be longer than 10 digits. Please enter an appropriate value.")
            msgBox.exec_()
            return
        elif busstopCode is None:
            msgBox.setText("Busstop Code cannot be empty. Please enter an appropriate value.")
            msgBox.exec_()
            return

        self.info["busstopCode"] = busstopCode

        if len(self.name.text())>20:
            msgBox.setText("Busstop Name cannot be longer than 20 characters. Please enter an appropriate name.")
            msgBox.exec_()
            return
        elif self.name.text is None:
            msgBox.setText("Busstop Name cannot be empty. Please enter an appropriate name.")
            msgBox.exec_()
            return
        self.info["name"] = self.name.text()

        if self.isTerminal.isChecked():
            self.info["isTerminal"] = "true"
        else:
            self.info["isTerminal"] = "false"                        
        if self.isBay.isChecked():
            self.info["isBay"] = "true"
        else:
            self.info["isBay"] = "false"  
        if self.hasShelter.isChecked():
            self.info["hasShelter"] = "true"
        else:
            self.info["hasShelter"] = "false"

        self.info["tags"] = self.busstoptags.toPlainText()

        self.isModified = True
        self.accept()