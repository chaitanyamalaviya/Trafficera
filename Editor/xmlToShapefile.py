import os, re
from xml.etree import ElementTree
from shapefileIO import ShapefileWriter, TYPE as SHTYPE
from PyQt4.QtCore import *
from qgis.core import *

class XmlToShapefile(QObject):
    # Signal emitted to update progress
    prog_sig = pyqtSignal(int)
    def __init__(self, xml_path, sh_dir, formula):
        QObject.__init__(self)
        self.document = None
        self.writer = ShapefileWriter(sh_dir)
        ElementTree.register_namespace('geo', "http://www.smart.mit.edu/geo")
        self.document = ElementTree.parse(xml_path)
        self.formula = formula

    def parseLocation(self, data):
        x = float(data.find("xPos").text)
        y = float(data.find("yPos").text)
        
        pos = QgsPoint(eval(self.formula[0]), eval(self.formula[1]))
        data.find("xPos").text = "--"
        data.find("yPos").text = "--"
        return pos

    def parseUninode(self, uninode):
        nodeId = uninode.find("nodeID").text
        location = uninode.find("location")
        if location is None:
            QgsMessageLog.logMessage("No location in uninode %s"%str(nodeId), 'SimGDC')
            return
        point = self.parseLocation(location)
        attr = [nodeId]
        self.writer.addPoint(SHTYPE.UNINODE, point, attr)

    def parseMulnode(self, mulnode):
        nodeId = mulnode.find("nodeID").text
        location = mulnode.find("location")
        if location is None:
            QgsMessageLog.logMessage("No location in multinode %s"%str(nodeId), 'SimGDC')
            return        
        point = self.parseLocation(location)
        attr = [nodeId]
        self.writer.addPoint(SHTYPE.MULNODE, point, attr)

    def parseLane(self, segmentId, lane):
        landId = lane.find("laneID").text
        attr = [segmentId, landId]
        coordinates = []
        polyLine = lane.find("PolyLine")
        if polyLine is None:
            QgsMessageLog.logMessage("No PolyLine in lane %s"%str(landId), 'SimGDC')
            return  
        for polypoint in polyLine.findall('PolyPoint'):
            coordinates.append(self.parseLocation(polypoint.find('location')))
        self.writer.addPolyline(SHTYPE.LANE, coordinates, attr)

    def parseLaneEdge(self, segmentId, laneEdge):
        laneNumber = laneEdge.find("laneNumber").text
        attr = [segmentId, laneNumber]
        coordinates = []
        polyLine = laneEdge.find("polyline")
        if polyLine is None:
            QgsMessageLog.logMessage("No polyline in laneEdge %s of segment %s"%(str(laneNumber),str(segmentId)), 'SimGDC')
            return            
        for polypoint in polyLine.findall('PolyPoint'):
            coordinates.append(self.parseLocation(polypoint.find('location')))
        self.writer.addPolyline(SHTYPE.LANEEDGE, coordinates, attr)
    
    def parseCrossing(self, segmentId, crossing):
        crossingId = crossing.find("id").text
        attr = [segmentId, crossingId]
        coordinates = [0, 1, 2, 3]
        nearLine = crossing.find("nearLine")
        if nearLine is None:
            QgsMessageLog.logMessage("No nearLine in crossing %s"%crossingId, 'SimGDC')
            return 
        coordinates[0] = self.parseLocation(nearLine.find('first'))
        coordinates[1] = self.parseLocation(nearLine.find('second'))
        farLine = crossing.find("farLine")
        if farLine is None:
            QgsMessageLog.logMessage("No farLine in crossing %s"%crossingId, 'SimGDC')
            return 
        coordinates[3] = self.parseLocation(farLine.find('first'))
        coordinates[2] = self.parseLocation(farLine.find('second'))
        self.writer.addPolygon(SHTYPE.CROSSING, coordinates, attr)

    def parseBusstop(self, segmentId, busstop):
        point = self.parseLocation(busstop)
        attr = [segmentId, busstop.find("id").text]
        self.writer.addPoint(SHTYPE.BUSSTOP, point, attr) 

    def parseSegment(self, linkId, segment):
        segmentId = segment.find("segmentID").text
        attr = [linkId, segmentId]
        coordinates = [] 
        polyline = segment.find("polyline")
        if polyline is None:
            QgsMessageLog.logMessage("segment %s has no polyline info."%segmentId, 'SimGDC')
            return
        for polypoint in polyline.findall('PolyPoint'):
            coordinates.append(self.parseLocation(polypoint.find('location')))
        if len(coordinates) == 0:
            QgsMessageLog.logMessage("segment %s has no polygon info."%segmentId, 'SimGDC')
            return
        if len(coordinates) < 3:
            coordinates.append(QgsPoint(coordinates[0]))
            coordinates.append(QgsPoint(coordinates[1]))
        #parse Lane
        lanes = segment.find("Lanes")
        if lanes is not None:
            for lane in lanes.findall('Lane'):
                self.parseLane(segmentId, lane)
        #parse Lane Egde
        laneEdges = segment.find("laneEdgePolylines_cached")
        if laneEdges is not None:
            for laneEdge in laneEdges.findall('laneEdgePolyline_cached'):
                self.parseLaneEdge(segmentId, laneEdge)
        #parse obstacles
        obstacles = segment.find("Obstacles")
        if obstacles is not None:
            for obstacle in obstacles.iter():
                if obstacle.tag == "Crossing":
                    self.parseCrossing(segmentId, obstacle)
                elif obstacle.tag == "BusStop":
                    self.parseBusstop(segmentId, obstacle)
        self.writer.addPolygon(SHTYPE.SEGMENT, coordinates, attr)

    def run(self):
        if self.document == None:
            return
        progPercent = 0
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        #parse nodes
        nodes = roadNetwork.find('Nodes')
        if nodes is not None:
            uniNodes = []
            mulNodes = []
            uniNodeParent = nodes.find('UniNodes')
            if uniNodeParent is not None:
                uniNodes = uniNodeParent.findall('UniNode')
            mulNodeParent = nodes.find('Intersections')
            if mulNodeParent is not None:
                mulNodes = mulNodeParent.findall('Intersection')

            count = len(uniNodes) + len(mulNodes)
            for uninode in uniNodes:
                self.parseUninode(uninode)
                progPercent = progPercent + 50.0/count
                self.prog_sig.emit(progPercent)
            for mulNode in mulNodes:
                self.parseMulnode(mulNode)
                progPercent = progPercent + 50.0/count
                self.prog_sig.emit(progPercent)

        #parse segment
        links = []
        linkParent = roadNetwork.find('Links')
        if linkParent is not None:
            links = linkParent.findall('Link')
        count = len(links)
        for link in links:
            linkId = link.find('linkID').text
            segmentParent = link.find('Segments')
            if segmentParent is not None:
                segments = segmentParent.findall('Segment')
                if segments is not None:
                    for segment in segments:
                        self.parseSegment(linkId, segment)
            progPercent = progPercent + 50.0/count
            self.prog_sig.emit(progPercent)
        
        #save shapefiles
        self.writer.save()
        #save the rest of xml file
        xmlRemainPath = os.path.join(self.writer.path, "data.xml")
        self.document.write(xmlRemainPath, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml")