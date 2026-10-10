import requests

new_post = {
    "title": "Learning AI Engineering",
    "body": "I am learning APIs.",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post
)

print(response.status_code)
print(response.json())