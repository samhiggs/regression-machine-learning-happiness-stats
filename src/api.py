from flask import Flask, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

def predict(payload, version='latest'):
    with open('model/kernelridge_model_v1.0.0.pkl', 'rb') as mdl_pkl:
        model = pickle.load(mdl_pkl)
        # Key Indicators
        indicators = ['economy',
                'family',
                'health',
                'freedom',
                'dystopia_residual',
                'internet_access_population[%]',
                'cellular_subscriptions',
                'GDP_per_capita[$]',
                'inflation_rate[%]']
    if len(payload.keys()) != 9:
        return 0
    df = pd.DataFrame([payload])
    return model.predict(df)[0]


@app.route('/score', methods=['POST'])
def score():
    request_data = request.get_json()
    return {"score" : predict(request_data)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)