# cisco-dnac-platform-webex-notifications
## Receive Events from Cisco DNA-C and push the information to Cisco Webex Teams

## Disclaimer
* This solution isn't using Username/Password header with Cisco DNA-C (let me know if needed)
* Host this solution behind something that handles encryption (TLS) - else the payload is unencrypted from DNA-C

![](cisco.dnac.webex.teams.assurance.jpg)

## How to run
```
docker run -d -p 5000:5000 -e WEBEX_TEAMS_ACCESS_TOKEN="TOKEN" -e WEBEX_TEAMS_ROOM_ID="ID" robertcsapo/cisco-dnac-platform-webex-notifications
```

Then point your Cisco DNA-C Webhook to <ip>:5000/dnac (POST) as URL

## Troubleshooting
### Sample - /sample URL (GET)
Sends Sample data from outputdata.json

### Webex - /webex URL (GET)
Sends Sample data to Webex Room

### Post Sample (POST) - /postsample URL
Send your own JSON sample data to URL Path (use POST Method and Postman)
