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
        x = float(data.find("x").text)
        y = float(data.find("y").text)
        
        pos = QgsPoint(eval(self.formula[0]), eval(self.formula[1]))
        # data.find("x").text = "--"                                    Won't parse out location
        # data.find("y").text = "--"
        return pos

    def parseMulnode(self, mulnode):
        nodeId = mulnode.find("id").text
        point = mulnode.find("point")
        if point is None:
            QgsMessageLog.logMessage("No polypoint in node %s"%str(nodeId), 'SimGDC')
            return        
        point = self.parseLocation(point)
        attr = [nodeId]
        turningPaths = mulnode.find("turning_path")

        self.writer.addPoint(SHTYPE.NODE, point, attr)

    def parseLane(self, segmentId, lane):
        laneId = lane.find("id").text
        attr = [segmentId, laneId]
        coordinates = []
        polyLine = lane.find("polyline")
        if polyLine is None:
            QgsMessageLog.logMessage("No polyline in lane %s"%str(laneId), 'SimGDC')
            return
        points = polyLine.find("points")
        for point in points.findall("point"):
            coordinates.append(self.parseLocation(point))
        if len(coordinates) == 0:
            QgsMessageLog.logMessage("Lane %s has no polyline info."%laneId, 'SimGDC')
            return

        self.writer.addPolyline(SHTYPE.LANE, coordinates, attr)

    def parseLaneEdge(self, segmentId, laneEdge):
        laneNumber = laneEdge.find("laneNumber").text
        attr = [segmentId, laneNumber]
        coordinates = []
        polyLine = laneEdge.find("polyline")
        if polyLine is None:
            QgsMessageLog.logMessage("No polyline in laneEdge %s of segment %s"%(str(laneNumber),str(segmentId)), 'SimGDC')
            return            
        for polypoint in polyLine.findall('point'):
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

    def parseTurningPath(self, turningpath):

        id = turningpath.find("id").text
        groupID = turningpath.find("group_id").text
        attr = [id, groupID]
        coordinates = []
        polyline = turningpath.find("polyline")
        if polyline is None:
            QgsMessageLog.logMessage("Turning Path %s has no polyline info."%id, 'SimGDC')
            return
        points = polyline.find("points")
        for point in points.findall("point"):
            coordinates.append(self.parseLocation(point))
        if len(coordinates) == 0:
            QgsMessageLog.logMessage("Turning Path %s has no polyline info."%id, 'SimGDC')
            return

        self.writer.addPolyline(SHTYPE.TURNINGPATH,coordinates, attr)

    def parseLink(self, link):

        id = link.find("id").text
        road_name = link.find("road_name").text
        attr = [id,road_name]
        coordinates = []
        polyline = link.find("polyline")
        if polyline is None:
            QgsMessageLog.logMessage("Link %s has no polyline info."%id, 'SimGDC')
            return
        points = polyline.find("points")
        for point in points.findall("point"):
            coordinates.append(self.parseLocation(point))
        if len(coordinates) == 0:
            QgsMessageLog.logMessage("Link %s has no polyline info."%id, 'SimGDC')
            return

        self.writer.addPolyline(SHTYPE.LINK,coordinates, attr)


    def parseBusstop(self, busstop):
        point = busstop.find("point")
        coordinates = self.parseLocation(point)
        attr = [busstop.find("segment_id").text, busstop.find("id").text]
        self.writer.addPoint(SHTYPE.BUSSTOP, coordinates, attr)

    def parseTrainstop(self, trainstop):
        point = trainstop.find("point")
        coordinates = self.parseLocation(point)
        attr = ["".join(trainstop.findall("segment_id")), trainstop.find("id").text]
        self.writer.addPoint(SHTYPE.TRAINSTOP, coordinates, attr)

    def parseSegment(self, linkId, segment):
        segmentId = segment.find("id").text
        attr = [linkId, segmentId]
        coordinates = [] 
        polyline = segment.find("polyline")
        if polyline is None:
            QgsMessageLog.logMessage("segment %s has no polyline info."%segmentId, 'SimGDC')
            return
        points = polyline.find("points")
        for point in points.findall("point"):
            coordinates.append(self.parseLocation(point))
        if len(coordinates) == 0:
            QgsMessageLog.logMessage("segment %s has no polyline info."%segmentId, 'SimGDC')
            return
        # if len(coordinates) < 3:
        #     coordinates.append(QgsPoint(coordinates[0]))
        #     coordinates.append(QgsPoint(coordinates[1]))
        #parse Lane
        lanes = segment.find("lanes")
        if lanes is not None:
            for lane in lanes.findall('lane'):
                self.parseLane(segmentId, lane)
        # #parse Lane Edge
        # laneEdges = segment.find("laneEdgePolylines_cached")
        # if laneEdges is not None:
        #     for laneEdge in laneEdges.findall('laneEdgePolyline_cached'):
        #         self.parseLaneEdge(segmentId, laneEdge)

        self.writer.addPolyline(SHTYPE.SEGMENT, coordinates, attr)

    def run(self):
        if self.document == None:
            return
        progPercent = 0
        roadNetwork = self.document.find('road_network')
        #parse nodes
        nodes = roadNetwork.find('nodes')
        if nodes is not None:
            mulNodes = nodes.findall('node')

            count = len(mulNodes)
            for mulNode in mulNodes:
                self.parseMulnode(mulNode)
                progPercent = progPercent + 50.0/count
                self.prog_sig.emit(progPercent)


        for turningpath in roadNetwork.iter('turning_path'):
            self.parseTurningPath(turningpath)

        #parse obstacles
        pt_stops = roadNetwork.find("pt_stops")
        if pt_stops is not None:
            for bus_stop in pt_stops.iter('bus_stop'):
                self.parseBusstop(bus_stop)
            for train_stop in pt_stops.iter('train_stop'):
                self.parseTrainstop(train_stop)

        #parse link,segment
        links = []
        linkParent = roadNetwork.find('links')
        if linkParent is not None:
            links = linkParent.findall('link')
        count = len(links)
        for link in links:
            self.parseLink(link)
            linkId = link.find('id').text
            segmentParent = link.find('segments')
            if segmentParent is not None:
                segments = segmentParent.findall('segment')
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