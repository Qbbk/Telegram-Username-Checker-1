import requests
from lxml import html
from tqdm import tqdm

def check_username(username):
    url = f"https://t.me/{username}"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    user_icon = tree.xpath('//*[@class="tgme_icon_user"]')
    return len(user_icon) > 0

def main():
    valid_usernames = []
    file_path = "/Users/mac/user/list.txt"
    valid_file_path = "/Users/mac/user/valid.txt"

    with open(file_path, "r") as file:
        usernames = file.read().splitlines()
        progress_bar = tqdm(usernames, desc="Checking usernames", unit="username")
        for username in progress_bar:
            if check_username(username):
                valid_usernames.append(username)

    with open(valid_file_path, "w") as valid_file:
        for username in valid_usernames:
            valid_file.write(username + "\n")

    print("Valid Usernames:")
    for username in valid_usernames:
        print(username)

if __name__ == "__main__":
    main()
