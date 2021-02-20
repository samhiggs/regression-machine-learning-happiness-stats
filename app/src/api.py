from flask import Flask, request
import pickle
import pandas as pd
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def predict(payload, version='latest'):
    with open('model/kernelridge_model_v1.0.0.pkl', 'rb') as mdl_pkl:
        model = pickle.load(mdl_pkl)
        if model is None:
            app.logger.error("Model didn't load")
            return 0
        # Key Indicators
        # indicators = ['economy',
        #         'family',
        #         'health',
        #         'freedom',
        #         'dystopia_residual',
        #         'internet_access_population[%]',
        #         'cellular_subscriptions',
        #         'GDP_per_capita[$]',
        #         'inflation_rate[%]']
    if len(payload.keys()) != 9:
        return 0
    df = pd.DataFrame([payload])
    return model.predict(df)[0]


@app.route('/score', methods=['POST'])
def score():
    app.logger.info("HELO")
    request_data = request.get_json()
    app.logger.info(request_data)
    pred = predict(request_data)
    app.logger.info(pred)
    return {"score": pred}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
