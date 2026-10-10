import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts"
)

data = response.json()

print(type(data))
print(len(data))
for post in data:
    print(post["title"])