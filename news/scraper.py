# THE SCRAPING LOGIC

import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from datetime import datetime, timedelta
import time
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def scrape_news(name):
    try:
        session = requests.Session()
        session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

        url = f"https://www.theonion.com/{name}"
        response = session.get(url)
        response.raise_for_status()

        content = response.content
        soup = BSoup(content, "html.parser")
        News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})

        for article in News:
            linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
            link = linkx["href"]

            titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
            title = titlex.text

            imgx = article.find("img")["data-src"]

            if not Headline.objects.filter(title=title).exists():
                new_headline = Headline()
                new_headline.title = title
                new_headline.url = link
                new_headline.image = imgx
                new_headline.category = name
                new_headline.save()
            else:
                logger.info(f"Skipping duplicate headline: {title}")

    except requests.RequestException as e:
        logger.error(f"Error during request: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    finally:
        pass

def send_notification(title, message, task_id):

		# Update notification_sent to True after successfully sending the notification
		headline = Headline.objects.get(id=task_id)
		headline.notification_sent = True
		headline.save()

	