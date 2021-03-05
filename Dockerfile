###############################
# STAGE 1: Get Artefacts
FROM amazon/aws-cli as download-artefacts

# For this to run you will need to configure your aws privileges in the projects directory
# Keep it project specific so you can associate your keys with roles specific to the project
COPY ./.aws /root/.aws

RUN aws s3 cp s3://project-models/happiness-project/model /app/model --recursive
RUN aws s3 cp s3://project-models/happiness-project/data /app/data --recursive


###############################
# Base Image
FROM python:3.9.2-slim-buster as base


###############################
# STAGE 2: Build App
FROM base as build

COPY --from=download-artefacts /app /app

RUN mkdir /install

COPY requirements.txt /requirements.txt

RUN pip install --target=/install --no-cache-dir -r /requirements.txt

COPY app/src /app/src



###############################
# STAGE 3: Test App
FROM base as test

RUN pip install pytest

COPY tests /tests

RUN ["pytest", "--rootdir", "/tests"]



###############################
# STAGE 4: Deploy App
FROM base as deploy

COPY --from=build /app /app
COPY --from=build /install /usr/local/lib/python3.9/site-packages
COPY entrypoint.sh /entrypoint.sh

RUN useradd -m happydocker
USER happydocker

ENTRYPOINT ["/entrypoint.sh"]

