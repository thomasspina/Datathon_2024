FROM python:3.9-slim

EXPOSE 80

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY ./config ./config
COPY ./src ./src
COPY ./main.py ./main.py

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=80", "--server.address=0.0.0.0"]