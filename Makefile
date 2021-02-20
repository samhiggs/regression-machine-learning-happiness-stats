.PHONY: all clean build run

all: clean build run

clean:
	@echo todo

build:
	@echo Hello World

run:
	python app/src/api.py &
	streamlit run --server.port 53000 app/src/dashboard.py
