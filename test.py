import requests

url = "http://127.0.0.1:8000/api/users/login/"
data = {
    "phone": "1234567890",
    "password": "1234"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
