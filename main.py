from glob import glob
import json
import math
import ast
from flask import Flask,request

from progressionObjects.prgGetFirstFleet import GetFirstFleet

#{'buildingID': buildingID, 'buildingLevel': buildingLevel, 'severity': severity}
#Linear progression
#Robot factory x2 -> shipyard 2x                     -----|->
# |-> Research C -> energy tech -> combustion drive 2x----|->
class progressionManager():
    def __init__(self):
        self.request_data = ''

    def processRequest(self):
        self.activeProgressionObject = self.getCurrentProgressionObject()
        progItemToB = self.getNextProgressionItemToBuild()



        if(self.isProgressionItemWorthIt(progItemToB)):
            return progItemToB
        return {'Result': 'None'}
    
    def getNextProgressionItemToBuild(self): 
        itemsParallel = self.activeProgressionObject.getNextItemsParallel(self.request_data)
        affordableItemsParallel = self.getFilteredListByAffordance(itemsParallel)
        return 'Not implemented (getNextProgressionItemToBuild)'

    def getFilteredListByAffordance(self, items):
        return {}

    def getCurrentProgressionObject(self):
        if(GetFirstFleet.isRelevantProgressionObject(self.request_data)):
            return GetFirstFleet()
        return None

    def isProgressionItemWorthIt(self, progItem):
        
        return False

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