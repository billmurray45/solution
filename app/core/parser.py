from fastapi import APIRouter
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List

router = APIRouter()


class NewsItem(BaseModel):
    title: str
    date: str
    link: str
    image: str


def fetch_news():
    url = "https://yu.edu.kz/ru/news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    news = []
    for item in soup.select("div.item"):
        title_tag = item.select_one("a.title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag["href"] if title_tag and title_tag.has_attr("href") else ""

        date_tag = item.select_one("span.date")
        date = date_tag.get_text(strip=True) if date_tag else ""

        thumb_div = item.select_one("div.thumbnail")
        image = ""
        if thumb_div and "background-image" in thumb_div.get("style", ""):
            bg = thumb_div["style"]
            import re
            m = re.search(r'url\(([^)]+)\)', bg)
            if m:
                image = m.group(1)

        news.append(NewsItem(
            title=title,
            date=date,
            link=link,
            image=image
        ))
    return news


@router.get("/news/", response_model=List[NewsItem])
def get_news():
    return fetch_news()
