FROM python:3.8-slim-buster
WORKDIR /cisco-dnac-platform-webex-notifications/
COPY ./ ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]
