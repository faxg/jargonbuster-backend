FROM python:3.8


RUN apt-get update && \
     apt-get install -y openjdk-8-jdk-headless && \
    rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME  /usr/lib/jvm/java-8-openjdk-amd64/




###############################################################################################
########## PYTHON 
###############################################################################################


WORKDIR /usr/src/app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY swagger . 
COPY templates .
COPY summarizer .
COPY summarizer2 .


EXPOSE 5000

ENTRYPOINT ["python", "app.py"]