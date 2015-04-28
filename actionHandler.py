import os, re
from xml.etree import ElementTree
from xml.dom import minidom
from shapefileIO import TAGS, TYPE
from qgis.core import *
from PyQt4 import QtCore, QtGui

def getSHTypeFromLayername(layer_name):
    parts = layer_name.split("_")
    if len(parts) < 2:
        return 0
    for typeid, tag in TAGS.iteritems():
        if parts[1] == tag:
            return typeid
    return 0

class ActionHandler():
    def __init__(self, sh_dir, canvas):
        ElementTree.register_namespace('geo', "http://www.smart.mit.edu/geo")
        self.sh_dir = sh_dir
        self.data_path = os.path.join(sh_dir, "data.xml")
        self.document = ElementTree.parse(self.data_path)
        self.layers = {}
        self.active_layer = canvas.currentLayer()
        self.active_layer_id = 0

        # add all layers
        for layer in canvas.layers():
            self.layers[getSHTypeFromLayername(layer.name())] = layer

        # current layer
        current_layer_name = self.active_layer.name()
        self.prefix = current_layer_name.split("_")[0]
        self.active_layer_id = getSHTypeFromLayername(current_layer_name)

    def getLayer(self, typeId):
        if typeId not in self.layers:
            QgsMessageLog.logMessage("load file type %s"%typeId, 'SimGDC')
            full_path = os.path.join(self.sh_dir, "%s_%s.shp"%(self.prefix, TAGS[typeId]))
            self.layers[typeId] = QgsVectorLayer(full_path, "%s_isim"%typeId, "ogr")
        return self.layers[typeId]


    def addMultiNode(self, point, nodeData):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes (1)
        feat.setAttribute(0, nodeData["id"])
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point.x(),point.y())))
        self.active_layer.dataProvider().addFeatures([feat])
        '''ADD TO data.xml '''
        roadNetwork = self.document.find('geospatial/road_network')
        nodes = roadNetwork.find('nodes')
        node = ElementTree.SubElement(nodes, 'node')
        #add Id
        ElementTree.SubElement(node, 'id').text = str(nodeData["id"])
        #addType
        ElementTree.SubElement(node, 'node_type').text = str(nodeData["nodeType"])
        #addTrafficLightId
        ElementTree.SubElement(node, 'traffic_light_id').text = str(nodeData["trafficLightID"])
        #addTags
        ElementTree.SubElement(node,'tags').text = str(nodeData["tags"])
        #addTurningGroup
        turningGroupParent = ElementTree.SubElement(node, 'turning_groups')

        #if nodeData["turningGroup"]:
        for tG in nodeData["turningGroup"]:
            turningGroup = ElementTree.SubElement(turningGroupParent, 'turning_group')
            ElementTree.SubElement(turningGroup, 'id').text = str(tG[0])
            ElementTree.SubElement(turningGroup, 'from_link').text = str(tG[1])
            ElementTree.SubElement(turningGroup, 'to_link').text = str(tG[2])
            ElementTree.SubElement(turningGroup, 'phases').text = str(tG[3])
            ElementTree.SubElement(turningGroup, 'rules').text = str(tG[4])
            ElementTree.SubElement(turningGroup, 'visibility').text = str(tG[5])
            ElementTree.SubElement(turningGroup, 'tags').text = str(tG[6])
            if nodeData["turningPath"]:
                turningPathParent = ElementTree.SubElement(turningGroup, 'turning_paths')
                for tP in nodeData["turningPath"]:
                    if tP[0] == tG[0]:
                        turningPath = ElementTree.SubElement(turningPathParent, 'turning_path')
                        ElementTree.SubElement(turningPath, 'groupID').text = str(tP[0])
                        ElementTree.SubElement(turningPath, 'id').text = str(tP[1])
                        ElementTree.SubElement(turningPath, 'from_lane').text = str(tP[2])
                        ElementTree.SubElement(turningPath, 'to_lane').text = str(tP[3])
                        ElementTree.SubElement(turningPath, 'max_speed').text = str(tP[4])
                        ElementTree.SubElement(turningPath, 'tags').text = str(tP[5])



        #add location
        point = ElementTree.SubElement(multiNode, 'point')
        ElementTree.SubElement(point, 'x').text = str(feat.geometry().asPoint().x())
        ElementTree.SubElement(point, 'y').text = str(feat.geometry().asPoint().y())
        ElementTree.SubElement(point, 'z').text = str(feat.geometry().asPoint().z())
        #add originalDB_ID
        # ElementTree.SubElement(multiNode, 'originalDB_ID').text = "\"aimsun-id\":\"%s\""%str(nodeData["aimsunId"])
        # #add roadSegmentsAt
        # roadSegmentsAt = ElementTree.SubElement(multiNode, 'roadSegmentsAt')
        # for roadSegment in nodeData["roadSegments"]:
        #     ElementTree.SubElement(roadSegmentsAt, 'segmentID').text = str(roadSegment)
        # #add connectors
        # connectorsEle = ElementTree.SubElement(multiNode, 'Connectors')
        # for multiConnector in nodeData["multiConnectors"]:
        #     multiConnectorEle = ElementTree.SubElement(connectorsEle, 'MultiConnectors')
        #     ElementTree.SubElement(multiConnectorEle, 'RoadSegment').text = str(multiConnector[0])
        #     connectors = ElementTree.SubElement(multiConnectorEle, 'Connectors')
        #     for innerConnector in multiConnector[1]:
        #         connector = ElementTree.SubElement(connectors, 'Connector')
        #         ElementTree.SubElement(connector, 'laneFrom').text = str(innerConnector[0])
        #         ElementTree.SubElement(connector, 'laneTo').text = str(innerConnector[1])


    def updateMultiNode(self, feature, nodeData):
        #update feature if necessary
        attrs = feature.attributes()
        id = int(attrs[0])
        if id != nodeData["id"]:
            attrs = {0 : nodeData["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        nodeparent = roadNetwork.find('nodes')
        nodes = nodeparent.findall('node')
        selectedNode = None
        if nodes is not None:
            for node in nodes:
                nodeId = int(node.find("id").text)
                if nodeId == id:
                    selectedNode = node
                    break
        if selectedNode is None:
            QgsMessageLog.logMessage("updateMultiNode not find node id %s"%id, 'SimGDC')
            return
        #update id
        selectedNode.find("id").text = str(nodeData["id"])
        #update type
        selectedNode.find("node_type").text = str(nodeData["nodeType"])

        #addTrafficLightID
        selectedNode.find("traffic_light_id").text = str(nodeData["trafficLightID"])

        #add Tags
        selectedNode.find("tags").text = str(nodeData["tags"])

        #addTurningGroup
        turningGroupParent = selectedNode.find("turning_groups")

        for tG in turningGroupParent.findall('turning_group'):
            turningGroupParent.remove(tG)
        for tG in selectedNode.findall('turning_group'):
            msgBox = QtGui.QMessageBox()
            msgBox.setText(tG.text)
            msgBox.exec_()
            return
        # for tG in nodeData["turningGroup"]:
        #     turningGroup = ElementTree.SubElement(turningGroup.text = str(tG[1])
        #     ElementTree.SubElement(turningGroup, 'toLink').text = str(tG[2])
        #     ElementTree.SubElement(turningGroup, 'Phases').text = str(tG[3])
        #     ElementTree.SubElement(turningGroup, 'Rules').text = str(tG[4])
        #     if nodeData["turningPath"]:
        #         turningPathParent = ElementTree.SubElement(turningGroup, 'TurningPaths')
        #         for tP in nodeData["turningPath"]:
        #             if tP[0] == tG[0]:
        #                 turningPath = ElementTree.SubElement(turningPathParent, 'TurningPath')
        #                 ElementTree.SubElement(turningPath, 'groupID').text = str(tP[0])
        #                 ElementTree.SubElement(turningPath, 'ID').text = str(tP[1])
        #                 ElementTree.SubElement(turningPath, 'fromLane').text = str(tP[2])
        #                 ElementTree.SubElement(turningPath, 'toLane').text = str(tP[3])


        # i=0
        # for tG in nodeData["turningGroup"]:
        #     j=0
        #     tG.find("ID").text = str(nodeData["turningGroup"][i][0])
        #     tG.find("fromLink").text = str(nodeData["turningGroup"][i][1])
        #     tG.find("toLink").text = str(nodeData["turningGroup"][i][2])
        #     tG.find("Phases").text = str(nodeData["turningGroup"][i][3])
        #     tG.find('Rules').text = str(nodeData["turningGroup"][i][4])
        #     for tP in nodeData["turningPath"]:
        #         if str(nodeData["turningGroup"][i][0]) == str(nodeData["turningPath"][j][0]):
        #             tP.find("groupID").text = str(nodeData["turningPath"][j][0])
        #             tP.find("ID").text = str(nodeData["turningPath"][j][1])
        #             tP.find("fromLane").text = str(nodeData["turningPath"][j][2])
        #             tP.find("toLane").text = str(nodeData["turningPath"][j][3])
        #         j+=1
        #     i+=1

        #update aimsunId
        # selectedNode.find("originalDB_ID").text = "\"aimsun-id\":\"%s\""%str(nodeData["aimsunId"])




    def getMultiNode(self, feature):
        #get id from feature
        attrs = feature.attributes()
        id = int(attrs[0])   
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        nodeparent = roadNetwork.find('nodes')
        nodes = nodeparent.findall('node')
        selectedNode = None
        if nodes is not None:
            for node in nodes:
                nodeId = int(node.find("id").text)
                if nodeId == id:
                    selectedNode = node
                    break
        if selectedNode is not None:
            info = {}
            info["id"] = selectedNode.find("id").text
            # aimsunIdStr = selectedNode.find("originalDB_ID").text
            # aimsunIds = re.findall(r'[0-9]+', aimsunIdStr)
            # info["aimsunId"] = aimsunIds[0]
            info["nodeType"] = selectedNode.find("node_type").text
            info["trafficLightID"] = selectedNode.find("traffic_light_id").text


        turningGroups = selectedNode.find("turning_groups")

        turningGroup = turningGroups.findall("turning_group")

        info["turningGroup"] = []
        info["turningPath"] = []

        if turningGroup:
        #     msgBox = QtGui.QMessageBox()
        #     msgBox.setText(turningGroup[0].find("ID").text)
        #     msgBox.exec_()
        #     return
            for tG in turningGroup:
                info["turningGroup"].append([tG.find("id").text,tG.find("from_link").text,tG.find("to_link").text,tG.find("phases").text,tG.find("rules").text,tG.find("visibility"),tG.find("tags")])
                # turningPaths = turningGroups.findall("TurningPath")
                # if turningPaths:
                for tP in selectedNode.iter('turning_path'):
                    if tP.find("groupID").text == tG.find("id").text:
                        # info["turningPath"].append(tP)
                        info["turningPath"].append([tP.find("groupID").text,tP.find("id").text,tP.find("from_lane").text,tP.find("to_lane").text,tP.find("max_speed").text,tP.find("tags").text])



            # info["roadSegmentsAt"] = None
            # roadSegmentsAt = selectedNode.find("roadSegmentsAt")
            # if roadSegmentsAt is not None:
            #     info["roadSegmentsAt"] = []
            #     for segmentID in roadSegmentsAt.findall('segmentID'):
            #         info["roadSegmentsAt"].append(segmentID.text)
            # info["connectors"] = None
            # connectors = selectedNode.find("Connectors")
            # if connectors is not None:
            #     info["connectors"] = []
            #     for multiConnector in connectors.findall('MultiConnectors'):
            #         roadSegment = multiConnector.find("RoadSegment").text
            #         innerConnectors = []
            #         for innerConnector in multiConnector.find("Connectors"):
            #             innerConnectors.append("%s,%s"%(innerConnector.find("laneFrom").text,innerConnector.find("laneTo").text))
            #         info["connectors"].append([roadSegment, innerConnectors])
            return info
        return None    


    def getLinkList(self):
        listLinks = {}
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                linkName = link.find("road_name").text
                listLinks[linkId] = linkName
        return listLinks

    def getLinkListDetail(self):
        listLinks = {}
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                linkName = link.find("road_name").text
                startNode = int(link.find("from_node").text)
                endNode = int(link.find("to_node").text)
                listLinks[linkId] = [linkId, linkName, startNode, endNode]
        return listLinks

    def manageLink(self, data):
        if data["oldId"] < 1:
            #add new
            roadNetwork = self.document.find('geospatial/road_network')
            linkParent = roadNetwork.find('links')
            if linkParent is None:
                linkParent = ElementTree.SubElement(roadNetwork, 'links')
            link = ElementTree.SubElement(linkParent, 'link')
            ElementTree.SubElement(link, 'id').text = str(data["id"])
            ElementTree.SubElement(link, 'road_name').text = str(data["roadName"])
            ElementTree.SubElement(link, 'from_node').text = str(data["startingNode"])
            ElementTree.SubElement(link, 'to_node').text = str(data["endingNode"])
            ElementTree.SubElement(link, 'segments')
        else:
            roadNetwork = self.document.find('geospatial/road_network')
            linkParent = roadNetwork.find('links')
            links = linkParent.findall('link')
            selectedLink = None
            if links is not None:
                for link in links:
                    linkId = int(link.find("id").text)
                    if linkId == data["oldId"]:
                        selectedLink = link
                        break
            #update info
            selectedLink.find("id").text = str(data["id"])
            selectedLink.find("road_name").text = str(data["roadName"])
            selectedLink.find("from_node").text = str(data["startingNode"])
            selectedLink.find("to_node").text = str(data["endingNode"])
            #update segment layer when the id is changed
            if data["id"] != data["oldId"]:
                segmentLayer = self.getLayer(TYPE.SEGMENT)
                for feature in segmentLayer.getFeatures():
                    attrs = feature.attributes()
                    if attrs[0] == data["oldId"]:
                        attrs = {0 : data["id"], 1: attrs[1]}
                        self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })


    def addSegment(self, point, data):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes(2)
        distance = 1000
        #coordinates = [QgsPoint(point.x(),point.y()), QgsPoint(point.x(), point.y() + distance), QgsPoint(point.x() + 2*distance, point.y() + distance), QgsPoint(point.x() + 2*distance, point.y())]
        coordinates = [QgsPoint(point.x(),point.y()), QgsPoint(point.x() + distance, point.y() + distance)]
        feat.setAttribute(0, data["linkId"])
        feat.setAttribute(1, data["id"])
        feat.setGeometry(QgsGeometry.fromPolyline(coordinates))
        self.active_layer.dataProvider().addFeatures([feat])
        '''ADD TO data.xml '''
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedLink = None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                if linkId == data["linkId"]:
                    selectedLink = link
                    break
        if selectedLink is not None:
            segments = selectedLink.find("segments")
            if segments is None:
                segments = ElementTree.SubElement(selectedLink, 'segments')
            segment = ElementTree.SubElement(segments, 'segment')
            #add Info
            ElementTree.SubElement(segment, 'id').text = str(data["id"])
            ElementTree.SubElement(segment, 'sequence_num').text = str(data["sequence_num"])
            ElementTree.SubElement(segment, 'capacity').text = str(data["capacity"])
            ElementTree.SubElement(segment, 'max_speed').text = str(data["max_speed"])
            ElementTree.SubElement(segment, 'tags').text = str(data["tags"])
            connectors = ElementTree.SubElement(selectedLink, 'connectors')
            connector = ElementTree.SubElement(connectors, 'connector')
            for conn in data["connectors"]:
                ElementTree.SubElement(connector, 'id').text = str(conn[0])
                ElementTree.SubElement(connector, 'from_section').text = str(conn[1])
                ElementTree.SubElement(connector, 'to_section').text = str(conn[2])
                ElementTree.SubElement(connector, 'from_lane').text = str(conn[3])
                ElementTree.SubElement(connector, 'to_lane').text = str(conn[4])

        polyline = ElementTree.SubElement(segment, 'polyline')
        points = ElementTree.SubElement(polyline, 'points')

        coordinates = str(feat.geometry().asPolyline().asPoint.x())             #need to find a way to get the points

        for pt in coordinates:
            point = ElementTree.SubElement(points, 'point')
            ElementTree.SubElement(point, 'x').text = pt[0]
            ElementTree.SubElement(point, 'y').text = pt[1]
            ElementTree.SubElement(point, 'z').text = pt[2]

    def updateSegment(self, feature, data):
        #update feature if necessary
        attrs = feature.attributes()
        oldLinkId = int(attrs[0])
        oldSegmentId = int(attrs[1])
        if oldLinkId != data["linkId"] or oldSegmentId != data["id"]:
            attrs = {0 : data["linkId"], 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedLink = None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                if linkId == data["linkId"]:
                    selectedLink = link
                    break
        selectedSegment= None
        oldLinkSegments = None
        newLinkSegments = None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                if linkId == data["linkId"]:
                    newLinkSegments = link.find("segments")
                if linkId == oldLinkId:
                    oldLinkSegments = link.find("segments")
                    segments = oldLinkSegments.findall("segment")
                    for segment in segments:
                        segmentId = int(segment.find("id").text)
                        if segmentId == oldSegmentId:
                            selectedSegment = segment
        if selectedSegment is None:
            QgsMessageLog.logMessage("updateSegment can not find segment id %s"%str(oldSegmentId), 'SimGDC')
            return
        #update info
        selectedSegment.find("id").text = str(data["id"])
        selectedSegment.find("sequence_num").text = str(data["sequence_num"])
        selectedSegment.find("capacity").text = str(data["capacity"])
        selectedSegment.find("max_speed").text = str(data["max_speed"])
        selectedSegment.find("tags").text = str(data["tags"])

        connectorsroot = selectedLink.find("connectors").text
        connectors = connectorsroot.findall("connector")
        for conn in connectors:
            conn.find("id").text = str(conn[0])
            conn.find("from_section").text = str(conn[1])
            conn.find("to_section").text = str(conn[2])
            conn.find("from_lane").text = str(conn[3])
            conn.find("to_lane").text = str(conn[4])

        #move to new link if necessary
        if oldLinkId != data["linkId"]:
            oldLinkSegments.remove(selectedSegment)
            newLinkSegments.append(selectedSegment)

    def getSegment(self, feature):
        #get id from feature
        attrs = feature.attributes()
        selectedLinkId = int(attrs[0])
        selectedSegmentId = int(attrs[1])
        #get info
        listLinks = {}
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedLink = None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                if linkId == data["linkId"]:
                    selectedLink = link
                    break
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                linkName = link.find("road_name").text
                listLinks[linkId] = linkName
                if linkId == selectedLinkId:
                    segments = link.find("segments").findall("segment")
                    for segment in segments:
                        segmentId = int(segment.find("id").text)
                        if segmentId == selectedSegmentId:
                            selectedSegment = segment
        if selectedSegment is not None:
            info = {}
            info["linkId"] = selectedLinkId
            info["id"] = selectedSegment.find("id").text
            # aimsunIdStr = selectedSegment.find("originalDB_ID").text
            # aimsunIds = re.findall(r'[0-9]+', aimsunIdStr)
            # info["aimsunId"] = aimsunIds[0]
            info["sequence_num"] = selectedSegment.find("sequence_num").text
            info["capacity"] = selectedSegment.find("capacity").text
            info["max_speed"] = selectedSegment.find("max_speed").text
            info["tags"] = selectedSegment.find("tags").text
            # info["roadType"] = selectedSegment.find("roadType").text
            # info["category"] = selectedSegment.find("category").text
            info["connectors"] =selectedLink.find("connectors").text
            connectorsroot = selectedLink.find("connectors").text
            connectors = connectorsroot.findall("connector")
            for conn in connectors:
                info["connectors"].append(conn)

            return [listLinks, info]
        return None

    def addCrossing(self, point, data):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes(2)
        distance = 1000
        coordinates = [QgsPoint(point.x(),point.y()), QgsPoint(point.x() + distance,point.y()), QgsPoint(point.x() + distance,point.y() + distance), QgsPoint(point.x(),point.y() + distance)]
        feat.setAttribute(0, data["segmentId"])
        feat.setAttribute(1, data["id"])
        feat.setGeometry(QgsGeometry.fromPolygon([coordinates]))
        self.active_layer.dataProvider().addFeatures([feat])
        '''ADD TO data.xml '''
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    selectedSegment = segment
                    break
        if selectedSegment is not None:
            obstacles = selectedSegment.find("Obstacles")
            if obstacles is None:
                obstacles = ElementTree.SubElement(selectedSegment, 'Obstacles')

            crossing = ElementTree.SubElement(obstacles, 'Crossing')
            #add Info
            ElementTree.SubElement(crossing, 'id').text = str(data["id"])
            ElementTree.SubElement(crossing, 'Offset').text = str(data["offset"])

    def updateCrossing(self, feature, data):
        #update feature if necessary
        attrs = feature.attributes()
        selectedsegmentId = int(attrs[0])
        oldCrossingId = int(attrs[1])
        if oldCrossingId != data["id"]:
            attrs = {0 : selectedsegmentId, 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedCrossing = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedsegmentId:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None: 
                        crossings = obstacles.findall('Crossing')
                        for crossing in crossings:
                            crossingId = int(crossing.find("id").text)
                            if crossingId == oldCrossingId:
                                selectedCrossing = crossing
                    break
        if selectedCrossing is None:
            QgsMessageLog.logMessage("updateCrossing can not find crossing id %s"%str(oldCrossingId), 'SimGDC')
            return
        selectedCrossing.find("id").text = str(data["id"])
        selectedCrossing.find("Offset").text = str(data["offset"])

    def getCrossing(self, feature):
        #get id from feature
        attrs = feature.attributes()
        selectedSegmentId = int(attrs[0])
        selectedCrossingId = int(attrs[1])
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedCrossing = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None: 
                        crossings = obstacles.findall('Crossing')
                        for crossing in crossings:
                            crossingId = int(crossing.find("id").text)
                            if crossingId == selectedCrossingId:
                                selectedCrossing = crossing
                    break
        if selectedCrossing is not None:
            info = {}
            info["segmentId"] = selectedSegmentId
            info["id"] = selectedCrossing.find("id").text
            info["offset"] = selectedCrossing.find("Offset").text
            return info
        return None


    def addBusstop(self, point, data):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes(2)
        feat.setAttribute(0, data["segmentId"])
        feat.setAttribute(1, data["id"])
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point.x(),point.y())))
        self.active_layer.dataProvider().addFeatures([feat])
        '''ADD TO data.xml '''       
         #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    selectedSegment = segment
                    break
        if selectedSegment is not None:
            obstacles = selectedSegment.find("Obstacles")
            if obstacles is None:
                obstacles = ElementTree.SubElement(selectedSegment, 'Obstacles')

            busstop = ElementTree.SubElement(obstacles, 'BusStop')
            #add Info
            ElementTree.SubElement(busstop, 'id').text = str(data["id"])
            ElementTree.SubElement(busstop, 'Offset').text = str(data["offset"])  
            ElementTree.SubElement(busstop, 'is_terminal').text = str(data["isTerminal"])
            ElementTree.SubElement(busstop, 'is_bay').text = str(data["isBay"])     
            ElementTree.SubElement(busstop, 'has_shelter').text = str(data["hasShelter"])  
            ElementTree.SubElement(busstop, 'busCapacityAsLength').text = str(data["busCapacity"])  
            ElementTree.SubElement(busstop, 'busstopno').text = str(data["busstopno"])            

    def updateBusstop(self, feature, data):
         #update feature if necessary
        attrs = feature.attributes()
        selectedsegmentId = int(attrs[0])
        oldBusstopId = int(attrs[1])
        if oldBusstopId != data["id"]:
            attrs = {0 : selectedsegmentId, 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedBusstop = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedsegmentId:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None: 
                        busstops = obstacles.findall('BusStop')
                        for busstop in busstops:
                            busstopId = int(busstop.find("id").text)
                            if busstopId == oldBusstopId:
                                selectedBusstop = busstop
                    break
        if selectedBusstop is None:
            QgsMessageLog.logMessage("updateBusstop can not find busstop id %s"%str(oldBusstopId), 'SimGDC')
            return
        selectedBusstop.find("id").text = str(data["id"])
        selectedBusstop.find("Offset").text = str(data["offset"])
        selectedBusstop.find("is_terminal").text = data["isTerminal"]
        selectedBusstop.find("is_bay").text = data["isBay"]   
        selectedBusstop.find("has_shelter").text = data["hasShelter"]   
        selectedBusstop.find("busCapacityAsLength").text = str(data["busCapacity"])  
        selectedBusstop.find("busstopno").text = str(data["busstopno"])                   

    def getBusstop(self, feature):
         #get id from feature
        attrs = feature.attributes()
        selectedSegmentId = int(attrs[0])
        selectedBusstopId = int(attrs[1])       
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedBusstop = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None: 
                        busstops = obstacles.findall('BusStop')
                        for busstop in busstops:
                            busstopId = int(busstop.find("id").text)
                            if busstopId == selectedBusstopId:
                                selectedBusstop = busstop
                    break
        if selectedBusstop is not None:
            info = {}
            info["segmentId"] = selectedSegmentId
            info["id"] = selectedBusstop.find("id").text
            info["offset"] = selectedBusstop.find("Offset").text
            info["isTerminal"] = selectedBusstop.find("is_terminal").text
            info["isTerminal"] = info["isTerminal"].strip().lower()
            info["isBay"] = selectedBusstop.find("is_bay").text
            info["isBay"] = info["isBay"].strip().lower()
            info["hasShelter"] = selectedBusstop.find("has_shelter").text
            info["hasShelter"] = info["hasShelter"].strip().lower()
            info["busCapacity"] = selectedBusstop.find("busCapacityAsLength").text
            info["busstopno"] = selectedBusstop.find("busstopno").text
            return info
        return None

    def addLane(self, point, data):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes(2)
        distance = 1000
        coordinates = [QgsPoint(point.x(),point.y()), QgsPoint(point.x() + distance,point.y() + distance)]
        feat.setAttribute(0, data["segmentId"])
        feat.setAttribute(1, data["id"])
        feat.setGeometry(QgsGeometry.fromPolyline(coordinates))
        self.active_layer.dataProvider().addFeatures([feat])
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    selectedSegment = segment
                    break
        if selectedSegment is not None:
            laneParent = selectedSegment.find("lanes")
            if laneParent is None:
                laneParent = ElementTree.SubElement(selectedSegment, 'lanes')
            lane = ElementTree.SubElement(laneParent, 'lane')
            ElementTree.SubElement(lane, 'id').text = str(data["id"])
            ElementTree.SubElement(lane, 'width').text = str(data["width"])
            ElementTree.SubElement(lane, 'can_go_straight').text = str(data["can_go_straight"])
            ElementTree.SubElement(lane, 'can_turn_left').text = str(data["can_turn_left"])
            ElementTree.SubElement(lane, 'can_turn_right').text = str(data["can_turn_right"])
            ElementTree.SubElement(lane, 'can_turn_on_red_signal').text = str(data["can_turn_on_red_signal"])
            ElementTree.SubElement(lane, 'can_change_lane_left').text = str(data["can_change_lane_left"])
            ElementTree.SubElement(lane, 'can_change_lane_right').text = str(data["can_change_lane_right"])
            ElementTree.SubElement(lane, 'is_road_shoulder').text = str(data["is_road_shoulder"])
            ElementTree.SubElement(lane, 'is_bicycle_lane').text = str(data["is_bicycle_lane"])
            ElementTree.SubElement(lane, 'is_pedestrian_lane').text = str(data["is_pedestrian_lane"])
            ElementTree.SubElement(lane, 'is_vehicle_lane').text = str(data["is_vehicle_lane"])
            ElementTree.SubElement(lane, 'is_standard_bus_lane').text = str(data["is_standard_bus_lane"])
            ElementTree.SubElement(lane, 'is_whole_day_bus_lane').text = str(data["is_whole_day_bus_lane"])
            ElementTree.SubElement(lane, 'is_high_occupancy_vehicle_lane').text = str(data["is_high_occupancy_vehicle_lane"])
            ElementTree.SubElement(lane, 'can_freely_park_here').text = str(data["can_freely_park_here"])
            ElementTree.SubElement(lane, 'can_stop_here').text = str(data["can_stop_here"])
            ElementTree.SubElement(lane, 'is_u_turn_allowed').text = str(data["is_u_turn_allowed"])
            ElementTree.SubElement(lane, 'tags').text = str(data["tags"])

    def updateLane(self, feature, data):
         #update feature if necessary
        attrs = feature.attributes()
        selectedsegmentId = int(attrs[0])
        oldLaneId = int(attrs[1])
        if oldLaneId != data["id"]:
            attrs = {0 : selectedsegmentId, 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedLane = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedsegmentId:
                    laneParent = segment.find("lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall('lane')
                        for lane in lanes:
                            laneId = int(lane.find("id").text)
                            if laneId == oldLaneId:
                                selectedLane = lane
                    break
        if selectedLane is None:
            QgsMessageLog.logMessage("updateLane can not find the lane id %s"%str(oldLaneId), 'SimGDC')
            return
        selectedLane.find("laneID").text = str(data["id"])
        selectedLane.find("width").text = str(data["width"])
        selectedLane.find("can_go_straight").text = str(data["can_go_straight"])
        selectedLane.find("can_turn_left").text = str(data["can_turn_left"])
        selectedLane.find("can_turn_right").text = str(data["can_turn_right"])
        selectedLane.find("can_turn_on_red_signal").text = str(data["can_turn_on_red_signal"])
        selectedLane.find("can_change_lane_left").text = str(data["can_change_lane_left"])    
        selectedLane.find("can_change_lane_right").text = str(data["can_change_lane_right"])   
        selectedLane.find("is_road_shoulder").text = str(data["is_road_shoulder"])   
        selectedLane.find("is_bicycle_lane").text = str(data["is_bicycle_lane"]) 
        selectedLane.find("is_pedestrian_lane").text = str(data["is_pedestrian_lane"]) 
        selectedLane.find("is_vehicle_lane").text = str(data["is_vehicle_lane"])
        selectedLane.find("is_standard_bus_lane").text = str(data["is_standard_bus_lane"])
        selectedLane.find("is_whole_day_bus_lane").text = str(data["is_whole_day_bus_lane"])
        selectedLane.find("is_high_occupancy_vehicle_lane").text = str(data["is_high_occupancy_vehicle_lane"])
        selectedLane.find("can_freely_park_here").text = str(data["can_freely_park_here"])
        selectedLane.find("can_stop_here").text = str(data["can_stop_here"])
        selectedLane.find("is_u_turn_allowed").text = str(data["is_u_turn_allowed"])
        selectedLane.find("tags").text = str(data["tags"])

    def getLane(self, feature):
         #get id from feature
        attrs = feature.attributes()
        selectedSegmentId = int(attrs[0])
        selectedLaneId = int(attrs[1]) 
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedLane = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    laneParent = segment.find("lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall('lane')
                        for lane in lanes:
                            laneId = int(lane.find("id").text)
                            if laneId == selectedLaneId:
                                selectedLane = lane
                    break
        if selectedLane is not None:
            info = {}
            info["segmentId"] = selectedSegmentId
            info["id"] = selectedLane.find("id").text
            info["width"] = selectedLane.find("width").text 
            info["can_go_straight"] = selectedLane.find("can_go_straight").text
            info["can_go_straight"] = info["can_go_straight"].strip().lower()  
            info["can_turn_left"] = selectedLane.find("can_turn_left").text
            info["can_turn_left"] = info["can_turn_left"].strip().lower()   
            info["can_turn_right"] = selectedLane.find("can_turn_right").text
            info["can_turn_right"] = info["can_turn_right"].strip().lower()  
            info["can_turn_on_red_signal"] = selectedLane.find("can_turn_on_red_signal").text
            info["can_turn_on_red_signal"] = info["can_turn_on_red_signal"].strip().lower()    
            info["can_change_lane_left"] = selectedLane.find("can_change_lane_left").text
            info["can_change_lane_left"] = info["can_change_lane_left"].strip().lower()   
            info["can_change_lane_right"] = selectedLane.find("can_change_lane_right").text
            info["can_change_lane_right"] = info["can_change_lane_right"].strip().lower()  
            info["is_road_shoulder"] = selectedLane.find("is_road_shoulder").text
            info["is_road_shoulder"] = info["is_road_shoulder"].strip().lower() 
            info["is_bicycle_lane"] = selectedLane.find("is_bicycle_lane").text
            info["is_bicycle_lane"] = info["is_bicycle_lane"].strip().lower() 
            info["is_pedestrian_lane"] = selectedLane.find("is_pedestrian_lane").text
            info["is_pedestrian_lane"] = info["is_pedestrian_lane"].strip().lower() 
            info["is_vehicle_lane"] = selectedLane.find("is_vehicle_lane").text
            info["is_vehicle_lane"] = info["is_vehicle_lane"].strip().lower() 
            info["is_standard_bus_lane"] = selectedLane.find("is_standard_bus_lane").text
            info["is_standard_bus_lane"] = info["is_standard_bus_lane"].strip().lower() 
            info["is_whole_day_bus_lane"] = selectedLane.find("is_whole_day_bus_lane").text
            info["is_whole_day_bus_lane"] = info["is_whole_day_bus_lane"].strip().lower() 
            info["is_high_occupancy_vehicle_lane"] = selectedLane.find("is_high_occupancy_vehicle_lane").text
            info["is_high_occupancy_vehicle_lane"] = info["is_high_occupancy_vehicle_lane"].strip().lower() 
            info["can_freely_park_here"] = selectedLane.find("can_freely_park_here").text
            info["can_freely_park_here"] = info["can_freely_park_here"].strip().lower() 
            info["can_stop_here"] = selectedLane.find("can_stop_here").text
            info["can_stop_here"] = info["can_stop_here"].strip().lower() 
            info["is_u_turn_allowed"] = selectedLane.find("is_u_turn_allowed").text
            info["is_u_turn_allowed"] = info["is_u_turn_allowed"].strip().lower()
            info["tags"] = selectedLane.find("tags").text

            return info
        return None

    def addLaneEdge(self, point, data):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes(2)
        distance = 1000
        coordinates = [QgsPoint(point.x(),point.y()), QgsPoint(point.x() + distance,point.y() + distance)]
        feat.setAttribute(0, data["segmentId"])
        feat.setAttribute(1, data["laneNumber"])
        feat.setGeometry(QgsGeometry.fromPolyline(coordinates))
        self.active_layer.dataProvider().addFeatures([feat])
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    selectedSegment = segment
                    break
        if selectedSegment is not None:
            laneEdgeParent = selectedSegment.find("laneEdgePolylines_cached")
            if laneEdgeParent is None:
                laneEdgeParent = ElementTree.SubElement(selectedSegment, 'laneEdgePolylines_cached')
            laneEdge = ElementTree.SubElement(laneEdgeParent, 'laneEdgePolyline_cached')
            ElementTree.SubElement(laneEdge, 'laneNumber').text = str(data["laneNumber"])

    def updateLaneEdge(self, feature, data):
         #update feature if necessary
        attrs = feature.attributes()
        selectedsegmentId = int(attrs[0])
        oldLaneEdgeNumber = int(attrs[1])
        if oldLaneEdgeNumber != data["laneNumber"]:
            attrs = {0 : selectedsegmentId, 1: data["laneNumber"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedLaneEdge = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedsegmentId:
                    laneEdgeParent = segment.find("laneEdgePolylines_cached")
                    if laneEdgeParent is not None:
                        laneEdges = laneEdgeParent.findall('laneEdgePolyline_cached')
                        for laneEdge in laneEdges:
                            laneEdgeNumber = int(laneEdge.find("laneNumber").text)
                            if laneEdgeNumber == oldLaneEdgeNumber:
                                selectedLaneEdge = laneEdge
                    break
        if selectedLaneEdge is None:
            QgsMessageLog.logMessage("updateLaneEdge can not find the lane edge number %s"%str(oldLaneEdgeNumber), 'SimGDC')
            return
        selectedLaneEdge.find("laneNumber").text = str(data["laneNumber"])

    def getLaneEdge(self, feature):
        #get id from feature
        attrs = feature.attributes()
        selectedSegmentId = int(attrs[0])
        selectedLaneEdgeNumber = int(attrs[1])
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        selectedLaneEdge = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("id").text)
                if segmentId == selectedSegmentId:
                    laneEdgeParent = segment.find("laneEdgePolylines_cached")
                    if laneEdgeParent is not None:
                        laneEdges = laneEdgeParent.findall('laneEdgePolyline_cached')
                        for laneEdge in laneEdges:
                            laneNumber = int(laneEdge.find("laneNumber").text)
                            if laneNumber == selectedLaneEdgeNumber:
                                selectedLaneEdge = laneEdge
                    break
        if selectedLaneEdge is not None:
            info = {}
            info["segmentId"] = selectedSegmentId
            info["laneNumber"] = int(selectedLaneEdge.find("laneNumber").text)
            return info
        return None         

    def generateLaneByNumber(self, feature, nLane):
        #find segment
        attrs = feature.attributes()
        selectedLinkId = int(attrs[0])
        selectedSegmentId = int(attrs[1])
        selectedPolyline = feature.geometry().asPolyline()
        listPoints = selectedPolyline[0]
        gapXTop = (listPoints[1].x() - listPoints[0].x())/nLane
        gapYTop = (listPoints[1].y() - listPoints[0].y())/nLane
        gapXBottom = (listPoints[2].x() - listPoints[3].x())/nLane
        gapYBottom = (listPoints[2].y() - listPoints[3].y())/nLane
        QgsMessageLog.logMessage("test (%s, %s)"%(str(listPoints[0].x()), str(listPoints[0].y())), 'SimGDC')
        #get info
        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        links = linkParent.findall('link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("id").text)
                if linkId == selectedLinkId:
                    segments = link.find("segments").findall("segment")
                    for segment in segments:
                        segmentId = int(segment.find("id").text)
                        if segmentId == selectedSegmentId:
                            selectedSegment = segment
        if selectedSegment is None:
            QgsMessageLog.logMessage("selectedSegment not find segment id %s"%str(selectedSegmentId), 'SimGDC')
            return
        laneEdgeLayer = self.getLayer(TYPE.LANEEDGE)
        laneEdges = selectedSegment.find("laneEdgePolylines_cached")
        if laneEdges is not None:
            selectedSegment.remove(laneEdges)
            #delete features from shapefile layer
            delete_lane_edge_feature_ids = []
            for feature in laneEdgeLayer.getFeatures():
                attrs = feature.attributes()
                if attrs[0] == selectedSegmentId:
                    delete_lane_edge_feature_ids.append(feature.id())
            if len(delete_lane_edge_feature_ids) > 0:
                laneEdgeLayer.dataProvider().deleteFeatures(delete_lane_edge_feature_ids)

        #add laneEdge
        laneEdges = ElementTree.SubElement(selectedSegment, 'laneEdgePolylines_cached')
        for num in range(0, nLane+1):
            laneEdge = ElementTree.SubElement(laneEdges, 'laneEdgePolyline_cached')
            ElementTree.SubElement(laneEdge, 'laneNumber').text = str(num)
            #add laneEdge shape
            feat = QgsFeature()
            feat.initAttributes(2)
            coordinates = None
            if num == 0:
                coordinates = [QgsPoint(listPoints[0]), QgsPoint(listPoints[3])]
            elif num == nLane:
                coordinates = [QgsPoint(listPoints[1]), QgsPoint(listPoints[2])]
            else:
                coordinates = [QgsPoint(listPoints[0].x() + gapXTop*num, listPoints[0].y() + gapYTop*num), QgsPoint(listPoints[3].x() + gapXBottom*num, listPoints[3].y() + gapYBottom*num)]
            feat.setAttribute(0, selectedSegmentId)
            feat.setAttribute(1, num)
            feat.setGeometry(QgsGeometry.fromPolyline(coordinates))
            laneEdgeLayer.dataProvider().addFeatures([feat])

        #remove old lanes
        lanes = selectedSegment.find("Lanes")
        laneLayer = self.getLayer(TYPE.LANE)
        if lanes is not None:
            selectedSegment.remove(lanes)
            #delete features from shapefile layer
            delete_lane_feature_ids = []
            for feature in laneLayer.getFeatures():
                attrs = feature.attributes()
                if attrs[0] == selectedSegmentId:
                    delete_lane_feature_ids.append(feature.id())
            if len(delete_lane_feature_ids) > 0:
                laneLayer.dataProvider().deleteFeatures(delete_lane_feature_ids)
        #add lanes
        lanes = ElementTree.SubElement(selectedSegment, 'lanes')
        for num in range(0, nLane):
            lane = ElementTree.SubElement(lanes, 'lane')
            laneId = "%s%s"%(str(selectedSegmentId), str(num))
            ElementTree.SubElement(lane, 'id').text = laneId
            ElementTree.SubElement(lane, 'width').text = "100"
            ElementTree.SubElement(lane, 'can_go_straight').text = "false"                       
            ElementTree.SubElement(lane, 'can_turn_left').text = "false" 
            ElementTree.SubElement(lane, 'can_turn_right').text = "false" 
            ElementTree.SubElement(lane, 'can_turn_on_red_signal').text = "false"
            ElementTree.SubElement(lane, 'can_change_lane_left').text = "false"
            ElementTree.SubElement(lane, 'can_change_lane_right').text = "false"
            ElementTree.SubElement(lane, 'is_road_shoulder').text = "false"
            ElementTree.SubElement(lane, 'is_bicycle_lane').text = "false"
            ElementTree.SubElement(lane, 'is_pedestrian_lane').text = "false"
            ElementTree.SubElement(lane, 'is_vehicle_lane').text = "false"
            ElementTree.SubElement(lane, 'is_standard_bus_lane').text = "false"
            ElementTree.SubElement(lane, 'is_whole_day_bus_lane').text = "false"
            ElementTree.SubElement(lane, 'is_high_occupancy_vehicle_lane').text = "false"
            ElementTree.SubElement(lane, 'can_freely_park_here').text = "false"
            ElementTree.SubElement(lane, 'can_stop_here').text = "false"      
            ElementTree.SubElement(lane, 'is_u_turn_allowed').text = "false"
            #add shape
            feat = QgsFeature()
            feat.initAttributes(2)
            coordinates = [QgsPoint(gapXTop/2 + listPoints[0].x() + gapXTop*num, gapYTop/2 + listPoints[0].y() + gapYTop*num), QgsPoint(gapXBottom/2 + listPoints[3].x() + gapXBottom*num, gapYBottom/2 + listPoints[3].y() + gapYBottom*num)]
            feat.setAttribute(0, selectedSegmentId)
            feat.setAttribute(1, int(laneId))
            feat.setGeometry(QgsGeometry.fromPolyline(coordinates))
            laneLayer.dataProvider().addFeatures([feat])

    def delete(self, features):
        if self.active_layer_id == TYPE.MULNODE:
            self.deleteMulNode(features)
        elif self.active_layer_id == TYPE.SEGMENT:
            self.deleteSegment(features)
        else:
            self.deleteSegmentComponents(features)

    # def deleteUniNode(self, features):
    #     ids = {}
    #     # delete from shapefile
    #     for feature in features:
    #         self.active_layer.dataProvider().deleteFeatures([feature.id()])
    #         attrs = feature.attributes()
    #         ids[int(attrs[0])] = True
    #     # delete data dependency
    #     roadNetwork = self.document.find('geospatial/road_network')
    #     nodes = roadNetwork.find('Nodes')
    #     uniNodeParent = nodes.find('UniNodes')
    #     uniNodes = uniNodeParent.findall('UniNode')
    #     if uniNodes is not None:
    #         for uniNode in uniNodes:
    #             nodeId = int(uniNode.find("nodeID").text)
    #             if nodeId in ids:
    #                 uniNodeParent.remove(uniNode)

    def deleteMulNode(self, features):
        ids = {}
        # delete from shapefile
        for feature in features:
            self.active_layer.dataProvider().deleteFeatures([feature.id()])
            attrs = feature.attributes()
            ids[int(attrs[0])] = True
        roadNetwork = self.document.find('geospatial/road_network')
        nodesParent = roadNetwork.find('nodes')
        nodes = nodesParent.find('node')
        if nodes is not None:
            for node in nodes:
                nodeId = int(node.find("nodeID").text)
                if nodeId in ids:
                    nodesParent.remove(mulNode)

    def deleteSegmentComponents(self, features):                            #for busstop, crossing, laneedge
        ids = {}
        # delete from shapefile
        for feature in features:
            self.active_layer.dataProvider().deleteFeatures([feature.id()])
            attrs = feature.attributes()
            if not ids.has_key(attrs[0]):
                ids[attrs[0]] = {}
            ids[attrs[0]][attrs[1]] = True

        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        segments = linkParent.findall('link/segments/segment')
        for segment in segments:
            segmentId = int(segment.find("segmentID").text)
            if segmentId in ids:
                if self.active_layer_id == TYPE.LANE:
                    laneParent = segment.find("lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall("lane")
                        for lane in lanes:
                            laneId = int(lane.find("id").text)
                            if laneId in ids[segmentId]:
                                laneParent.remove(lane)
                elif self.active_layer_id == TYPE.LANEEDGE:
                    laneEdgeParent = segment.find("laneEdgePolylines_cached")
                    if laneEdgeParent is not None:
                        laneEdges = laneEdgeParent.findall("laneEdgePolyline_cached")
                        for laneEdge in laneEdges:
                            laneEdgeNumber = int(laneEdge.find("laneNumber").text)
                            if laneEdgeNumber in ids[segmentId]:
                                laneEdgeParent.remove(laneEdge)
                elif self.active_layer_id == TYPE.CROSSING:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None:
                        crossings = obstacles.findall("Crossing")
                        for crossing in crossings:
                            crossing_id = int(crossing.find("id").text)
                            if crossing_id in ids[segmentId]:
                                obstacles.remove(crossing)
                elif self.active_layer_id == TYPE.BUSSTOP:
                    obstacles = segment.find("Obstacles")
                    if obstacles is not None:
                        busstops = obstacles.findall("BusStop")
                        for busstop in busstops:
                            busstop_id = int(busstop.find("id").text)
                            if busstop_id in ids[segmentId]:
                                obstacles.remove(busstop)


    def deleteSegment(self, features):
        ids = {}
        # delete from shapefile
        for feature in features:
            self.active_layer.dataProvider().deleteFeatures([feature.id()])
            attrs = feature.attributes()
            ids[attrs[1]] = attrs[1]
        # delete inside components
        layers = [self.getLayer(TYPE.LANEEDGE), self.getLayer(TYPE.LANE), self.getLayer(TYPE.CROSSING), self.getLayer(TYPE.BUSSTOP)]
        for layer in layers:
            delete_feature_ids = []
            for feature in layer.getFeatures():
                attrs = feature.attributes()
                if attrs[0] in ids:
                    delete_feature_ids.append(feature.id())
            if len(delete_feature_ids) > 0:
                layer.dataProvider().deleteFeatures(delete_feature_ids)

        roadNetwork = self.document.find('geospatial/road_network')
        linkParent = roadNetwork.find('links')
        if linkParent is not None:
            links = linkParent.findall('link')
            if links is not None:
                for link in links:
                    segmentParent = link.find('segments')
                    if segmentParent is not None:
                        segments = segmentParent.findall('segment')
                        if segments is not None:
                            for segment in segments:
                                segmentId = int(segment.find("id").text)
                                if segmentId in ids:
                                    segmentParent.remove(segment)


    def save(self):
        self.document.write(self.data_path, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml")