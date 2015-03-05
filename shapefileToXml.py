import os, re
from xml.etree import ElementTree
from xml.dom import minidom
from shapefileIO import ShapefileReader, TYPE as SHTYPE
from PyQt4.QtCore import *

class ShapefileToXml(QObject):
    # Signal emitted to update progress
    prog_sig = pyqtSignal(int)
    def __init__(self, xmlPath, shDir, formula):
        QObject.__init__(self)
        self.xmlPath = xmlPath
        self.reader = ShapefileReader(shDir)
        ElementTree.register_namespace('geo', "http://www.smart.mit.edu/geo")
        self.document = ElementTree.parse(os.path.join(shDir, "data.xml"))
        self.formula = formula

    def warnNonExist(self, typeId, id):
        print "Warning: there is not %s whose id is %s in shapefile!" % (typeId, id)
    
    def updateLocation(self, element, data):
        x = float(data.x())
        y = float(data.y())

        xPos = element.find("xPos")
        if xPos is None:
            xPos = ElementTree.SubElement(element, 'xPos')
        xPos.text = str(eval(self.formula[0]))
        yPos = element.find("yPos")
        if yPos is None:
            yPos = ElementTree.SubElement(element, 'yPos')
        yPos.text = str(eval(self.formula[1]))

    def addXMLLocation(self, parent, data):
        x = float(data.x())
        y = float(data.y())
        
        location = ElementTree.SubElement(parent, 'location')
        ElementTree.SubElement(location, 'xPos').text = str(eval(self.formula[0]))
        ElementTree.SubElement(location, 'yPos').text = str(eval(self.formula[1]))

    def updateUninodes(self, uninodes):
        nodeData = self.reader.getNodes(SHTYPE.UNINODE)
        for uninode in uninodes:
            nodeId = int(uninode.find("nodeID").text)
            if nodeId in nodeData:
                location = uninode.find("location")
                if location is None:
                    self.addXMLLocation(uninode, nodeData[nodeId])
                else:
                    self.updateLocation(location, nodeData[nodeId])
            else:
                self.warnNonExist("UniNode", nodeId)

    def updateMulnodes(self, mulnodes):
        nodeCoordinates = self.reader.getNodes(SHTYPE.MULNODE)
        for mulnode in mulnodes:
            nodeId = int(mulnode.find("nodeID").text)
            if nodeId in nodeCoordinates:
                location = mulnode.find("location")
                if location is None:
                    self.addXMLLocation(mulnode, nodeCoordinates[nodeId])
                else:
                    self.updateLocation(location, nodeCoordinates[nodeId])
            else:
                self.warnNonExist("multiNode", nodeId)

    def updateLane(self, segmentId, lane):
        laneCoordinates = self.reader.getSegmentComponents(SHTYPE.LANE, int(segmentId))
        laneID = int(lane.find("laneID").text)
        polyline = lane.find("PolyLine")
        if laneID in laneCoordinates:
            if polyline is None:
                polyline = ElementTree.SubElement(lane, 'PolyLine')
            for polyPoint in polyline.findall('PolyPoint'):
                polyline.remove(polyPoint)
            index = 0
            for point in laneCoordinates[laneID]:
                polyPoint = ElementTree.SubElement(polyline, 'PolyPoint')
                ElementTree.SubElement(polyPoint, 'pointID').text = str(index)
                self.addXMLLocation(polyPoint, point)
                index = index + 1
        else:
            self.warnNonExist("lane", segmentId)
    
    def updateLaneEdge(self, segmentId, laneEdge):
        laneEdgeCoordinates = self.reader.getSegmentComponents(SHTYPE.LANEEDGE, int(segmentId))
        laneNumber = int(laneEdge.find("laneNumber").text)
        polyline = laneEdge.find("polyline")
        if laneNumber in laneEdgeCoordinates:
            if polyline is None:
                polyline = ElementTree.SubElement(laneEdge, 'polyline')
            for polyPoint in polyline.findall('PolyPoint'):
                polyline.remove(polyPoint)
            index = 0
            for point in laneEdgeCoordinates[laneNumber]:
                polyPoint = ElementTree.SubElement(polyline, 'PolyPoint')
                ElementTree.SubElement(polyPoint, 'pointID').text = str(index)
                self.addXMLLocation(polyPoint, point)
                index = index + 1
        else:
            self.warnNonExist("laneEdge", segmentId)

    def updateCrossing(self, segmentId, crossing):
        crossCoordinates = self.reader.getSegmentComponents(SHTYPE.CROSSING, int(segmentId))
        crossingId = int(crossing.find("id").text)
        if crossingId in crossCoordinates:
            coordinates = crossCoordinates[crossingId][0]
            nearLine = crossing.find("nearLine")
            if nearLine is None:
                nearLine = ElementTree.SubElement(crossing, 'nearLine')
                ElementTree.SubElement(nearLine, 'first')
                ElementTree.SubElement(nearLine, 'second')
            self.updateLocation(nearLine.find('first'), coordinates[0])
            self.updateLocation(nearLine.find('second'), coordinates[1])
            farLine = crossing.find("farLine")
            if farLine is None:
                farLine = ElementTree.SubElement(crossing, 'farLine')
                ElementTree.SubElement(farLine, 'first')
                ElementTree.SubElement(farLine, 'second')
            self.updateLocation(farLine.find('first'), coordinates[3])
            self.updateLocation(farLine.find('second'), coordinates[2])            
        else:
            self.warnNonExist("crossing", crossingId)     

    def updateBusstop(self, segmentId, busstop):
        busstopCoordinates = self.reader.getSegmentComponents(SHTYPE.BUSSTOP, int(segmentId))
        busstopId = int(busstop.find("id").text)
        if busstopId in busstopCoordinates:
           pos = busstopCoordinates[busstopId]
           self.updateLocation(busstop, pos) 
        else:
            self.warnNonExist("Busstop", busstopId)   

    def updateSegment(self, linkId, segment):
        segmentCoordinates = self.reader.getSegmentsByLinkId(int(linkId))
        segmentID = int(segment.find("segmentID").text)
        polyline = segment.find("polyline")
        if polyline is None:
            polyline = ElementTree.SubElement(segment, 'polyline')
        #update segment
        if segmentID in segmentCoordinates:
            for polyPoint in polyline.findall('PolyPoint'):
                polyline.remove(polyPoint)
            segmentCoordinate = segmentCoordinates[segmentID][0]
            for index in range(0, len(segmentCoordinate)-1):
                point = segmentCoordinate[index]
                polyPoint = ElementTree.SubElement(polyline, 'PolyPoint')
                ElementTree.SubElement(polyPoint, 'pointID').text = str(index)
                self.addXMLLocation(polyPoint, point)
        else:
            self.warnNonExist("segment", segmentID)
        #update lanes
        lanes = segment.find("Lanes")
        if lanes is not None:
            for lane in lanes.findall('Lane'):
                self.updateLane(segmentID, lane)
        #update laneEdge
        laneEdges = segment.find("laneEdgePolylines_cached")
        if laneEdges is not None:
            for laneEdge in laneEdges.findall('laneEdgePolyline_cached'):
                self.updateLaneEdge(segmentID, laneEdge)
        #update obstacles
        obstacles = segment.find("Obstacles")
        if obstacles is not None:
            for obstacle in obstacles.iter():
                if obstacle.tag == "Crossing":
                    self.updateCrossing(segmentID, obstacle)
                elif obstacle.tag == "BusStop":
                    self.updateBusstop(segmentID, obstacle)

    def writePrettyToXml(self):
        roughString = ElementTree.tostring(self.document.getroot(), 'utf-8')
        reparsed = minidom.parseString(roughString)
        pretty_string =  '\n'.join([line for line in reparsed.toprettyxml(indent=' '*4).split('\n') if line.strip()])
        xmlFile = open(self.xmlPath, 'w')
        xmlFile.write(pretty_string)
        xmlFile.close()

    def run(self):
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        #update nodes
        nodes = roadNetwork.find('Nodes')
        if nodes is not None:
            uninodes = nodes.find('UniNodes')
            if uninodes is not None:
                self.updateUninodes(uninodes.findall('UniNode'))
        self.prog_sig.emit(25)
        if nodes is not None:
            multinodes = nodes.find('Intersections')
            if multinodes is not None:
                self.updateMulnodes(multinodes.findall('Intersection'))
        self.prog_sig.emit(50)
        #update segment
        linksParent = roadNetwork.find('Links')
        if linksParent is not None:
            links = linksParent.findall('Link')
            count = len(links)
            progPercent = 50
            for link in links:
                segments = link.find('Segments')
                linkId = link.find('linkID').text
                for segment in segments.findall('Segment'):
                    self.updateSegment(linkId, segment)
                progPercent = progPercent + 25.0/count
                self.prog_sig.emit(progPercent)
        self.writePrettyToXml()
        self.prog_sig.emit(100)
