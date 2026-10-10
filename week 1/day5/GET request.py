import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

data = response.json()

print(data)
print(response.status_code)
print(data["title"])
print(data["body"])
print(type(data))
print(data.keys())