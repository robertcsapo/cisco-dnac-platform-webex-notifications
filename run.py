import json
import os
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI

if not "WEBEX_TEAMS_ACCESS_TOKEN" in os.environ:
    webexAPI = WebexTeamsAPI(access_token='CHANGEME')
else:
    webexAPI = WebexTeamsAPI()

if not "WEBEX_TEAMS_ROOM_ID" in os.environ:
    os.environ["WEBEX_TEAMS_ROOM_ID"] = "CHANGEME"
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]
else:
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def mainPage():
    print(os.environ)
    return("cisco-dnac-platform-webex-notifications -> by Robert Csapo (robert@nigma.org)")

@app.route('/sample', methods=['GET'])
def sample():
    jsonFile = "outputdata.json"
    with open(jsonFile) as f:
        data = json.load(f)
    issueTitle = data["title"]
    issuePriority = data["priority"]
    for item in data["enrichmentInfo"]["issueDetails"]["issue"]:
        issueDescription = item["issueDescription"]
        issueSeverity = item["issueSeverity"]
        issueSummary = item["issueSummary"]
    data = "Warning %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)
    webex(str(data))
    return("Sample data from -> %s" % jsonFile)

@app.route('/postsample', methods=['POST'])
def postSample():
    data = request.json
    issueTitle = data["title"]
    for item in data["enrichmentInfo"]["issueDetails"]["issue"]:
        issueDescription = item["issueDescription"]
        issueSeverity = item["issueSeverity"]
        issueSummary = item["issueSummary"]
    data = "Warning %s! %s - %s" % (issueSeverity, issueTitle, issueSummary)
    webex(str(data))
    return("Sample JSON Payload received")

@app.route('/webex', methods=['GET'])
def webex(*data):
    if not len(data) == 0:
        data = data[0]
        webexAPI.messages.create(webexRoomId, text=data)
    else:
        webexAPI.messages.create(webexRoomId, text="Sample connection!")
    return("webex")

@app.route('/dnac', methods=['POST'])
def dnacPayload():
    data = request.json
    if not len(data) == 0:
        issueTitle = data["title"]
        issuePriority = data["priority"]
        for item in data["enrichmentInfo"]["issueDetails"]["issue"]:
            issueDescription = item["issueDescription"]
            issueSeverity = item["issueSeverity"]
            issueSummary = item["issueSummary"]
        data = "Warning %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)
        webex(str(data))
        return("DNA-C JSON Payload received")
    else:
        return("Connection Alive")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,threaded=True,debug=False)
