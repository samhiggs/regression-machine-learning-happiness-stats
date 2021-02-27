#! /bin/bash

python app/src/api.py &
streamlit run --server.port 8000 app/src/dashboard.py