import os
from PyQt4.QtCore import *
from qgis.core import *

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Constants
TYPE = enum('MULNODE', 'SEGMENT', 'TURNINGPATH', 'LANE', 'CROSSING', 'BUSSTOP', 'LANEEDGE')
TAGS = {TYPE.MULNODE: "mulnode", TYPE.SEGMENT: "segment", TYPE.TURNINGPATH: "turningPath",
        TYPE.LANE: "lane", TYPE.CROSSING: "crossing", TYPE.BUSSTOP: "busstop", TYPE.LANEEDGE: "laneedge"}
SCHEMA = {}
SCHEMA[TYPE.MULNODE] = [QGis.WKBPoint, [QgsField("id", QVariant.Int)]] 
SCHEMA[TYPE.SEGMENT] = [QGis.WKBLineString, [QgsField("link-id", QVariant.Int), QgsField("segmentID", QVariant.Int)]]
SCHEMA[TYPE.TURNINGPATH] = [QGis.WKBLineString, [QgsField("turningPathID", QVariant.Int)]]
SCHEMA[TYPE.LANE]    = [QGis.WKBLineString, [QgsField("segmentID", QVariant.Int), QgsField("laneID", QVariant.Int)]]
SCHEMA[TYPE.CROSSING]= [QGis.WKBPolygon, [QgsField("segmentID", QVariant.Int), QgsField("id", QVariant.Int)]]
SCHEMA[TYPE.BUSSTOP] = [QGis.WKBPoint, [QgsField("segmentID", QVariant.Int), QgsField("id", QVariant.Int)]]    
SCHEMA[TYPE.LANEEDGE]= [QGis.WKBLineString, [QgsField("segmentID", QVariant.Int), QgsField("number", QVariant.Int)]] 

class ShapefileWriter:
    def __init__(self, path):
        self.path = path
        self.prefix = os.path.basename(path)
        self.layer = {}

        for typeid, tag in TAGS.iteritems():
            fields = QgsFields()
            for field in SCHEMA[typeid][1]:
                fields.append(field)
            dest = os.path.join(self.path, "%s_%s"%(self.prefix, tag))
            crs = QgsCoordinateReferenceSystem(3168)
            self.layer[typeid] = QgsVectorFileWriter(dest, "UTF-8", fields, SCHEMA[typeid][0], crs, "ESRI Shapefile")
            if self.layer[typeid].hasError() != QgsVectorFileWriter.NoError:
                QgsMessageLog.logMessage("Error: unable to create layer writer")
        
    def addPoint(self, typeid, point, attr):       
        if SCHEMA[typeid][0] == QGis.WKBPoint:
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPoint(point))
            fet.setAttributes(attr)
            self.layer[typeid].addFeature(fet)

    def addPolygon(self, typeid, coordinates, attr):      
        if SCHEMA[typeid][0] == QGis.WKBPolygon:
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPolygon([coordinates]))
            fet.setAttributes(attr)
            self.layer[typeid].addFeature(fet)          

    def addPolyline(self, typeid, coordinates, attr):     
        if SCHEMA[typeid][0] == QGis.WKBLineString:
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPolyline(coordinates))
            fet.setAttributes(attr)
            self.layer[typeid].addFeature(fet)

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        #save to shapefiles 
        for typeid, tag in TAGS.iteritems():
            del self.layer[typeid]


class ShapefileReader:
    def __init__(self, path):
        self.path = path
        self.prefix = os.path.basename(path)
        self.layer = {}
        self.data = {}
        for typeid, tag in TAGS.iteritems():
            filepath = os.path.join(self.path, "%s_%s.shp" % (self.prefix, tag))
            if os.path.isfile(filepath):
                self.layer[typeid] = QgsVectorLayer(filepath, "%s_isim"%typeid, "ogr")
            else:
                self.layer[typeid] = None
            self.loadData(typeid)
            

    def loadData(self, typeid):
        self.data[typeid] = {}
        if self.layer[typeid] == None:
            return

        features = self.layer[typeid].getFeatures()
        # load node
        if typeid == TYPE.MULNODE:
            for feature in features:
                attr = feature.attributes()
                self.data[typeid][attr[0]] = feature.geometry().asPoint()
        else:
            for feature in features:
                attr = feature.attributes()
                if attr[0] not in self.data[typeid]:
                    self.data[typeid][attr[0]] = {}

                if typeid == TYPE.CROSSING:
                    self.data[typeid][attr[0]][attr[1]] = feature.geometry().asPolygon()
                elif typeid == TYPE.BUSSTOP:
                    self.data[typeid][attr[0]][attr[1]] = feature.geometry().asPoint()
                else:
                    self.data[typeid][attr[0]][attr[1]] = feature.geometry().asPolyline()


    def getNodes(self, typeId):
        return self.data[typeId]

    def getSegmentsByLinkId(self, linkId):
        return self.data[TYPE.SEGMENT][linkId]

    def getSegmentComponents(self, typeId, segmentId):
        return self.data[typeId][segmentId]
