FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN mkdir /app && mkdir /app/dfi/ && mkdir /app/tests/
WORKDIR /app

ADD dfi/ /app/dfi/
ADD tests/ /app/tests/
ADD setup.py /app/
ADD input.txt /app/
RUN virtualenv /app && source /app/bin/activate && /app/bin/python setup.py test && /app/bin/python setup.py install

