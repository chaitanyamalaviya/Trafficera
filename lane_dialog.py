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
            self.segmentId.setText(str(self.info["segmentId"]))
            self.id.setText(str(self.info["id"]))
            self.width.setText(str(self.info["width"]))
            self.tags.setText(str(self.info["tags"]))

            if self.info["can_go_straight"] == "true":
                self.can_go_straight.setCheckState(QtCore.Qt.Checked)
            if self.info["can_turn_left"] == "true":
                self.can_turn_left.setCheckState(QtCore.Qt.Checked)   
            if self.info["can_turn_right"] == "true":
                self.can_turn_right.setCheckState(QtCore.Qt.Checked)   
            if self.info["can_turn_on_red_signal"] == "true":
                self.can_turn_on_red_signal.setCheckState(QtCore.Qt.Checked)  
            if self.info["can_change_lane_left"] == "true":
                self.can_change_lane_left.setCheckState(QtCore.Qt.Checked)  
            if self.info["can_change_lane_right"] == "true":
                self.can_change_lane_right.setCheckState(QtCore.Qt.Checked)   
            if self.info["is_road_shoulder"] == "true":
                self.is_road_shoulder.setCheckState(QtCore.Qt.Checked)     
            if self.info["is_bicycle_lane"] == "true":
                self.is_bicycle_lane.setCheckState(QtCore.Qt.Checked)  
            if self.info["is_pedestrian_lane"] == "true":
                self.is_pedestrian_lane.setCheckState(QtCore.Qt.Checked)  
            if self.info["is_vehicle_lane"] == "true":
                self.is_vehicle_lane.setCheckState(QtCore.Qt.Checked)  
            if self.info["is_standard_bus_lane"] == "true":
                self.is_standard_bus_lane.setCheckState(QtCore.Qt.Checked)  
            if self.info["is_whole_day_bus_lane"] == "true":
                self.is_whole_day_bus_lane.setCheckState(QtCore.Qt.Checked) 
            if self.info["is_high_occupancy_vehicle_lane"] == "true":
                self.is_high_occupancy_vehicle_lane.setCheckState(QtCore.Qt.Checked) 
            if self.info["can_freely_park_here"] == "true":
                self.can_freely_park_here.setCheckState(QtCore.Qt.Checked) 
            if self.info["can_stop_here"] == "true":
                self.can_stop_here.setCheckState(QtCore.Qt.Checked) 
            if self.info["is_u_turn_allowed"] == "true":
                self.is_u_turn_allowed.setCheckState(QtCore.Qt.Checked) 
        else:
            self.actionButton.setText("ADD")
        QtCore.QObject.connect(self.actionButton, QtCore.SIGNAL('clicked(bool)'), self.update)

    def update(self):
        self.errorMessage.setText("")
        self.info = {}

        id = self.id.text()
        if id.isdigit() is False:
            self.errorMessage.setText("id is invalid. It must be a number.")
            return
        self.info["id"] = int(id)

        width = self.width.text()
        if width.isdigit() is False:
            self.errorMessage.setText("width is invalid. It must be a number.")
            return
        self.info["width"] = int(width)  

        if self.can_go_straight.isChecked():
            self.info["can_go_straight"] = "true"
        else:
            self.info["can_go_straight"] = "false"                        
        if self.can_turn_left.isChecked():
            self.info["can_turn_left"] = "true"
        else:
            self.info["can_turn_left"] = "false"  
        if self.can_turn_right.isChecked():
            self.info["can_turn_right"] = "true"
        else:
            self.info["can_turn_right"] = "false"  
        if self.can_turn_on_red_signal.isChecked():
            self.info["can_turn_on_red_signal"] = "true"
        else:
            self.info["can_turn_on_red_signal"] = "false"  
        if self.can_change_lane_left.isChecked():
            self.info["can_change_lane_left"] = "true"
        else:
            self.info["can_change_lane_left"] = "false" 
        if self.can_change_lane_right.isChecked():
            self.info["can_change_lane_right"] = "true"
        else:
            self.info["can_change_lane_right"] = "false" 
        if self.is_road_shoulder.isChecked():
            self.info["is_road_shoulder"] = "true"
        else:
            self.info["is_road_shoulder"] = "false" 
        if self.is_bicycle_lane.isChecked():
            self.info["is_bicycle_lane"] = "true"
        else:
            self.info["is_bicycle_lane"] = "false" 
        if self.is_pedestrian_lane.isChecked():
            self.info["is_pedestrian_lane"] = "true"
        else:
            self.info["is_pedestrian_lane"] = "false" 
        if self.is_vehicle_lane.isChecked():
            self.info["is_vehicle_lane"] = "true"
        else:
            self.info["is_vehicle_lane"] = "false" 
        if self.is_standard_bus_lane.isChecked():
            self.info["is_standard_bus_lane"] = "true"
        else:
            self.info["is_standard_bus_lane"] = "false" 
        if self.is_whole_day_bus_lane.isChecked():
            self.info["is_whole_day_bus_lane"] = "true"
        else:
            self.info["is_whole_day_bus_lane"] = "false" 
        if self.is_high_occupancy_vehicle_lane.isChecked():
            self.info["is_high_occupancy_vehicle_lane"] = "true"
        else:
            self.info["is_high_occupancy_vehicle_lane"] = "false" 
        if self.can_freely_park_here.isChecked():
            self.info["can_freely_park_here"] = "true"
        else:
            self.info["can_freely_park_here"] = "false" 
        if self.can_stop_here.isChecked():
            self.info["can_stop_here"] = "true"
        else:
            self.info["can_stop_here"] = "false" 
        if self.is_u_turn_allowed.isChecked():
            self.info["is_u_turn_allowed"] = "true"
        else:
            self.info["is_u_turn_allowed"] = "false" 

        self.info["segmentId"] = int(self.segmentId.text())

        self.info["tags"] = self.tags.text()

        self.isModified = True
        self.accept()


