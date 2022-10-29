from copyreg import constructor
from glob import glob
import json
import math
import ast
import numpy as np
from flask import Flask,request
from common_lib.const import constants

from progressionObjects.prgGetFirstFleet import GetFirstFleet


#TODO Consider ongoing construction and research 
class progressionManager():
    def __init__(self):
        self.request_data = ''

    def processRequest(self):
        self.activeProgressionObject = self.getCurrentProgressionObject()
        return self.getProgressionItemsToBuild()
    
    def getProgressionItemsToBuild(self): 
        itemsParallel = self.activeProgressionObject.getNextItemsParallel(self.request_data)
        prefferedConstructable = self.getPrefferedConstructable(itemsParallel['constructable'])
        prefferedResearchable = self.getPrefferedResearchable(itemsParallel['researchable'])
        
        return  GetFirstFleet.createResponseJson(prefferedConstructable[0], prefferedConstructable[1], prefferedResearchable[0], prefferedResearchable[1])

    def getPrefferedConstructable(self, constuctables):
        prefferedConstructableId = -1
        prefferedConstructableLevel = -1
        for constAble in constuctables:
            if(constAble['buildingID'] == constants.RESEARCH_LAB and self.isConstructableAffordable(constAble['buildingID'])):
                prefferedConstructableId = constAble['buildingID']
                prefferedConstructableLevel = constAble['buildingLevel']
            elif(constAble['buildingID'] == constants.ROBOT_FACTORY and prefferedConstructableId != constants.RESEARCH_LAB and self.isConstructableAffordable(constAble['buildingID'])):
                prefferedConstructableId = constAble['buildingID']
                prefferedConstructableLevel = constAble['buildingLevel']
            elif(prefferedConstructableId == -1 and self.isConstructableAffordable(constAble['buildingID'])):
                prefferedConstructableId = constAble['buildingID']
                prefferedConstructableLevel = constAble['buildingLevel']

        return (prefferedConstructableId, prefferedConstructableLevel)

    def getPrefferedResearchable(self, researchables):
        prefferedResearchableId = -1
        prefferedResearchableLevel = -1
        for researchAble in researchables:
            if(researchAble['researchID'] == constants.RESEARCH_LAB and self.isConstructableAffordable(researchAble['researchID'])):
                prefferedResearchableId = researchAble['researchID']
                prefferedResearchableLevel = researchAble['researchLevel']
            elif(researchAble['researchID'] == constants.ROBOT_FACTORY and prefferedResearchableId != constants.RESEARCH_LAB and self.isConstructableAffordable(researchAble['buildingID'])):
                prefferedResearchableId = researchAble['researchID']
                prefferedResearchableLevel = researchAble['researchLevel']
            elif(prefferedResearchableId == -1 and self.isConstructableAffordable(researchAble['researchID'])):
                prefferedResearchableId = researchAble['researchID']
                prefferedResearchableLevel = researchAble['researchLevel']

        return (prefferedResearchableId, prefferedResearchableLevel)

    def isConstructableAffordable(self, ogameID):
        facPrices = self.request_data['facilityPrices']
        buildingPrices = self.request_data['buildingPrices']

        attrName = constants.convertOgameIDToAttrName(ogameID)
        if any(x == attrName for x in facPrices):
            return self.isPriceAffordable(facPrices[attrName])
        if any(x == attrName for x in buildingPrices):
            return self.isPriceAffordable(buildingPrices[attrName])
        return False

    def isResearchableAffordable(self, ogameID, constructableCost):
        researchPrices = self.request_data['researchPrices']
        attrName = constants.convertOgameIDToAttrName(ogameID)

        researchPrices['Metal'][attrName] = researchPrices['Metal'][attrName] + constructableCost['Metal']
        researchPrices['Crystal'][attrName] = researchPrices['Crystal'][attrName] + constructableCost['Crystal']
        researchPrices['Deuterium'][attrName] = researchPrices['Deuterium'][attrName] + constructableCost['Deuterium']

        if any(x == attrName for x in researchPrices):
            return self.isPriceAffordable(researchPrices[attrName])
        return False

    def isPriceAffordable(self, priceDict):
        if(self.request_data['actualResources']['Metal'] < priceDict['Metal']):
            return False
        if(self.request_data['actualResources']['Crystal'] < priceDict['Crystal']):
            return False
        if(self.request_data['actualResources']['Deuterium'] < priceDict['Deuterium']):
            return False
        return True

    def getCurrentProgressionObject(self):
        if(GetFirstFleet.isRelevantProgressionObject(self.request_data)):
            return GetFirstFleet()
        return None

progManager = progressionManager()

port = 5002
app = Flask(__name__)

@app.route('/get_progression_suggestion', methods=['GET'])
def getProgressionSuggestionEndpoint():
    progManager.request_data = ast.literal_eval((request.get_json()))
    print(progManager.request_data)
    return progManager.processRequest()

@app.route('/ready', methods=['GET'])
def getReadiness():
    return "{Status: OK}"

app.run(host='0.0.0.0', port=port)