FROM python:3.8

WORKDIR /usr/src/app

RUN apt-get install openjdk-11-jdk

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY swagger . 
COPY templates .
COPY summarizer .

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]