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
from ui_crossing import Ui_Crossing
import os
# create the dialog for zoom to point


class CrossingDialog(QtGui.QDialog, Ui_Crossing):
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

        offset = self.offset.text()
        if offset.isdigit() is False:
            self.errorMessage.setText("offset is invalid. It must be a number.")
            return
        self.info["offset"] = int(offset)

        self.info["segmentId"] = int(self.segmentId.text())

        self.isModified = True
        self.accept()


