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

    # def addUninode(self, point, nodeData):
    #     '''ADD FEATURE TO LAYER'''
    #     feat = QgsFeature()
    #     feat.initAttributes (1)
    #     feat.setAttribute(0, nodeData["id"])
    #     feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point.x(),point.y())))
    #     self.active_layer.dataProvider().addFeatures([feat])
    #
    #     '''ADD TO data.xml '''
    #     roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
    #     nodes = roadNetwork.find('Nodes')
    #     uniNodeParent = nodes.find('UniNodes')
    #     node = ElementTree.SubElement(uniNodeParent, 'UniNode')
    #     #add Id
    #     ElementTree.SubElement(node, 'nodeID').text = str(nodeData["id"])
    #     #add location
    #     location = ElementTree.SubElement(node, 'location')
    #     ElementTree.SubElement(location, 'xPos').text = "--"
    #     ElementTree.SubElement(location, 'yPos').text = "--"
    #     #add originalDB_ID
    #     ElementTree.SubElement(node, 'originalDB_ID').text = "\"aimsun-id\":\"%s\""%str(nodeData["aimsunId"])
    #     #add firstPair
    #     if nodeData["firstPair"] is not 0:
    #         firstPair = ElementTree.SubElement(node, 'firstPair')
    #         ElementTree.SubElement(firstPair, 'first').text = str(nodeData["firstPair"][0])
    #         ElementTree.SubElement(firstPair, 'second').text = str(nodeData["firstPair"][1])
    #     if nodeData["secondPair"] is not 0:
    #         secondPair = ElementTree.SubElement(node, 'secondPair')
    #         ElementTree.SubElement(secondPair, 'first').text = str(nodeData["secondPair"][0])
    #         ElementTree.SubElement(secondPair, 'second').text = str(nodeData["secondPair"][1])
    #
    #     connectorsEle = ElementTree.SubElement(node, 'Connectors')
    #     if nodeData["connectors"] :
    #         for connector in nodeData["connectors"]:
    #             connectorEle = ElementTree.SubElement(connectorsEle, 'Connector')
    #             ElementTree.SubElement(connectorEle, 'laneFrom').text = str(connector[0])
    #             ElementTree.SubElement(connectorEle, 'laneTo').text = str(connector[1])

    # def updateUninode(self, feature, nodeData):
    #     #update feature if necessary
    #     attrs = feature.attributes()
    #     id = int(attrs[0])
    #     if id != nodeData["id"]:
    #         attrs = {0 : nodeData["id"]}
    #         self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
    #     #get info
    #     roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
    #     nodes = roadNetwork.find('Nodes')
    #     uniNodeParent = nodes.find('UniNodes')
    #     uniNodes = uniNodeParent.findall('UniNode')
    #     selectedNode = None
    #     if uniNodes is not None:
    #         for uniNode in uniNodes:
    #             nodeId = int(uniNode.find("nodeID").text)
    #             if nodeId == id:
    #                 selectedNode = uniNode
    #                 break
    #     if selectedNode is None:
    #         QgsMessageLog.logMessage("updateUninode not find node id %s"%id, 'SimGDC')
    #         return
    #     #update id
    #     selectedNode.find("nodeID").text = str(nodeData["id"])
    #     #update aimsunId
    #     selectedNode.find("originalDB_ID").text = "\"aimsun-id\":\"%s\""%str(nodeData["aimsunId"])
    #     #firstPair
    #     firstPair = selectedNode.find("firstPair")
    #     if firstPair is None and nodeData["firstPair"] is not 0:
    #         newFirstPair = ElementTree.SubElement(selectedNode, 'firstPair')
    #         ElementTree.SubElement(newFirstPair, 'first').text = str(nodeData["firstPair"][0])
    #         ElementTree.SubElement(newFirstPair, 'second').text = str(nodeData["firstPair"][1])
    #     if firstPair is not None:
    #         if nodeData["firstPair"] is not 0:
    #             firstPair.find("first").text = str(nodeData["firstPair"][0])
    #             firstPair.find("second").text = str(nodeData["firstPair"][1])
    #         else:
    #             selectedNode.remove(firstPair)
    #     #secondPair
    #     secondPair = selectedNode.find("secondPair")
    #     if secondPair is None and nodeData["secondPair"] is not None:
    #         if nodeData["secondPair"] is not 0:
    #             newSecondPair = ElementTree.SubElement(selectedNode, 'secondPair')
    #             ElementTree.SubElement(newSecondPair, 'first').text = str(nodeData["secondPair"][0])
    #             ElementTree.SubElement(newSecondPair, 'second').text = str(nodeData["secondPair"][1])
    #     if secondPair is not None:
    #         if nodeData["secondPair"] is not None and nodeData["secondPair"] is not 0:
    #             secondPair.find("first").text = str(nodeData["secondPair"][0])
    #             secondPair.find("second").text = str(nodeData["secondPair"][1])
    #         else:
    #             selectedNode.remove(secondPair)
    #     #connectors
    #     connectors = selectedNode.find("Connectors")
    #     if connectors is not None:
    #         selectedNode.remove(connectors)
    #     connectorsEle = ElementTree.SubElement(selectedNode, 'Connectors')
    #     if nodeData["connectors"] :
    #         for connector in nodeData["connectors"]:
    #             connectorEle = ElementTree.SubElement(connectorsEle, 'Connector')
    #             ElementTree.SubElement(connectorEle, 'laneFrom').text = str(connector[0])
    #             ElementTree.SubElement(connectorEle, 'laneTo').text = str(connector[1])

    #
    # def getUninode(self, feature):
    #     #get id from feature
    #     attrs = feature.attributes()
    #     id = int(attrs[0])
    #     #get info
    #     roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
    #     nodes = roadNetwork.find('Nodes')
    #     uniNodeParent = nodes.find('UniNodes')
    #     uniNodes = uniNodeParent.findall('UniNode')
    #     selectedNode = None
    #     if uniNodes is not None:
    #         for uniNode in uniNodes:
    #             nodeId = int(uniNode.find("nodeID").text)
    #             if nodeId == id:
    #                 selectedNode = uniNode
    #                 break
    #     if selectedNode is not None:            # Modifying existing node
    #         info = {}
    #         info["id"] = selectedNode.find("nodeID").text
    #         aimsunIdStr = selectedNode.find("originalDB_ID").text
    #         aimsunIds = re.findall(r'[0-9]+', aimsunIdStr)
    #         info["aimsunId"] = aimsunIds[0]
    #         info["firstPair"] = None
    #         firstPair = selectedNode.find("firstPair")
    #         if firstPair is not None and firstPair is not 0:
    #             info["firstPair"] = [int(firstPair.find("first").text), int(firstPair.find("second").text)]
    #         info["secondPair"] = None
    #         secondPair = selectedNode.find("secondPair")
    #         if secondPair is not None:
    #             info["secondPair"] = [int(secondPair.find("first").text), int(secondPair.find("second").text)]
    #         info["connectors"] = None
    #         connectors = selectedNode.find("Connectors")
    #         if connectors is not None:
    #             info["connectors"] = []
    #             for connector in connectors.findall('Connector'):
    #                 info["connectors"].append([int(connector.find("laneFrom").text), int(connector.find("laneTo").text)])
    #         return info
    #     return None


    def addMultiNode(self, point, nodeData):
        '''ADD FEATURE TO LAYER'''
        feat = QgsFeature()
        feat.initAttributes (1)
        feat.setAttribute(0, nodeData["id"])
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point.x(),point.y())))
        self.active_layer.dataProvider().addFeatures([feat])
        '''ADD TO data.xml '''
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        nodes = roadNetwork.find('Nodes')
        intersectionsParent = nodes.find('Intersections')
        multiNode = ElementTree.SubElement(intersectionsParent, 'Intersection')
        #add Id
        ElementTree.SubElement(multiNode, 'nodeID').text = str(nodeData["id"])
        #addType
        ElementTree.SubElement(multiNode, 'nodeType').text = str(nodeData["nodeType"])
        #addTrafficLightID
        ElementTree.SubElement(multiNode, 'trafficLightID').text = str(nodeData["trafficLightID"])

        #addTurningGroup
        turningGroupParent = ElementTree.SubElement(multiNode, 'TurningGroups')

        #if nodeData["turningGroup"]:
        for tG in nodeData["turningGroup"]:
            turningGroup = ElementTree.SubElement(turningGroupParent, 'TurningGroup')
            ElementTree.SubElement(turningGroup, 'ID').text = str(tG[0])
            ElementTree.SubElement(turningGroup, 'fromLink').text = str(tG[1])
            ElementTree.SubElement(turningGroup, 'toLink').text = str(tG[2])
            ElementTree.SubElement(turningGroup, 'Phases').text = str(tG[3])
            ElementTree.SubElement(turningGroup, 'Rules').text = str(tG[4])
            if nodeData["turningPath"]:
                turningPathParent = ElementTree.SubElement(turningGroup, 'TurningPaths')
                for tP in nodeData["turningPath"]:
                    if tP[0] == tG[0]:
                        turningPath = ElementTree.SubElement(turningPathParent, 'TurningPath')
                        ElementTree.SubElement(turningPath, 'groupID').text = str(tP[0])
                        ElementTree.SubElement(turningPath, 'ID').text = str(tP[1])
                        ElementTree.SubElement(turningPath, 'fromLane').text = str(tP[2])
                        ElementTree.SubElement(turningPath, 'toLane').text = str(tP[3])



        #add location
        location = ElementTree.SubElement(multiNode, 'location')
        ElementTree.SubElement(location, 'xPos').text = str(feat.geometry().asPoint().x())
        ElementTree.SubElement(location, 'yPos').text = str(feat.geometry().asPoint().y())

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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        nodes = roadNetwork.find('Nodes')
        intersectionsParent = nodes.find('Intersections')
        multiNodes = intersectionsParent.findall('Intersection')
        selectedNode = None
        if multiNodes is not None:
            for multiNode in multiNodes:
                nodeId = int(multiNode.find("nodeID").text)
                if nodeId == id:
                    selectedNode = multiNode
                    break
        if selectedNode is None:
            QgsMessageLog.logMessage("updateMultiNode not find node id %s"%id, 'SimGDC')
            return
        #update id
        selectedNode.find("nodeID").text = str(nodeData["id"])
        #update type
        selectedNode.find("nodeType").text = str(nodeData["nodeType"])

        #addTrafficLightID
        selectedNode.find("trafficLightID").text = str(nodeData["trafficLightID"])

        #addTurningGroup
        turningGroupParent = selectedNode.find("TurningGroups")

        for tG in turningGroupParent.findall('TurningGroup'):
            turningGroupParent.remove(tG)
        for tG in selectedNode.findall('TurningGroup'):
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

        # #update roadSegmentsAt
        # roadSegmentsAt = selectedNode.find("roadSegmentsAt")
        # if roadSegmentsAt is not None:
        #     selectedNode.remove(roadSegmentsAt)
        # roadSegmentsAt = ElementTree.SubElement(selectedNode, 'roadSegmentsAt')
        # for roadSegment in nodeData["roadSegments"]:
        #     ElementTree.SubElement(roadSegmentsAt, 'segmentID').text = str(roadSegment)
        #update connectors
        # connectorsEle = selectedNode.find("Connectors")
        # if connectorsEle is not None:
        #     selectedNode.remove(connectorsEle)
        # connectorsEle = ElementTree.SubElement(selectedNode, 'Connectors')
        # for multiConnector in nodeData["multiConnectors"]:
        #     multiConnectorEle = ElementTree.SubElement(connectorsEle, 'MultiConnectors')
        #     ElementTree.SubElement(multiConnectorEle, 'RoadSegment').text = str(multiConnector[0])
        #     connectors = ElementTree.SubElement(multiConnectorEle, 'Connectors')
        #     for innerConnector in multiConnector[1]:
        #         connector = ElementTree.SubElement(connectors, 'Connector')
        #         ElementTree.SubElement(connector, 'laneFrom').text = str(innerConnector[0])
        #         ElementTree.SubElement(connector, 'laneTo').text = str(innerConnector[1])


    def getMultiNode(self, feature):
        #get id from feature
        attrs = feature.attributes()
        id = int(attrs[0])   
        #get info
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        nodes = roadNetwork.find('Nodes')
        multiNodeParent = nodes.find('Intersections')
        multiNodes = multiNodeParent.findall('Intersection')
        selectedNode = None
        if multiNodes is not None:
            for multiNode in multiNodes:
                nodeId = int(multiNode.find("nodeID").text)
                if nodeId == id:
                    selectedNode = multiNode
                    break
        if selectedNode is not None:
            info = {}
            info["id"] = selectedNode.find("nodeID").text
            # aimsunIdStr = selectedNode.find("originalDB_ID").text
            # aimsunIds = re.findall(r'[0-9]+', aimsunIdStr)
            # info["aimsunId"] = aimsunIds[0]
            info["nodeType"] = selectedNode.find("nodeType").text
            info["trafficLightID"] = selectedNode.find("trafficLightID").text


        turningGroups = selectedNode.find("TurningGroups")

        turningGroup = turningGroups.findall("TurningGroup")

        info["turningGroup"] = []
        info["turningPath"] = []

        if turningGroup:
        #     msgBox = QtGui.QMessageBox()
        #     msgBox.setText(turningGroup[0].find("ID").text)
        #     msgBox.exec_()
        #     return
            for tG in turningGroup:
                info["turningGroup"].append([tG.find("ID").text,tG.find("fromLink").text,tG.find("toLink").text,tG.find("Phases").text,tG.find("Rules").text])
                # turningPaths = turningGroups.findall("TurningPath")
                # if turningPaths:
                for tP in selectedNode.iter('TurningPath'):
                    if tP.find("groupID").text == tG.find("ID").text:
                        # info["turningPath"].append(tP)
                        info["turningPath"].append([tP.find("groupID").text,tP.find("ID").text,tP.find("fromLane").text,tP.find("toLane").text])



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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                linkName = link.find("roadName").text
                listLinks[linkId] = linkName
        return listLinks

    def getLinkListDetail(self):
        listLinks = {}
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                linkName = link.find("roadName").text
                startNode = int(link.find("StartingNode").text)
                endNode = int(link.find("EndingNode").text)
                listLinks[linkId] = [linkId, linkName, startNode, endNode]
        return listLinks

    def manageLink(self, data):
        if data["oldId"] < 1:
            #add new
            roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
            linkParent = roadNetwork.find('Links')
            if linkParent is None:
                linkParent = ElementTree.SubElement(roadNetwork, 'Links')
            link = ElementTree.SubElement(linkParent, 'Link')
            ElementTree.SubElement(link, 'linkID').text = str(data["id"])
            ElementTree.SubElement(link, 'roadName').text = str(data["roadName"])
            ElementTree.SubElement(link, 'StartingNode').text = str(data["startingNode"])
            ElementTree.SubElement(link, 'EndingNode').text = str(data["endingNode"])
            ElementTree.SubElement(link, 'Segments')
        else:
            roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
            linkParent = roadNetwork.find('Links')
            links = linkParent.findall('Link')
            selectedLink = None
            if links is not None:
                for link in links:
                    linkId = int(link.find("linkID").text)
                    if linkId == data["oldId"]:
                        selectedLink = link
                        break
            #update info
            selectedLink.find("linkID").text = str(data["id"])
            selectedLink.find("roadName").text = str(data["roadName"])
            selectedLink.find("StartingNode").text = str(data["startingNode"])
            selectedLink.find("EndingNode").text = str(data["endingNode"])
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedLink = None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                if linkId == data["linkId"]:
                    selectedLink = link
                    break
        if selectedLink is not None:
            segments = selectedLink.find("Segments")
            if segments is None:
                segments = ElementTree.SubElement(selectedLink, 'Segments')
            segment = ElementTree.SubElement(segments, 'Segment')
            #add Info
            ElementTree.SubElement(segment, 'segmentID').text = str(data["id"])
            ElementTree.SubElement(segment, 'sequenceno').text = str(data["sequenceno"])
            ElementTree.SubElement(segment, 'capacity').text = str(data["capacity"])
            ElementTree.SubElement(segment, 'maxSpeed').text = str(data["maxSpeed"])
            ElementTree.SubElement(segment, 'Tags').text = str(data["tags"])
            connectors = ElementTree.SubElement(segment, 'Connectors')
            connector = ElementTree.SubElement(connectors, 'Connector')
            for conn in data["connectors"]:
                ElementTree.SubElement(connector, 'laneconnectorID').text = str(conn[0])
                ElementTree.SubElement(connector, 'fromSection').text = str(conn[1])
                ElementTree.SubElement(connector, 'toSection').text = str(conn[2])
                ElementTree.SubElement(connector, 'fromLane').text = str(conn[3])
                ElementTree.SubElement(connector, 'toLane').text = str(conn[4])

        ElementTree.SubElement(segment, 'x').text = str(feat.geometry().asPolyline().point.x())
        ElementTree.SubElement(segment, 'y').text = str(feat.geometry().asPolyline().point.y())
        ElementTree.SubElement(segment, 'z').text = str(feat.geometry().asPolyline().point.z())

    def updateSegment(self, feature, data):
        #update feature if necessary
        attrs = feature.attributes()
        oldLinkId = int(attrs[0])
        oldSegmentId = int(attrs[1])
        if oldLinkId != data["linkId"] or oldSegmentId != data["id"]:
            attrs = {0 : data["linkId"], 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedSegment= None
        oldLinkSegments = None
        newLinkSegments = None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                if linkId == data["linkId"]:
                    newLinkSegments = link.find("Segments")
                if linkId == oldLinkId:
                    oldLinkSegments = link.find("Segments")
                    segments = oldLinkSegments.findall("Segment")
                    for segment in segments:
                        segmentId = int(segment.find("segmentID").text)
                        if segmentId == oldSegmentId:
                            selectedSegment = segment
        if selectedSegment is None:
            QgsMessageLog.logMessage("updateSegment can not find segment id %s"%str(oldSegmentId), 'SimGDC')
            return
        #update info
        selectedSegment.find("segmentID").text = str(data["id"])
        selectedSegment.find("sequenceno").text = str(data["sequenceno"])
        selectedSegment.find("capacity").text = str(data["capacity"])
        selectedSegment.find("maxSpeed").text = str(data["maxSpeed"])
        selectedSegment.find("Tags").text = str(data["tags"])

        connectorsroot = selectedSegment.find("Connectors").text
        connectors = connectorsroot.findall("Connector")
        for conn in connectors:
            conn.find("laneconnectorID").text = str(conn[0])
            conn.find("fromSection").text = str(conn[1])
            conn.find("toSection").text = str(conn[2])
            conn.find("fromLane").text = str(conn[3])
            conn.find("toLane").text = str(conn[4])

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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                linkName = link.find("roadName").text
                listLinks[linkId] = linkName
                if linkId == selectedLinkId:
                    segments = link.find("Segments").findall("Segment")
                    for segment in segments:
                        segmentId = int(segment.find("segmentID").text)
                        if segmentId == selectedSegmentId:
                            selectedSegment = segment
        if selectedSegment is not None:
            info = {}
            info["linkId"] = selectedLinkId
            info["id"] = selectedSegment.find("segmentID").text
            # aimsunIdStr = selectedSegment.find("originalDB_ID").text
            # aimsunIds = re.findall(r'[0-9]+', aimsunIdStr)
            # info["aimsunId"] = aimsunIds[0]
            info["sequenceno"] = selectedSegment.find("sequenceno").text
            info["capacity"] = selectedSegment.find("capacity").text
            info["maxSpeed"] = selectedSegment.find("maxSpeed").text
            info["tags"] = selectedSegment.find("Tags").text
            # info["roadType"] = selectedSegment.find("roadType").text
            # info["category"] = selectedSegment.find("category").text
            info["connectors"] = selectedSegment.find("connectors").text
            connectorsroot = selectedSegment.find("Connectors").text
            connectors = connectorsroot.findall("Connector")
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedCrossing = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedCrossing = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedBusstop = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedBusstop = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
                if segmentId == selectedSegmentId:
                    selectedSegment = segment
                    break
        if selectedSegment is not None:
            laneParent = selectedSegment.find("Lanes")
            if laneParent is None:
                laneParent = ElementTree.SubElement(selectedSegment, 'Lanes')
            lane = ElementTree.SubElement(laneParent, 'Lane')
            ElementTree.SubElement(lane, 'laneID').text = str(data["id"])
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

    def updateLane(self, feature, data):
         #update feature if necessary
        attrs = feature.attributes()
        selectedsegmentId = int(attrs[0])
        oldLaneId = int(attrs[1])
        if oldLaneId != data["id"]:
            attrs = {0 : selectedsegmentId, 1: data["id"]}
            self.active_layer.dataProvider().changeAttributeValues({int(feature.id()) : attrs })
        #get info
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedLane = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
                if segmentId == selectedsegmentId:
                    laneParent = segment.find("Lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall('Lane')
                        for lane in lanes:
                            laneId = int(lane.find("laneID").text)
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

    def getLane(self, feature):
         #get id from feature
        attrs = feature.attributes()
        selectedSegmentId = int(attrs[0])
        selectedLaneId = int(attrs[1]) 
        #get info
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedLane = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
                if segmentId == selectedSegmentId:
                    laneParent = segment.find("Lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall('Lane')
                        for lane in lanes:
                            laneId = int(lane.find("laneID").text)
                            if laneId == selectedLaneId:
                                selectedLane = lane
                    break
        if selectedLane is not None:
            info = {}
            info["segmentId"] = selectedSegmentId
            info["id"] = selectedLane.find("laneID").text
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedSegmentId = int(data["segmentId"])
        selectedSegment = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedLaneEdge = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        selectedLaneEdge = None
        if segments is not None:
            for segment in segments:
                segmentId = int(segment.find("segmentID").text)
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
        selectedPolygon = feature.geometry().asPolygon()
        listPoints = selectedPolygon[0]
        gapXTop = (listPoints[1].x() - listPoints[0].x())/nLane
        gapYTop = (listPoints[1].y() - listPoints[0].y())/nLane
        gapXBottom = (listPoints[2].x() - listPoints[3].x())/nLane
        gapYBottom = (listPoints[2].y() - listPoints[3].y())/nLane
        QgsMessageLog.logMessage("test (%s, %s)"%(str(listPoints[0].x()), str(listPoints[0].y())), 'SimGDC')
        #get info
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        links = linkParent.findall('Link')
        selectedSegment= None
        if links is not None:
            for link in links:
                linkId = int(link.find("linkID").text)
                if linkId == selectedLinkId:
                    segments = link.find("Segments").findall("Segment")
                    for segment in segments:
                        segmentId = int(segment.find("segmentID").text)
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
        lanes = ElementTree.SubElement(selectedSegment, 'Lanes')
        for num in range(0, nLane):
            lane = ElementTree.SubElement(lanes, 'Lane')
            laneId = "%s%s"%(str(selectedSegmentId), str(num))
            ElementTree.SubElement(lane, 'laneID').text = laneId
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
        if self.active_layer_id == TYPE.UNINODE:
            self.deleteUniNode(features)
        elif self.active_layer_id == TYPE.MULNODE:
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
    #     roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
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
        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        nodes = roadNetwork.find('Nodes')
        mulNodeParent = nodes.find('Intersections')
        mulNodes = mulNodeParent.findall('Intersection')
        if mulNodes is not None:
            for mulNode in mulNodes:
                nodeId = int(mulNode.find("nodeID").text)
                if nodeId in ids:
                    mulNodeParent.remove(mulNode)

    def deleteSegmentComponents(self, features):                            #for busstop, crossing, laneedge
        ids = {}
        # delete from shapefile
        for feature in features:
            self.active_layer.dataProvider().deleteFeatures([feature.id()])
            attrs = feature.attributes()
            if not ids.has_key(attrs[0]):
                ids[attrs[0]] = {}
            ids[attrs[0]][attrs[1]] = True

        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        segments = linkParent.findall('Link/Segments/Segment')
        for segment in segments:
            segmentId = int(segment.find("segmentID").text)
            if segmentId in ids:
                if self.active_layer_id == TYPE.LANE:
                    laneParent = segment.find("Lanes")
                    if laneParent is not None:
                        lanes = laneParent.findall("Lane")
                        for lane in lanes:
                            laneId = int(lane.find("laneID").text)
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

        roadNetwork = self.document.find('GeoSpatial/RoadNetwork')
        linkParent = roadNetwork.find('Links')
        if linkParent is not None:
            links = linkParent.findall('Link')
            if links is not None:
                for link in links:
                    segmentParent = link.find('Segments')
                    if segmentParent is not None:
                        segments = segmentParent.findall('Segment')
                        if segments is not None:
                            for segment in segments:
                                segmentId = int(segment.find("segmentID").text)
                                if segmentId in ids:
                                    segmentParent.remove(segment)


    def save(self):
        self.document.write(self.data_path, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml")