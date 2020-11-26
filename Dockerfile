FROM python:3.8


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/




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