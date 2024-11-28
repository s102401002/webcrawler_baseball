import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd

def download_image(url, save_path):
    
    response = requests.get(url)
    with open(save_path, "wb") as file:
        file.write(response.content)
    print("-"*30)
    pass

def main():
    url = "https://www.ptt.cc/bbs/Beauty/M.1686997472.A.FDA.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 
            'Cookie': 'over18=1'
            }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    spans = soup.find_all('span', class_="article-meta-value")
    title = spans[2].text
    dir_name = f"images/{title}"

    # 1. making a new dir
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 2. finding all images
    links = soup.find_all('a')
    allow_file_name = ["jpg", "png", "jpeg", "gif"]
    for link in links:
        href = link.get("href")
        if not href:
            continue
        extension = href.split('.')[-1].lower()
        file_name = href.split('/')[-1]
        if extension in allow_file_name:
            print(href)
            download_image(href, f"{dir_name}/{file_name}")

if __name__ == "__main__":
    main()