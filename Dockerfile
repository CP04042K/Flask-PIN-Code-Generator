FROM python:3.8-slim-buster

WORKDIR /app

ENV FLASK_DEBUG=1
RUN pip3 install flask

COPY ./src/ .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]