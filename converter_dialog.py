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
from ui_converter import Ui_Converter
from xmlToShapefile import XmlToShapefile
from shapefileToXml import ShapefileToXml
import os
# create the dialog for zoom to point


class ConverterDialog(QtGui.QDialog, Ui_Converter):
    open_sig = QtCore.pyqtSignal(str)
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        #XML to SH
        self.xmlsh_progress.setVisible(False)
        self.xmlsh_status.setVisible(False)
        QtCore.QObject.connect(self.xmlsh_converter_but, QtCore.SIGNAL('clicked(bool)'), self.convertXMLToSH)
        QtCore.QObject.connect(self.xmlsh_xml_browser, QtCore.SIGNAL('clicked(bool)'), self.xmlshXMLBrowser)
        QtCore.QObject.connect(self.xmlsh_sh_browser, QtCore.SIGNAL('clicked(bool)'), self.xmlshSHBrowser)

        #SH to XML
        self.shxml_progress.setVisible(False)
        self.shxml_status.setVisible(False)
        QtCore.QObject.connect(self.shxml_converter_but, QtCore.SIGNAL('clicked(bool)'), self.convertSHToXML)
        QtCore.QObject.connect(self.shxml_xml_browser, QtCore.SIGNAL('clicked(bool)'), self.shxmlXMLBrowser)
        QtCore.QObject.connect(self.shxml_sh_browser, QtCore.SIGNAL('clicked(bool)'), self.shxmlSHBrowser)

    def xmlshXMLBrowser(self):
        xml_path = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'), "XML files (*.xml)")
        self.xmlsh_xml_path.setText(xml_path)

    def shxmlXMLBrowser(self):
        xml_path = QtGui.QFileDialog.getSaveFileName(self, 'Save XML', "%s/untitled.xml" % os.getenv('HOME'), "XML files (*.xml)")
        self.shxml_xml_path.setText(xml_path)

    def xmlshSHBrowser(self):
        sh_dir = QtGui.QFileDialog.getExistingDirectory(self, 'Save Shapefile output', os.getenv('HOME'))
        self.xmlsh_sh_path.setText(sh_dir)

    def shxmlSHBrowser(self):
        sh_dir = QtGui.QFileDialog.getExistingDirectory(self, 'Open iSim Shapefile directory', os.getenv('HOME'))
        self.shxml_sh_path.setText(sh_dir)

    def xmlshUpdateProgress(self, value):
        self.xmlsh_progress.setProperty("value", value)
        QtGui.QApplication.processEvents()

    def shxmlUpdateProgress(self, value):
        self.shxml_progress.setProperty("value", value)
        QtGui.QApplication.processEvents()

    def convertXMLToSH(self):
        xml_path = self.xmlsh_xml_path.text()
        sh_dir = self.xmlsh_sh_path.text()
        if xml_path == "" or sh_dir == "":
            self.xmlsh_status.setVisible(True)
            self.xmlsh_status.setText("<font color='red'>Please select XML file and destination directory!<font>")
            return

        formula_x = self.xmlsh_formula_x.text()
        formula_y = self.xmlsh_formula_y.text()
        if formula_x == "" or formula_y == "":
            self.xmlsh_status.setVisible(True)
            self.xmlsh_status.setText("<font color='red'>Please enter the coordinate conversion formular!<font>")
            return

        self.xmlsh_status.setVisible(False)
        self.xmlsh_progress.setVisible(True)
        self.xmlsh_converter_but.setEnabled(False)
        try:
            xmlToShapefile = XmlToShapefile(xml_path, sh_dir, [formula_x, formula_y])
            xmlToShapefile.prog_sig.connect(self.xmlshUpdateProgress)
            xmlToShapefile.run()
        except IOError as e:
            self.xmlsh_status.setVisible(True)
            self.xmlsh_progress.setVisible(False)
            self.xmlsh_converter_but.setEnabled(True)
            self.xmlsh_status.setText("<font color='red'>Error: %s<font>" % e.strerror)

        self.open_sig.emit(sh_dir)
        self.accept()

    def convertSHToXML(self):
        xml_path = self.shxml_xml_path.text()
        sh_dir = self.shxml_sh_path.text()
        if xml_path == "" or sh_dir == "":
            self.shxml_status.setVisible(True)
            self.shxml_status.setText("<font color='red'>Please shape files directory and xml output!<font>")
            return

        formula_x = self.shxml_formula_x.text()
        formula_y = self.shxml_formula_y.text()
        if formula_x == "" or formula_y == "":
            self.shxml_status.setVisible(True)
            self.shxml_status.setText("<font color='red'>Please enter the coordinate conversion formular!<font>")
            return

        self.shxml_status.setVisible(False)
        self.shxml_progress.setVisible(True)
        self.shxml_converter_but.setEnabled(False)
        try:
            shapefileToXml = ShapefileToXml(xml_path, sh_dir, [formula_x, formula_y])
            shapefileToXml.prog_sig.connect(self.shxmlUpdateProgress)
            shapefileToXml.run()
        except IOError as e:
            self.shxml_status.setText("<font color='red'>Error: %s<font>" % e.strerror)
        finally:
            self.shxml_status.setVisible(True)
            self.shxml_progress.setVisible(False)
            self.shxml_converter_but.setEnabled(True)
        self.shxml_status.setText("<font color='blue'>Converting successfully.</font>")       