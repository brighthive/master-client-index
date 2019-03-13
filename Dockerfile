FROM python:3.7.2-slim
WORKDIR /master-client-index
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system
ADD cmd.sh cmd.sh
RUN chmod a+x cmd.sh
ADD mci mci
ADD schema schema
ENTRYPOINT [ "/master-client-index/cmd.sh" ]