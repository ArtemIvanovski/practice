from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = '4d29fffff502452bcd37d55f83b66401'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


def fetch_weather_data(city=None, method='GET'):
    params = {'appid': API_KEY}
    if city:
        params['q'] = city

    try:
        if method == 'GET':
            response = requests.get(BASE_URL, params=params)
        elif method == 'DELETE':
            response = requests.delete(BASE_URL, params=params)
        elif method == 'POST':
            response = requests.post(BASE_URL, params=params)
        else:
            return jsonify({'error': 'Invalid request method'}), 400

        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as err:
        return jsonify({'error': str(err)}), response.status_code


@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    return fetch_weather_data(city=city)


@app.route('/weather', methods=['DELETE'])
def delete_weather():
    return fetch_weather_data(method='DELETE')


@app.route('/weather', methods=['POST'])
def bad_request():
    return fetch_weather_data(method='POST')


@app.route('/simulate_error', methods=['GET'])
def simulate_error():
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
