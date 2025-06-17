import requests

url = "http://127.0.0.1:8000/api/chat"
data = {
    "messages": [
        {"role": "user", "content": "Hi Alverri, who are you?"}
    ]
}

res = requests.post(url, json=data)
print(res.json())
