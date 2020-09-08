# base image

FROM centos/python-36-centos7:latest

#Environment Variables
ENV PYTHONUNBUFFERED 1
VOLUME ["/home/vagrant/dev/punchh/json_parser"]
WORKDIR /opt/app-root/src
COPY . /opt/app-root/src

RUN chown -R $USER:$USER .

# RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# ENTRYPOINT ["python", "campaign_loader.py"]
# CMD ["campaign_data.json"]
