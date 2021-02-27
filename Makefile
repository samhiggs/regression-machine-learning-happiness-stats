.PHONY: all clean build run

all: clean-* docker-build docker-run

clean-py:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache

clean-nb:
	jupyter nbconvert --clear-output --inplace notebooks/*

clean-docker:
	docker stop happiness-regression

clean-all: clean-nb clean-py

docker-build:
	docker build -t happiness-regression .

docker-run:
	docker run \
		--rm \
		--detach \
		--publish 8000:8000 \
		--publish 9696:9696 \
		--name happiness-regression \
		happiness-regression

docker-mount-run:
	docker run \
		--rm \
		--interactive \
		--publish 8000:8000 \
		--publish 9696:9696 \
		--volume /mnt/c/Users/samhi/Documents/projects/regression-machine-learning-happiness-stats/app:/app \
		happiness-regression \
		--entrypoint /bin/bash

run:
	python app/src/api.py &
	streamlit run --server.port 8000 app/src/dashboard.py

run-jupyter:
	jupyter notebook --no-browser
