.PHONY: all clean build run

all: clean build run

clean:
	@echo todo

build:
	@echo Hello World

run:
	python src/api.py &
	streamlit run --server.port 53000 src/dashboard.py
