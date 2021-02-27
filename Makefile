.PHONY: all clean build run

all: clean build run

clean:
	@echo todo

build:
	docker build -t happiness-regression .

docker-run:
	docker run \
		--rm \
		-d \
		--publish 8000:8000 \
		--publish 9696:9696 \
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
