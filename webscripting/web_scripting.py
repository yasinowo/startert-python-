import json
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup


def getSrc(tag, attr):
    if tag:
        if attr == "text":
            return tag.text.strip()
        return tag.get(attr)
    return None


class Card:
    def __init__(self, title, image_url, auther, price):
        self.title = title
        self.image_url = image_url
        self.auther = auther
        self.price = price


def writefile(filename, content, ex="html"):
    with open(f"{filename}.{ex}", "w", encoding="utf-8") as f:
        f.write(content)
        print(f"Written to {filename}.{ex}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.iranketab.ir/tag/1821-hot-books")

    page.wait_for_timeout(5000)
    html = page.content()
    # writefile("page_playwright", html)

soup = BeautifulSoup(html, "html.parser")
title_page = soup.find("h4", class_="font-bold text-break")

writefile("title", str(title_page))

cards = soup.find_all("a", class_="card product-card-simple")
print("card len", len(cards))
writefile("cards", str(cards[0]))
allCards = []
for card in cards:
    cardItem = Card(
        title=getSrc(
            card.find("h5", class_="text-sm text-default-800 font-bold truncate pt-2"),
            "text",
        ),
        image_url=getSrc(card.find("img"), "src"),
        auther=getSrc(
            card.find("h6", class_="text-xs text-default truncate pt-1"), "text"
        ),
        price=getSrc(card.find("s", class_="price text-default"), "text"),
    )
    allCards.append(cardItem)

allCardsDict = [c.__dict__ for c in allCards]

with open("allCards.json", "w", encoding="utf-8") as f:
    json.dump(allCardsDict, f, ensure_ascii=False, indent=4)

print("Written allCards.json successfully!")
