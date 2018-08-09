FROM siangyeh8818/python-base-environment:3.6

RUN yum -y install npm crontabs.noarch net-tools
RUN npm install elasticdump -g
RUN wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
RUN python get-pip.py
RUN pip install -U elasticsearch-curator==5.5.4
RUN mkdir /code
WORKDIR /code
COPY run.sh /code
COPY dairy.py /code
COPY backup_data.py /code
RUN chmod +x /code/run.sh
RUN mkdir -p /curator
RUN mkdir -p /elasticsearch-backup
COPY curator.yaml /curator
COPY delete_index.yaml /curator
COPY crontabfile-backup /etc/cron.d/
CMD ["bash","/code/run.sh"]
