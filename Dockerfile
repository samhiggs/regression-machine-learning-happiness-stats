# --------- STAGE 1: Get Artefacts
FROM amazon/aws-cli as download-artefacts

# For this to run you will need to configure your aws privileges in the projects directory
COPY ./.aws /root/.aws

RUN aws s3 cp s3://project-models/happiness-project/model /model --recursive

# --------- STAGE 2: Build App
FROM python:3.9.2-slim-buster as test

COPY --from=download-artefacts /model /model

RUN pip install pytest

COPY app /app
COPY tests /app/tests

WORKDIR /app

RUN ["pytest", "--rootdir", "tests"]

# --------- STAGE 3: Deploy App
FROM python:3.9.2-slim-buster as deploy

COPY --from=download-artefacts /model /model

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY app /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9696 8000

ENTRYPOINT ["/entrypoint.sh"]

