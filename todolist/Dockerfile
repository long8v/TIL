FROM python:3.6.8

RUN pip3 install flask flask_sqlalchemy redis flask_cors flask_mongoengine flask_redis blinker

# docker run path 
WORKDIR /usr/src/app

CMD ["python3", "main.py"]