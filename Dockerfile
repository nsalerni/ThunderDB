FROM python:3

RUN set -ex \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends git build-essential libffi-dev python-dev 

ADD . /application
WORKDIR /application
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
CMD ["thunderdb"]
