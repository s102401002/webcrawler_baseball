import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
url = "https://www.ptt.cc/bbs/Baseball/index16936.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
articles = soup.find_all("div", class_="r-ent")
# print(articles)
data_list = []
for article in articles:
    data = {}
    title = article.find("div", class_="title")
    if title and title.a:
        title = title.a.text
    else: 
        title = "None"
    data["title"] = title
    popular = article.find("div", class_="nrec")
    if popular and popular.span:
        popular = popular.span.text
    else: 
        popular = "N/A"
    data["popular"] = popular
    date = article.find("div", class_="date")
    if date:
        date = date.text
    else:
        date = "None"
    data["date"] = date
    author = article.find("div", class_="author")
    if author:
        author = author.text
    else:
        author = "None"
    data["author"] = author
    data_list.append(data)
    # print(f"標題：{title} 人氣：{popular} 日期：{date} 作者：{author}")
# print(data_list)
with open("ptt_baseball_data.json", "w", encoding="utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent=4)
df = pd.DataFrame(data_list)
df.to_csv("ptt_baseball_data.csv", index=False, header=False)
print("Success")
