FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install python3-pip python-dev

RUN mkdir -p /home/app

COPY randimg.py requirements.txt /home/app/
RUN pip3 install -r /home/app/requirements.txt

EXPOSE 5000

WORKDIR /home/app
CMD ["python3", "randimg.py"]