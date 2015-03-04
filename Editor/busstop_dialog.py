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
from ui_busstop import Ui_Busstop
import os
from xml.etree import ElementTree
from qgis.core import *
from qgis.utils import *
# create the dialog for zoom to point


class BusstopDialog(QtGui.QDialog, Ui_Busstop):
    busstoplist = []

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

    def setSegmentId(self, segmentId):
        self.segmentId.setText(str(segmentId))

    def setInfo(self, info):
        self.info = info


        if self.info is not None:
            self.actionButton.setText("SAVE")
            self.segmentId.setText(str(self.info["segmentId"]))
            self.id.setText(str(self.info["id"]))
            self.offset.setText(str(self.info["offset"]))
            self.busCapacity.setText(str(self.info["busCapacity"]))
            self.busstopNo.setText(str(self.info["busstopno"]))
            if self.info["isTerminal"] == "true" or self.info["isTerminal"] == "True":
                self.isTerminal.setCheckState(QtCore.Qt.Checked)
            if self.info["isBay"] == "true" or self.info["isBay"] == "True":
                self.isBay.setCheckState(QtCore.Qt.Checked)   
            if self.info["hasShelter"] == "true" or self.info["hasShelter"] == "True":
                self.hasShelter.setCheckState(QtCore.Qt.Checked)          
        else:
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def update(self):
        self.errorMessage.setText("")
        self.info = {}
        busstopList = []
        id = self.id.text()
        if id.isdigit() is False:
            self.errorMessage.setText("id is invalid. It must be a number.")
            return

        layerfi = iface.activeLayer().dataProvider().dataSourceUri()
        (myDirectory,nameFile) = os.path.split(layerfi)
        tree = ElementTree.parse(myDirectory + '/data.xml')
        root = tree.getroot()

        for BusStop in root.iter('BusStop'):
            busstopid = BusStop.find('id').text
            busstopList.append(busstopid)

        if id in busstopList and self.isModified is True:
            self.errorMessage.setText("BusStop ID exists. Please enter another ID.")
            return

        self.info["id"] = int(id)
        busstopList.append(id)

        offset = self.offset.text()
        if offset.isdigit() is False:
            self.errorMessage.setText("offset is invalid. It must be a number.")
            return
        self.info["offset"] = int(offset)

        busCapacity = self.busCapacity.text()
        if busCapacity.isdigit() is False:
            self.errorMessage.setText("BusCapacity is invalid. It must be a number.")
            return
        self.info["busCapacity"] = int(busCapacity)  

        busstopno = self.busstopNo.text()
        if busstopno.isdigit() is False:
            self.errorMessage.setText("Busstop No is invalid. It must be a number.")
            return
        self.info["busstopno"] = int(busstopno)

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

        self.info["segmentId"] = int(self.segmentId.text())

        self.isModified = True
        self.accept()