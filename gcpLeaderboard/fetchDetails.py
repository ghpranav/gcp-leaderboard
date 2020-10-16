# Import libraries
import requests
import urllib.request
import time
from pytz import timezone
from bs4 import BeautifulSoup
import fileinput
import json
import time
from datetime import datetime
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv(".env")
biglist = []
url = []
url2 = []

track1 = [
    "Getting Started: Create and Manage Cloud Resources",
    "Perform Foundational Infrastructure Tasks in Google Cloud",
    "Set up and Configure a Cloud Environment in Google Cloud",
    "Deploy and Manage Cloud Environments with Google Cloud",
    "Build and Secure Networks in Google Cloud",
    "Deploy to Kubernetes in Google Cloud",
]
track2 = [
    "Getting Started: Create and Manage Cloud Resources",
    "Perform Foundational Data, ML, and AI Tasks in Google Cloud",
    "Insights from Data with BigQuery",
    "Engineer Data in Google Cloud",
    "Integrate with Machine Learning APIs",
    "Explore Machine Learning Models with Explainable AI",
]
# get the url in list


def data_scraping(url):
    # print("in data scraping")
    fetchUrl = os.environ.get("FETCH_URL")
    f = urllib.request.urlopen(fetchUrl)
    for line in f:
        url.append(line.decode("utf8").replace("\n", ""))
    for ele in url:
        if ele.strip():
            url2.append(ele)
    start_thread(url2)

    # Connect to the URL


def data_gathering(link):
    tempdic = {}
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    track1completed = []
    track2completed = []
    profile = soup.findAll("div", attrs={"class": "public-profile__hero"})[0]
    dp = profile.img["src"]
    name = profile.h1.text
    tempdic["name"] = name.strip()
    tempdic["dp"] = dp
    quests = soup.findAll("ql-badge")
    for quest in quests:
        allquest = json.loads(quest.get("badge"))["title"]
        if allquest in track1:
            track1completed.append(allquest)
        if allquest in track2:
            track2completed.append(allquest)
    tempdic["track1"] = track1completed
    tempdic["track2"] = track2completed
    tempdic["qcomplete_no"] = len(track1completed) + len(track2completed)

    if tempdic["qcomplete_no"] != 0:
        biglist.append(tempdic)


def data_saving(biglist):
    # print("in data saving")
    res = sorted(biglist, key=lambda x: x["qcomplete_no"], reverse=True)
    now = datetime.now(timezone("Asia/Kolkata"))
    dt_string = now.strftime("%d/%m/%Y %H:%M") + " IST"
    with open("gcpLeaderboard/static/lastUpdated.txt", "w") as f:
        print(dt_string, file=f)
    with open("gcpLeaderboard/static/details.json", "w") as f:
        json.dump(res, f)
    f.close()


def start_thread(url2):
    threads = 10

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(data_gathering, url2)
    data_saving(biglist)


def main():
    # print("in main")
    data_scraping(url)


t0 = time.time()
main()
t1 = time.time()
print(f"{t1-t0} seconds to download {len(url2)} profile.")
print("number of people started", len(biglist))
