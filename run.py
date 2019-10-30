import json
import os
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
import argparse

version = "1.3.1"

if "WEBEX_TEAMS_ACCESS_TOKEN" not in os.environ:
    webexAPI = WebexTeamsAPI(access_token='CHANGEME')
else:
    webexAPI = WebexTeamsAPI()

if "WEBEX_TEAMS_ROOM_ID" not in os.environ:
    os.environ["WEBEX_TEAMS_ROOM_ID"] = "CHANGEME"
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]
else:
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'GET':
        return("cisco-dnac-platform-webex-notifications version %s -> by Robert Csapo (robert@nigma.org)" % version)
    elif request.method == 'POST':
        return("cisco-dnac-platform-webex-notifications healthcheck")


@app.route('/sample', methods=['GET'])
def sample():
    jsonFile = "outputdata.json"
    with open(jsonFile) as f:
        data = json.load(f)

    issueTitle = (data["details"]["Type"] + " " + data["details"]["Device"])
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]

    data = "Warning Severity %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)
    webex(str(data))
    return("Sample data from -> %s" % jsonFile)


@app.route('/postsample', methods=['POST'])
def postSample():
    data = request.json

    issueTitle = (data["details"]["Type"] + " " + data["details"]["Device"])
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]

    data = "Warning Severity %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)

    webex(str(data))
    return("Sample JSON Payload received")


@app.route('/webex', methods=['GET'])
def webex(*data):
    if not len(data) == 0:
        data = data[0]
        webexAPI.messages.create(webexRoomId, text=data)
    else:
        webexAPI.messages.create(webexRoomId, text="Sample connection!")
    return("Sample Cisco Webex Teams Message")


@app.route('/dnac', methods=['POST'])
def dnacPayload():
    data = request.json
    if not len(data) == 0:

        issueTitle = (data["details"]["Type"] + " " + data["details"]["Device"])
        issuePriority = data["details"]["Assurance Issue Priority"]
        issueSeverity = data["severity"]
        issueSummary = data["details"]["Assurance Issue Details"]

        data = "Warning Severity %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)

        webex(str(data))
        return("Cisco DNA Center JSON Payload received")
    else:
        return("Connection Alive")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cisco-dnac-platform-webex-notifications version %s' % version)
    parser.add_argument('--ssl', action='store_true', help="please enable SSL TODO")
    args = parser.parse_args()
    if args.ssl is True:
        print(" * SSL Enabled (ADHOC)")
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=False, ssl_context='adhoc')
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=False)
