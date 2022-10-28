from operator import truediv
from common_lib.const import constants


class GetFirstFleet:
    goalBuilding = constants.SHIPYARD
    goalBuildingLevel = 2
    goalResearch = constants.COMBUSTION_DRIVE
    goalResearchLevel = 2

    def isRelevantProgressionObject(requestData):
        if(requestData['facilityLevels'][constants.ATTR_NAME_OF_SHIPYARD] < 2):
            return True
        return False

    def getNextItemsParallel(self, requestData):
        if(requestData['facilityLevels'][constants.ATTR_NAME_OF_SHIPYARD] == 1):
            return self.createResponseJson(constants.SHIPYARD, 2)

        respBuilding = self.getClosestResearchedPrerequisites(self.goalBuilding, requestData)
        respResearch = self.getClosestResearchedPrerequisites(self.goalResearch, requestData)


        return {'constructable' : [{'buildingID': 'buildingID', 'buildingLevel': 'buildingLevel'},{'buildingID': 'buildingID', 'buildingLevel': 'buildingLevel', 'severity': 'severity'}],
                'researchable' : 'IDK TODO'
        }
    
    def createResponseJson(self, buildingID, buildingLevel, researchID, researchLevel):
        return {'constructable' : {'buildingID': buildingID, 'buildingLevel': buildingLevel},
                'researchable' : {'researchID' : researchID, 'researchLevel' : researchLevel}
        }

    # def getAvailablePrerequisitesOf(self, ogameID, requestData):
    #     self.getClosestResearchedPrerequisites(ogameID, requestData)
    #     return constants.prerequisitesDict[ogameID]

    def getClosestResearchedPrerequisites(self, ogameID, requestData):
        directPrerequisite = constants.prerequisitesDict[ogameID]

        requiredBuildingID = directPrerequisite['constructable']['buildingID']
        requiredBuildingLevel = directPrerequisite['constructable']['buildingLevel']  
        
        requiredResearchID = directPrerequisite['researchable']['researchID']
        requiredResearchLevel = directPrerequisite['researchable']['researchLevel']   

        missingPrerequisites = {
            'constructable' : [],
            'researchable' : []
        }
        
        if(requiredBuildingID != -1):
            currentBuildingLevel = requestData['facilityLevels'][constants.convertOgameIDToAttrName(requiredBuildingID)]
        if(requiredResearchID != -1):
            currentResearchLevel  = requestData['researchLevels'][constants.convertOgameIDToAttrName(requiredResearchID)]

        if(requiredBuildingID != -1 and currentBuildingLevel < requiredBuildingLevel):
            if(self.isPrerequisiteMet(requiredBuildingID, requestData)):
                missingPrerequisites['constructable'].append({'buildingID': requiredBuildingID, 'buildingLevel': currentBuildingLevel + 1}) 
            else:
                innerPrereq = self.getClosestResearchedPrerequisites(requiredBuildingID, requestData)
                self.fillPrereqDataWithNonNull(missingPrerequisites, innerPrereq)

        if(requiredResearchID != -1 and currentResearchLevel < requiredResearchLevel):
            if(self.isPrerequisiteMet(requiredResearchID, requestData)):
                missingPrerequisites['researchable'].append({'researchID': requiredResearchID, 'researchLevel': currentResearchLevel + 1})
            else:
                innerPrereq = self.getClosestResearchedPrerequisites(requiredResearchID, requestData)
                self.fillPrereqDataWithNonNull(missingPrerequisites, innerPrereq)

        return missingPrerequisites

    def fillPrereqDataWithNonNull(self, missingPrerequisites, innerPrereq):
        for constructable in innerPrereq['constructable']:
            if(constructable['buildingID'] != -1):
                 missingPrerequisites['constructable'].append({'buildingID': constructable['buildingID'], 'buildingLevel': constructable['buildingLevel']})

        for researchable in innerPrereq['researchable']:
            if(researchable['researchID'] != -1):
                missingPrerequisites['researchable'].append({'researchID': researchable['researchID'], 'researchLevel': researchable['researchLevel']})

    def isPrerequisiteMet(self, ogameID, requestData):
        directPrerequisite = constants.prerequisitesDict[ogameID]

        requiredBuildingID = directPrerequisite['constructable']['buildingID']
        requiredBuildingLevel = directPrerequisite['constructable']['buildingLevel']

        requiredResearchID = directPrerequisite['researchable']['researchID']
        requiredResearchLevel = directPrerequisite['researchable']['researchLevel']   
        
        if(requiredBuildingID != -1):
            currentBuildingLevel = requestData['facilityLevels'][constants.convertOgameIDToAttrName(requiredBuildingID)]
        if(requiredResearchID != -1):
            currentResearchLevel  = requestData['researchLevels'][constants.convertOgameIDToAttrName(requiredResearchID)]

        if(requiredBuildingID != -1 and currentBuildingLevel < requiredBuildingLevel):
            return False 
        if(requiredResearchID != -1 and currentResearchLevel < requiredResearchLevel):
            return False
        return True

