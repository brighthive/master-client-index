FROM python:3.7.2-slim
WORKDIR /master-client-index
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

RUN apt-get update \
    && apt-get install -y git \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip && pip install pipenv && pipenv install --system \
    && apt-get purge -y --auto-remove gcc
ADD wsgi.py wsgi.py
ADD cmd.sh cmd.sh
RUN chmod a+x cmd.sh
ADD mci mci
ENTRYPOINT [ "/master-client-index/cmd.sh" ]
