# base image

FROM centos/python-36-centos7:latest
#Environment Variables
ENV PYTHONUNBUFFERED 1

COPY . /opt/app-root/src
WORKDIR /opt/app-root/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# ENTRYPOINT ["python", "/opt/app-root/src/campaign_loader.py", "-c", "%1"]
