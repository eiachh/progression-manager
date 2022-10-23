from common_lib.const import constants


class GetFirstFleet:
    goalBuilding = constants.attrnameofship

    def isRelevantProgressionObject(requestData):
        
        return False

    def getNextItemsParallel(requestData):
        return {'constructable' : [{'buildingID': 'buildingID', 'buildingLevel': 'buildingLevel', 'severity': 'severity'},{'buildingID': 'buildingID', 'buildingLevel': 'buildingLevel', 'severity': 'severity'}],
                'researchable' : 'IDK TODO'
        }
