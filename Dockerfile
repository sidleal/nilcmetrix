# cohmetrix
FROM ubuntu:focal

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update 
RUN apt install -y python3 python3-pip python3-numpy 
RUN apt install -y default-jre
#RUN apt install -y python3 python3-pip locales libpq-dev libxml2-dev libxslt1-dev python3-dev python3-lxml
#RUN apt-get install -y python3-numpy python3-scipy python3-matplotlib ipython ipython-notebook python3-pandas python3-sympy python3-nose
#RUN apt-get install -y python3-sklearn default-jre

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools 

WORKDIR /opt/text_metrics

COPY . .

#RUN cd tools/nlpnet-py3 && python3 setup.py install  && cd ..
RUN pip3 install https://github.com/kpu/kenlm/archive/master.zip
RUN pip3 install psycopg2-binary

RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 -m nltk.downloader all

RUN cd tools/idd3 && python3 setup.py install

WORKDIR /opt/text_metrics
