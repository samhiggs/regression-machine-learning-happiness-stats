HEROKU_REGISTRY 			  := "registry.heroku.com"
APP_NAME 							:= "happiness-regression-app"
HEROKU_PROCESS_TYPE 	 := "web"
IMAGE_NAME 						 := $(HEROKU_REGISTRY)/$(APP_NAME)/$(HEROKU_PROCESS_TYPE)
PORT 									 := 8000
LOCAL_API_PORT 					:= 9696

.PHONY: all clean build run

all: clean-* docker-build docker-run

clean-py:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache

clean-nb:
	jupyter nbconvert --clear-output --inplace notebooks/*

clean-files:
	rm app/data/*
	rm app/model/*

clean-all: clean-*

download-files:
	$(shell aws s3 cp s3://project-models/happiness-project/model app/model --recursive && \
		 aws s3 cp s3://project-models/happiness-project/data app/data --recursive)

clean-docker:
	docker stop $(IMAGE_NAME)

clean-all: clean-nb clean-py

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run \
		--rm \
		--detach \
		--env PORT=$(PORT) \
		--publish $(PORT):$(PORT) \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME)

docker-mount-run:
	docker run \
		--rm \
		--interactive \
		--env PORT=$(PORT) \
		--publish $(PORT):$(PORT) \
		--publish $(LOCAL_API_PORT):$(LOCAL_API_PORT) \
		--name $(IMAGE_NAME) \
		--volume /mnt/c/Users/samhi/Documents/projects/regression-machine-learning-happiness-stats/app:/app \
		$(IMAGE_NAME) \
		--entrypoint /bin/bash

run:
	python app/src/api.py &
	streamlit run --server.port $(PORT) app/src/dashboard.py

run-jupyter:
	jupyter notebook --no-browser
