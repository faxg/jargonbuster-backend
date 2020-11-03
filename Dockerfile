FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY swagger . 
EXPOSE 5000

ENTRYPOINT ["python", "app.py"]