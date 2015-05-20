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
from ui_trainstop import Ui_TrainStop
import os
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *
# create the dialog for zoom to point


class TrainstopDialog(QtGui.QDialog, Ui_TrainStop):

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

    def addSegment(self):
        segments = self.segmentsListLineEdit.text()
        segList = []
        if segments:
            segList = segments.split(',')
        segList.append(self.segmentIDcomboBox.currentText())
        self.segmentsListLineEdit.setText(",".join(segList))

    def setInfo(self, info):
        self.info = info
        global original_id
        original_id = 0
        # self.setSegmentList()
        if self.info is not None:
            self.isModified = True
            self.setSegmentList()
            self.pushButton.setText("SAVE")
            self.segmentIDcomboBox.setCurrentIndex(0)
            self.id.setText(str(self.info["id"]))
            original_id = self.info["id"]
            self.segmentsListLineEdit.setText(",".join(self.info["segments"]))
            self.platform_name.setText(str(self.info["platform_name"]))
            self.station_name.setText(str(self.info["station_name"]))
            self.type.setText(str(self.info["type"]))
            self.tags.setPlainText(str(self.info["tags"]))
        else:
            self.pushButton.setText("ADD")
        QtCore.QObject.connect(self.segmentIDcomboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.addSegment)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def update(self):
        global original_id
        msgBox = QtGui.QMessageBox()
        self.info = {}
        trainstopList = []
        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory,nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        id = self.id.text()
        if id.isdigit() is False:
            msgBox.setText("ID is invalid. It must be a number.")
            msgBox.exec_()
            return

        if len(id) > 5 :
            msgBox.setText("TrainStopId is beyond range. Enter a shorter TrainStopID.")
            msgBox.exec_()
            return

        for TrainStop in root.iter('train_stop'):
            trainstopid = TrainStop.find('id').text
            trainstopList.append(trainstopid)

        if id in trainstopList and id != original_id:
            msgBox.setText("TrainStop ID exists. Please enter another ID.")
            msgBox.exec_()
            return

        self.info["id"] = int(id)
        trainstopList.append(id)

        self.info["segments"] = self.segmentsListLineEdit.text().split(',')

        self.info["platform_name"] = self.platform_name.text()
        self.info["station_name"] = self.station_name.text()
        self.info["type"] = self.type.text()
        self.info["tags"] = self.tags.toPlainText()

        self.isModified = True
        self.accept()