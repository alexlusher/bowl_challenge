# base image

# base image
FROM docker.io/ubuntu

RUN apt-get update -y
RUN apt install software-properties-common wget apt-utils -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update -y
RUN apt-get install python3.7 -y
ENV PYTHONPATH=/usr/bin/python3.7
ENV PATH=/usr/bin:/usr/lib/python3.7:$PATH
ENV alias python=python3.7
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.7 get-pip.py

VOLUME ["/home/vagrant/dev/punchh/json_parser"]
WORKDIR /opt/app-root/src
COPY . /opt/app-root/src

RUN chown -R $USER:$USER .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python3.7", "campaign_loader.py"]
CMD ["campaign_data.json"]
