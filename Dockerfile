###############################
# STAGE 1: Get Artefacts
FROM amazon/aws-cli as download-artefacts

# For this to run you will need to configure your aws privileges in the projects directory
COPY ./.aws /root/.aws

RUN aws s3 cp s3://project-models/happiness-project/model /app/model --recursive
RUN aws s3 cp s3://project-models/happiness-project/data /app/data --recursive

###############################
# STAGE 2: Build App
FROM python:3.9.2-slim-buster as test

COPY app/src /app/src
COPY --from=download-artefacts /model /app/model
COPY --from=download-artefacts /data /app/data

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt && pip install pytest

COPY tests /tests

WORKDIR /app

RUN ["pytest", "--rootdir", "tests"]

###############################
# STAGE 3: Deploy App
FROM python:3.9.2-slim-buster as deploy

COPY --from=test /app /app
COPY --from=test /requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9696 8000

ENTRYPOINT ["/entrypoint.sh"]

