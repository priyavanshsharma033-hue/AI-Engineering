import requests
baseurl="https://jsonplaceholder.typicode.com/posts"
def getpost(postid):
   
   try:
       response = requests.get(f"{baseurl}/{postid}")
       response.raise_for_status()  
       data = response.json()
       print(data)
   except requests.exceptions.RequestException as e:
       print(f"An error occurred: {e}")




def getallposts(userid):
    try:
        response = requests.get(f"{baseurl}?userId={userid}")
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


 

def createpost(title, body):
    newpost = {
        "title": title,
        "body": body,
        "userId": 1
    }
    try:
        response = requests.post(baseurl, json=newpost)
        response.raise_for_status()
        data = response.json()

        print("\nPost created successfully!")
        print("Post ID:", data["id"])
        print("User ID:", data["userId"])
        print("Title:", data["title"])
        print("Body:", data["body"])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")




while True:
    print("1. Get a post by ID")
    print("2. Get all posts by user ID")
    print("3. Create a new post")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        postid = input("Enter post id: ")
        getpost(postid)
    elif choice == "2":
        userid = input("Enter user id: ")
        getallposts(userid)
    elif choice == "3":
        title = input("Enter post title: ")
        body = input("Enter post body: ")
        createpost(title, body)
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")



