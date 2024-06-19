import requests


def fetch_status(url):
    try:
        response = requests.get(url)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return str(e)


if __name__ == "__main__":
    # 200
    status, data = fetch_status(
        "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=4d29fffff502452bcd37d55f83b66401")
    print(f"Status: {status}, Data: {data}")

    # 400
    status, data = fetch_status(
        "https://api.openweathermap.org/data/2.5/weather?lat=-&lon=10.99&appid=4d29fffff502452bcd37d55f83b66401")
    print(f"Status: {status}, Data: {data}")

    # 401
    status, data = fetch_status(
        "https://api.openweathermap.org/data/3.0/onecall/timemachine?appid=aab2ed3489b0183f0de077dfe3e56826")
    print(f"Status: {status}, Data: {data}")

    # 404
    status, data = fetch_status(
        "https://api.openweathermap.org/data/2.5/weathe?lat=-&lon=10.99&appid=4d29fffff502452bcd37d55f83b66401")
    print(f"Status: {status}, Data: {data}")
