FROM tensorflow/tensorflow:latest

COPY . /app

RUN apt-get -y update

RUN apt-get -y upgrade

RUN pip install -r app/requirements.txt

CMD python app/prediction.py