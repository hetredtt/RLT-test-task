import requests

async def answer(json_data):
    url = "http://127.0.0.1:7000/aggregate"
    response = requests.post(url, json=json_data)
    data = response.json()
    print(data)
    return data