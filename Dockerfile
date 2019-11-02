FROM python:3.7-slim-buster
RUN apt-get update && apt-get install -y git
#TODO
RUN git clone https://github.com/robertcsapo/cisco-dnac-platform-webex-notifications

WORKDIR /cisco-dnac-platform-webex-notifications/
# TODO
#ADD . /cisco-dnac-platform-webex-notifications/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]
