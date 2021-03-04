#! /bin/bash

python app/src/api.py &
python -m streamlit run --server.port $PORT app/src/dashboard.py