# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SimGDC
                                 A QGIS plugin
 SimMobility Geospatial Data Converter
                              -------------------
        begin                : 2014-02-03
        copyright            : (C) 2014 by chaitanyamalaviya
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar, QgsMapToolEmitPoint, QgsMapToolPan
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from converter_dialog import ConverterDialog
from multinode_dialog import MultiNodeDialog
from segment_dialog import SegmentDialog
from crossing_dialog import CrossingDialog
from busstop_dialog import BusstopDialog
from trainstop_dialog import TrainstopDialog
from lane_dialog import LaneDialog
from laneedge_dialog import LaneEdgeDialog
from linkmanager_dialog import LinkManagerDialog
from os import listdir, path, getenv, getcwd
#import from others
import shutil
from xmlToShapefile import XmlToShapefile
from actionHandler import *

class SimGDC:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # reference to map canvas
        self.canvas = self.iface.mapCanvas() 
        # this QGIS tool emits as QgsPoint after each click on the map canvas
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        # create a pan tool
        self.toolPan = QgsMapToolPan(self.canvas)
        # converter dialog
        self.converterdlg = None
        self.featuredlg = None
        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = path.join(self.plugin_dir, 'i18n', 'isimgis_{}.qm'.format(locale))
        if path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        QSettings().setValue( "/Projections/defaultBehaviour", "useGlobal" )
        # crs
        #self.crs = QgsCoordinateReferenceSystem(3168)

    def initGui(self):
        self.converter_action = QAction(
            QIcon(":/plugins/isimgis/icons/converter.png"),
            u"SimMobility Geospatial Data Converter", self.iface.mainWindow())

        self.open_action = QAction(
            QIcon(":/plugins/isimgis/icons/open.png"),
            u"Open SimGDC shapefile directory", self.iface.mainWindow())

        self.new_action = QAction(
            QIcon(":/plugins/isimgis/icons/notepad-icon.png"),
            u"Create a new shapefile directory", self.iface.mainWindow())

        self.link_manager_action = QAction(
            QIcon(":/plugins/isimgis/icons/linkmanager.png"),
            u"Manage links.", self.iface.mainWindow())

        self.add_action = QAction(
            QIcon(":/plugins/isimgis/icons/add.png"),
            u"Add features to current active layer.", self.iface.mainWindow())

        self.edit_action = QAction(
            QIcon(":/plugins/isimgis/icons/edit.png"),
            u"Edit attributes of the selected feature", self.iface.mainWindow())
 
        self.delete_action = QAction(
            QIcon(":/plugins/isimgis/icons/delete.png"),
            u"Delete selected features from current active layer.", self.iface.mainWindow())

        self.gen_lane_action = QAction(
            QIcon(":/plugins/isimgis/icons/add_lane.png"),
            u"Generate lanes and lane edges for the selected segment.", self.iface.mainWindow())


        # connect the action to the run method
        self.converter_action.triggered.connect(self.converter)
        self.open_action.triggered.connect(self.open)
        self.new_action.triggered.connect(self.new)
        self.link_manager_action.triggered.connect(self.manageLinks)
        self.add_action.triggered.connect(self.addFeaturePre)
        self.edit_action.triggered.connect(self.editFeature)
        self.delete_action.triggered.connect(self.deleteFeature)
        self.gen_lane_action.triggered.connect(self.generateLane)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.converter_action)
        self.iface.addToolBarIcon(self.open_action)
        self.iface.addToolBarIcon(self.new_action)
        self.iface.addToolBarIcon(self.link_manager_action)
        self.iface.addToolBarIcon(self.add_action)
        self.iface.addToolBarIcon(self.edit_action)
        self.iface.addToolBarIcon(self.delete_action)
        self.iface.addToolBarIcon(self.gen_lane_action)

        self.iface.addPluginToMenu(u"&SimGDC", self.converter_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.open_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.new_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.link_manager_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.add_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.edit_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.delete_action)
        self.iface.addPluginToMenu(u"&SimGDC", self.gen_lane_action)

        self.clickTool.canvasClicked.connect(self.addFeature)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&SimGDC", self.open_action)
        self.iface.removePluginMenu(u"&SimGDC", self.converter_action)
        self.iface.removePluginMenu(u"&SimGDC", self.add_action)
        self.iface.removeToolBarIcon(self.open_action)
        self.iface.removeToolBarIcon(self.converter_action)
        self.iface.removeToolBarIcon(self.add_action)

    def new(self):
        sh_dir = QFileDialog.getExistingDirectory(None, 'Create new SimGDC Shapefile Directory', getenv('HOME'))
        if sh_dir == "":
            return
        prefix = path.basename(sh_dir)

        # find the template
        current_full_path = path.realpath(__file__)
        current_dir, current_file = path.split(current_full_path)
        template_dir = path.join(current_dir, "template")

        xml_path = path.join(template_dir, "template.xml")
        xmlToShapefile = XmlToShapefile(xml_path, sh_dir, ["x", "y"])
        xmlToShapefile.run()

        # open layer
        self.open(sh_dir)


    def open(self, sh_dir):
        if isinstance(sh_dir, bool) or sh_dir == "":
            sh_dir = QFileDialog.getExistingDirectory(None, 'Open SimGDC Shapefile Directory', getenv('HOME'))
            if sh_dir == "":
                return
        
        prefix = path.basename(sh_dir)
        for tag in TAGS.values():
            filename = "%s_%s" % (prefix, tag)
            full_path = path.join(sh_dir, "%s.shp"%filename)
            layer = QgsVectorLayer(full_path, filename, "ogr")
            if layer.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(layer)
        '''
        for filenames in listdir(sh_dir):
            full_path = path.join(sh_dir, filenames)
            names = filenames.split(".")
            if path.isfile(full_path) and names[1] == "shp":
                layer = QgsVectorLayer(full_path, names[0], "ogr")
                if layer.isValid():
                    #layer.setCrs(self.crs)
                    QgsMapLayerRegistry.instance().addMapLayer(layer)
        '''

    # open convert dialog
    def converter(self):
        if self.converterdlg is not None:
            self.converterdlg.raise_()
            self.converterdlg.activateWindow()
            return
        self.converterdlg = ConverterDialog()
        self.converterdlg.open_sig.connect(self.open)
        self.converterdlg.show()
        # Run the dialog event loop
        self.converterdlg.exec_()
        del self.converterdlg
        self.converterdlg = None

    #return isValid, sh_dir, layer_name 
    def checkActiveLayerInfo(self):
        active_layer = self.iface.activeLayer()
        if active_layer is None:
            return False, "", ""
        uri = active_layer.dataProvider().dataSourceUri()
        sh_dir = path.dirname(uri)
        layer_name = path.basename(uri).split(".")[0]
        data_file = path.join(sh_dir, "data.xml")
        if path.isfile(data_file):
            return True, sh_dir, layer_name
        else:
            return False, sh_dir, layer_name

    def addFeaturePre(self):
        # make our clickTool the tool that we'll use for now
        self.canvas.setMapTool(self.clickTool)
        #self.iface.messageBar().pushMessage("Info", "Please indica", level=QgsMessageBar.INFO)


    def addFeature(self, point, button):
        isValidLayer, sh_dir, layer_name = self.checkActiveLayerInfo()
        if not isValidLayer:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "There is no active layer or the active layer is not SimGDC shapefile layer.")
            return

        typeId = getSHTypeFromLayername(layer_name)
        if self.featuredlg is not None:
            self.featuredlg.close()
            del self.featuredlg
            self.featuredlg = None

        # initialize handler
        handler = ActionHandler(sh_dir, self.canvas)

        if typeId == TYPE.MULNODE:
            self.featuredlg = MultiNodeDialog()
        elif typeId == TYPE.SEGMENT:
            linkLists = handler.getLinkList()
            if len(linkLists) == 0:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "There is no link, so it is impossible to add a segment.")
                return
            self.featuredlg = SegmentDialog()
            self.featuredlg.setLinkList(linkLists)  
        elif typeId == TYPE.CROSSING or typeId == TYPE.BUSSTOP or typeId == TYPE.LANE or typeId == TYPE.LANEEDGE:
            segmenLayer = handler.getLayer(TYPE.SEGMENT)
            selectedSegments = segmenLayer.selectedFeatures()
            if len(selectedSegments) == 0:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please select a segment from the segment layer.")
                return
            if len(selectedSegments) > 1:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please select only one segment from the segment layer!")
                return 
            selectedSegment = selectedSegments[0]
            attrs = selectedSegment.attributes()
            selectedSegmentId = int(attrs[1])
            if typeId == TYPE.CROSSING:
                self.featuredlg = CrossingDialog()
            elif typeId == TYPE.BUSSTOP:
                self.featuredlg = BusstopDialog()
                self.featuredlg.setSegmentList()
                self.featuredlg.offset.setText(self.featuredlg.calculateOffset(point, selectedSegmentId))
            elif typeId == TYPE.LANE:
                self.featuredlg = LaneDialog()    
            elif typeId == TYPE.LANEEDGE:
                self.featuredlg = LaneEdgeDialog()             

            self.featuredlg.setSegmentId(selectedSegmentId)



        elif typeId == TYPE.TRAINSTOP:
            segmentLayer = handler.getLayer(TYPE.SEGMENT)
            selectedSegments = segmentLayer.selectedFeatures()
            if len(selectedSegments) == 0:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please select a segment from the segment layer.")
                return

            segIDlist = []
            for segment in selectedSegments:
                attrs = segment.attributes()
                selectedSegmentId = str(attrs[1])
                segIDlist.append(selectedSegmentId)

            segIDstring = ",".join(segIDlist)
            self.featuredlg = TrainstopDialog()
            self.featuredlg.setSegmentList()
            self.featuredlg.setSegmentId(segIDstring)

        #show the dialog
        self.featuredlg.setInfo(None)
        self.featuredlg.show()
        self.featuredlg.exec_()

        if self.featuredlg is not None and self.featuredlg.isModified is True:
            if typeId == TYPE.MULNODE:
                nodeData = self.featuredlg.info
                handler.addMultiNode(point, nodeData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.SEGMENT:
                segmentData = self.featuredlg.info
                handler.addSegment(point, segmentData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.CROSSING:
                crossingData = self.featuredlg.info
                handler.addCrossing(point, crossingData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.BUSSTOP:
                busstopData = self.featuredlg.info
                handler.addBusstop(point, busstopData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.TRAINSTOP:
                trainstopData = self.featuredlg.info
                handler.addTrainstop(point, trainstopData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.LANE:
                laneData = self.featuredlg.info
                handler.addLane(point, laneData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.LANEEDGE:
                laneEdgeData = self.featuredlg.info
                handler.addLaneEdge(point, laneEdgeData)
                handler.save()
                self.canvas.refresh()

        del self.featuredlg
        self.featuredlg = None
        self.canvas.setMapTool(self.toolPan)
        #QMessageBox.information(self.iface.mainWindow(),"Info", "X,Y = %s,%s" % (str(point.x()),str(point.y())))

    def editFeature(self):
        # verify the current layer
        isValidLayer, sh_dir, active_layer_name = self.checkActiveLayerInfo()
        if not isValidLayer:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "The active layer is not SimGDC shapefile layer.")
            return

        # make sure there is a selected feature
        active_layer = self.iface.activeLayer()
        selected_features = active_layer.selectedFeatures()
        if len(selected_features) == 0:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No feature is selected.")
            return

        if len(selected_features) > 1:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please select only one feature!")
            return

        typeId = getSHTypeFromLayername(active_layer_name)
        if self.featuredlg is not None:
            self.featuredlg.close()
            del self.featuredlg
            self.featuredlg = None

        handler = ActionHandler(sh_dir, self.canvas)
        if typeId == TYPE.MULNODE:
            eleData = handler.getMultiNode(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = MultiNodeDialog()    
        elif typeId == TYPE.SEGMENT:
            responseInfo = handler.getSegment(selected_features[0])
            if responseInfo is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            eleData = responseInfo[1]   
            self.featuredlg = SegmentDialog()  
            self.featuredlg.setLinkList(responseInfo[0])  
        elif typeId == TYPE.CROSSING:      
            eleData = handler.getCrossing(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = CrossingDialog() 
        elif typeId == TYPE.BUSSTOP:      
            eleData = handler.getBusstop(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = BusstopDialog()
        elif typeId == TYPE.TRAINSTOP:
            eleData = handler.getTrainstop(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = TrainstopDialog()
        elif typeId == TYPE.LANE:      
            eleData = handler.getLane(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = LaneDialog()
        elif typeId == TYPE.LANEEDGE:      
            eleData = handler.getLaneEdge(selected_features[0])
            if eleData is None:
                QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No data for that feature.")
                return
            self.featuredlg = LaneEdgeDialog()

        self.featuredlg.setInfo(eleData)
        self.featuredlg.show()
        self.featuredlg.exec_()

        if self.featuredlg is not None and self.featuredlg.isModified is True:
            if typeId == TYPE.MULNODE:
                newData = self.featuredlg.info
                handler.updateMultiNode(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.SEGMENT:
                newData = self.featuredlg.info
                handler.updateSegment(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.CROSSING:
                newData = self.featuredlg.info
                handler.updateCrossing(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.BUSSTOP:
                newData = self.featuredlg.info
                handler.updateBusstop(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.TRAINSTOP:
                newData = self.featuredlg.info
                handler.updateTrainstop(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.LANE:
                newData = self.featuredlg.info
                handler.updateLane(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()
            elif typeId == TYPE.LANEEDGE:
                newData = self.featuredlg.info
                handler.updateLaneEdge(selected_features[0], newData)
                handler.save()
                self.canvas.refresh()

        del self.featuredlg
        self.featuredlg = None       


    def deleteFeature(self):
        # verify the current layer
        isValidLayer, sh_dir, active_layer_name = self.checkActiveLayerInfo()
        if not isValidLayer:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "The active layer is not SimGDC shapefile layer.")
            return

        # make sure there is a selected feature
        active_layer = self.iface.activeLayer()
        selected_features = active_layer.selectedFeatures()
        if len(selected_features) == 0:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No feature is selected.")
            return

        # confirm message
        reply = QMessageBox.question(self.iface.mainWindow(), "Are you sure?", "Are you sure to delete the selected features ? It is NOT possible to undo this action.", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No);
        if reply == QMessageBox.No:
            return

        #should save all changes before deleting
        if active_layer.isEditable():
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please save all of your changes and turn of editing mode before deleting features.")
            return

        handler = ActionHandler(sh_dir, self.canvas)
        # remove data dependency
        handler.delete(selected_features)
        handler.save()
            
        self.canvas.refresh()

    def manageLinks(self):
        isValidLayer, sh_dir, layer_name = self.checkActiveLayerInfo()
        if not isValidLayer:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "There is no active layer or the active layer is not SimGDC shapefile layer.")
            return

        if self.featuredlg is not None:
            self.featuredlg.close()
            del self.featuredlg
            self.featuredlg = None

        handler = ActionHandler(sh_dir, self.canvas)
        linkLists = handler.getLinkListDetail()
        self.featuredlg = LinkManagerDialog()
        self.featuredlg.setLinkList(linkLists)

        self.featuredlg.show()
        self.featuredlg.exec_()

        if self.featuredlg is not None and self.featuredlg.isModified is True:
            linkData = self.featuredlg.info
            handler.manageLink(linkData)
            handler.save()

        del self.featuredlg
        self.featuredlg = None 

    def generateLane(self):
         # verify the current layer
        isValidLayer, sh_dir, active_layer_name = self.checkActiveLayerInfo()
        if not isValidLayer:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "The active layer is not SimGDC shapefile layer.")
            return

        # make sure there is a selected feature
        active_layer = self.iface.activeLayer()
        selected_features = active_layer.selectedFeatures()
        if len(selected_features) == 0:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "No feature is selected.")
            return

        if len(selected_features) > 1:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "Please select only one feature!")
            return
        
        typeId = getSHTypeFromLayername(active_layer_name)
        if typeId != TYPE.SEGMENT:
            QMessageBox.critical(self.iface.mainWindow(),"SimGDC Error", "This action is only applied to selected segment!")
            return

        nLane, ok = QInputDialog.getInt(self.iface.mainWindow(), 'Number of Lanes', 'Enter number of Lanes:', 1, 1, 20)
        width, ok2 = QInputDialog.getInt(self.iface.mainWindow(), 'Width', 'Enter width of the Lanes:', 100, 1, 1000)
        if ok and ok2:
            handler = ActionHandler(sh_dir, self.canvas)
            handler.generateLaneByNumber(selected_features[0], nLane, width)
            handler.generateLaneByNumber(selected_features[0], nLane, width)
            handler.save()
            self.canvas.refresh()

