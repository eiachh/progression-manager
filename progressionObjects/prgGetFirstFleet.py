from operator import truediv
from common_lib.const import constants
from common_lib.utilities import utilities


class GetFirstFleet:
    goalEntity = constants.SMALL_CARGO
    
    def __init__(self, prgManager):
        self.prgManager = prgManager

    def isRelevantProgressionObject(requestData):
        if(requestData['facilityLevels'][constants.ATTR_NAME_OF_SHIPYARD] < 2):
            return True
        return False

    def getNextItemsParallel(self, requestData):
        if(requestData['facilityLevels'][constants.ATTR_NAME_OF_SHIPYARD] == 1):
            return self.prgManager.createResponseJson(constants.SHIPYARD, 2)

        respBuilding = self.getAllDoablePrerequisites(self.goalEntity, requestData)

        

        respBuilding['constructable'] = [i for n, i in enumerate(respBuilding['constructable']) if i not in respBuilding['constructable'][n + 1:]]
        respBuilding['researchable'] = [i for n, i in enumerate(respBuilding['researchable']) if i not in respBuilding['researchable'][n + 1:]]

        return respBuilding

    def getAllDoablePrerequisites(self, ogameID, requestData):
        directPrerequisite = constants.prerequisitesDict[ogameID]
        missingPrerequisites = {
            'constructable' : [],
            'researchable' : []
        }

        for constructablePrereq in  directPrerequisite['constructable']:
            self.fillMissingPrereq(requestData, missingPrerequisites, constructablePrereq, False)

        for researchablePrereq in  directPrerequisite['researchable']:
            self.fillMissingPrereq(requestData, missingPrerequisites, researchablePrereq, True)

        return missingPrerequisites

    def fillMissingPrereq(self, requestData, missingPrerequisites, constructablePrereq, isResearchable):
        idAttrStr = 'buildingID'
        levelAttrStr = 'buildingLevel'
        requestDataLevelAttrStr = 'facilityLevels'
        typeAttrStr = 'constructable'

        if(isResearchable):
            idAttrStr = 'researchID'
            levelAttrStr = 'researchLevel'
            requestDataLevelAttrStr = 'researchLevels'
            typeAttrStr = 'researchable'
        
        requiredBuildingID = constructablePrereq[idAttrStr]
        requiredBuildingLevel = constructablePrereq[levelAttrStr]  

        if(requiredBuildingID != -1):
            currentBuildingLevel = requestData[requestDataLevelAttrStr][constants.convertOgameIDToAttrName(requiredBuildingID)]

        if(requiredBuildingID != -1 and currentBuildingLevel < requiredBuildingLevel):
            if(utilities.isPrerequisiteMet(requiredBuildingID, requestData)):
                missingPrerequisites[typeAttrStr].append({idAttrStr: requiredBuildingID, levelAttrStr: currentBuildingLevel + 1}) 
            else:
                innerPrereq = self.getAllDoablePrerequisites(requiredBuildingID, requestData)
                self.fillPrereqDataWithNonNull(missingPrerequisites, innerPrereq)

    def fillPrereqDataWithNonNull(self, missingPrerequisites, innerPrereq):
        for constructable in innerPrereq['constructable']:
            if(constructable['buildingID'] != -1):
                 missingPrerequisites['constructable'].append({'buildingID': constructable['buildingID'], 'buildingLevel': constructable['buildingLevel']})

        for researchable in innerPrereq['researchable']:
            if(researchable['researchID'] != -1):
                missingPrerequisites['researchable'].append({'researchID': researchable['researchID'], 'researchLevel': researchable['researchLevel']})