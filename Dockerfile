FROM python:2.7-alpine
MAINTAINER yangping <yangping@sci99.com>

RUN apk add -U tzdata
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
RUN apk del tzdata

RUN mkdir /code
ADD ./project/requirements.txt /code
RUN pip install -r /code/requirements.txt -i https://pypi.douban.com/simple

WORKDIR /code

ENTRYPOINT ["python", "main.py"]
