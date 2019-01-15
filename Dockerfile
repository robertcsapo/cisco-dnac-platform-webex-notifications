FROM python:alpine3.6
RUN apk add --no-cache git
RUN apk add --no-cache ca-certificates
RUN git clone https://github.com/robertcsapo/cisco-dnac-platform-webex-notifications
RUN pip install -r requirements.txt
CMD python run.py
