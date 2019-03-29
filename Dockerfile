FROM python:3.7.2-slim
WORKDIR /master-client-index
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc and-build-dependencies \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip && pip install pipenv && pipenv install --system \
    && apt-get purge -y --auto-remove gcc and-build-dependencies
ADD cmd.sh cmd.sh
RUN chmod a+x cmd.sh
ADD mci mci
ENTRYPOINT [ "/master-client-index/cmd.sh" ]
