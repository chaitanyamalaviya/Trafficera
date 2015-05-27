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
from ui_lane import Ui_Lane
import os
# create the dialog for zoom to point


class LaneDialog(QtGui.QDialog, Ui_Lane):
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
            self.width.hide()
            self.segmentId.setText(str(self.info["segmentId"]))
            self.id.setText(str(self.info["id"]))
            self.wlineEdit.setText(str(self.info["width"]))
            self.tags.setText(str(self.info["tags"]))

            mode = bin(self.info["vehicle_mode"])
            if mode[2]=='1':
                self.pedestrian.setCheckState(QtCore.Qt.Checked)
            if mode[3]=='1':
                self.bicycle.setCheckState(QtCore.Qt.Checked)
            if mode[4]=='1':
                self.car.setCheckState(QtCore.Qt.Checked)
            if mode[5]=='1':
                self.van.setCheckState(QtCore.Qt.Checked)
            if mode[6]=='1':
                self.truck.setCheckState(QtCore.Qt.Checked)
            if mode[7]=='1':
                self.bus.setCheckState(QtCore.Qt.Checked)
            if mode[8]=='1':
                self.taxi.setCheckState(QtCore.Qt.Checked)

            if self.info["can_stop"]==1:
                self.can_stop.setCheckState(QtCore.Qt.Checked)

            if self.info["can_park"]==1:
                self.can_park.setCheckState(QtCore.Qt.Checked)

            if self.info["high_occ_veh"]==1:
                self.high_occ_veh.setCheckState(QtCore.Qt.Checked)

            if self.info["has_road_shoulder"]==1:
                self.has_road_shoulder.setCheckState(QtCore.Qt.Checked)

            self.bus_lane.setCurrentIndex(self.info["bus_lane"])

        else:
            self.actionButton.setText("ADD")
            self.width.hide()
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def update(self):

        self.info = {}
        msgBox = QtGui.QMessageBox()
        id = self.id.text()
        if id.isdigit() is False:
            msgBox.setText("LaneID is invalid. It must be a number.")
            msgBox.exec_()
            return

        self.info["id"] = int(id)

        if self.actionButton.text() == "SAVE":
            width = self.wlineEdit.text()
            if width.isdigit() is False:
                msgBox.setText("Width is invalid. It must be a number.")
                msgBox.exec_()
                return
            self.info["width"] = int(width)
        else:
            self.info["width"] = int(self.width.text())

        if self.pedestrian.isChecked():
            pedestrian = 1
        else:
            pedestrian = 0

        if self.bicycle.isChecked():
            bicycle = 1
        else:
            bicycle = 0

        if self.car.isChecked():
            car = 1
        else:
            car = 0

        if self.van.isChecked():
            van = 1
        else:
            van = 0

        if self.truck.isChecked():
            truck = 1
        else:
            truck = 0

        if self.bus.isChecked():
            bus = 1
        else:
            bus = 0

        if self.taxi.isChecked():
            taxi = 1
        else:
            taxi = 0

        vehicle_mode = pow(2,6)*pedestrian+pow(2,5)*bicycle+pow(2,4)*car+pow(2,3)*van+pow(2,2)*truck+pow(2,1)*bus+pow(2,0)*taxi
        self.info["vehicle_mode"] = vehicle_mode

        self.info["bus_lane"] = self.bus_lane.currentIndex()

        if self.can_stop.isChecked():
            self.info["can_stop"] = 1
        else:
            self.info["can_stop"] = 0

        if self.can_park.isChecked():
            self.info["can_park"] = 1
        else:
            self.info["can_park"] = 0

        if self.high_occ_veh.isChecked():
            self.info["high_occ_veh"] = 1
        else:
            self.info["high_occ_veh"] = 0

        if self.has_road_shoulder.isChecked():
            self.info["has_road_shoulder"] = 1
        else:
            self.info["has_road_shoulder"] = 0

        self.info["segmentId"] = int(self.segmentId.text())

        self.info["tags"] = self.tags.toPlainText()

        self.isModified = True
        self.accept()


