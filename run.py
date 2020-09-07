import json
import os
import argparse
import sys
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI


__app__ = "cisco-dnac-platform-webex-notifications"
__version__ = "1.3.3"
__author__ = "Robert Csapo"
__email__ = "rcsapo@cisco.com"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

""" Read Cisco Webex Teams Settings either for Environment or in Code """
if "WEBEX_TEAMS_ACCESS_TOKEN" not in os.environ:
    webexAPI = WebexTeamsAPI(access_token="CHANGEME")
else:
    webexAPI = WebexTeamsAPI()

if "WEBEX_TEAMS_ROOM_ID" not in os.environ:
    os.environ["WEBEX_TEAMS_ROOM_ID"] = "CHANGEME"
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]
else:
    webexRoomId = os.environ["WEBEX_TEAMS_ROOM_ID"]

""" Verify Cisco Webex Teams Settings """


def webex_init_healthcheck():
    results = {}
    try:
        bot = webexAPI.people.me()
        results["bot_name"] = bot.displayName
        emails = []
        for email in bot.emails:
            emails.append(email)
        results["bot_emails"] = emails
        room = webexAPI.rooms.get(webexRoomId)
        results["room_title"] = room.title
        results["status"] = True
    except Exception as e:
        results["status"] = False
        print(e)
    return results


app = Flask(__name__)

""" Main page """


@app.route("/", methods=["GET", "POST"])
def mainPage():
    if request.method == "GET":
        return "{} version {} -> by {} ({})".format(
            __app__, __version__, __author__, __email__
        )
    if request.method == "POST":
        return "{} healthcheck".format(__app_)

    return None


""" Sample post with included file """


@app.route("/sample", methods=["GET"])
def sample():
    jsonFile = "outputdata.json"
    with open(jsonFile) as f:
        data = json.load(f)

    issueTitle = data["details"]["Type"] + " " + data["details"]["Device"]
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]

    data = "Warning Severity %s (%s)! %s - %s" % (
        issueSeverity,
        issuePriority,
        issueTitle,
        issueSummary,
    )
    webex(str(data))
    return "Sample data from -> %s" % jsonFile


""" Sample post with sent file """


@app.route("/postsample", methods=["POST"])
def postSample():
    data = request.json

    issueTitle = data["details"]["Type"] + " " + data["details"]["Device"]
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]

    data = "Warning Severity %s (%s)! %s - %s" % (
        issueSeverity,
        issuePriority,
        issueTitle,
        issueSummary,
    )

    webex(str(data))
    return "Sample JSON Payload received"


""" Cisco Webex Teams Interface """


@app.route("/webex", methods=["GET"])
def webex(*data):
    if not len(data) == 0:
        data = data[0]
        webexAPI.messages.create(webexRoomId, text=data)
    else:
        webexAPI.messages.create(webexRoomId, text="Sample connection!")
    return "Sample Cisco Webex Teams Message"


""" Cisco DNA Center Incoming Events Interface """


@app.route("/dnac", methods=["POST"])
def dnacPayload():
    data = request.json
    if not len(data) == 0:

        issueTitle = data["details"]["Type"] + " " + data["details"]["Device"]
        issuePriority = data["details"]["Assurance Issue Priority"]
        issueSeverity = data["severity"]
        issueSummary = data["details"]["Assurance Issue Details"]

        data = "Warning Severity %s (%s)! %s - %s" % (
            issueSeverity,
            issuePriority,
            issueTitle,
            issueSummary,
        )

        webex(str(data))
        return "Cisco DNA Center JSON Payload received"
    return "Connection Alive"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="{} {}".format(__app__, __version__))
    parser.add_argument("--ssl", action="store_true", help="enable SSL ADHOC")
    args = parser.parse_args()

    webex_init = webex_init_healthcheck()
    if webex_init["status"] is False:
        print("Problem with Cisco Webex Teams Settings {}".format(webex_init))
        sys.exit()
    else:
        print(
            " * Cisco Webex Teams: {} - {} - {}".format(
                webex_init["bot_name"],
                webex_init["room_title"],
                webex_init["bot_emails"],
            )
        )

    if args.ssl is True:
        print(" * SSL Enabled (ADHOC)")
        app.run(
            host="0.0.0.0", port=5000, threaded=True, debug=False, ssl_context="adhoc"
        )
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=False)
