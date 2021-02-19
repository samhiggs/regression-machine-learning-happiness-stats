from flask import Flask
import pickle
import numpy as np

app = Flask(__name__)

def get_model(version='latest'):
    with open('kkr_model.pkl', 'rb') as mdl_pkl:
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
        example_input = [[1,1,1,1,1,1,1,1,1]]
        predict_happiness(indicators, model)

@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)