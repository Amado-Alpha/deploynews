import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline
from datetime import datetime, timedelta
import time
from NewsAggregator.celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from .scraper import send_notification
from django.contrib import messages

logger = get_task_logger(__name__)




@app.task(bind=True)
def auto_scrape_news(self, target_names):
	for target_name in target_names:
		try:
			session = requests.Session()
			session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

			url = f"https://www.theonion.com/{target_name}"
			response = session.get(url)
			response.raise_for_status()

			content = response.content
			soup = BSoup(content, "html.parser")
			News = soup.find_all("div", {"class": "sc-cw4lnv-13 hHSpAQ"})

			"""
			This will display news items in the celery worker terminal
			Anywhere in the program this statement performs similar function
			"""
			logger.info(f"Found {len(News)} news items.")

			for article in News:
				linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
				link = linkx["href"]

				titlex = article.find("h2", {"class": "sc-759qgu-0 cvZkKd sc-cw4lnv-6 TLSoz"})
				title = titlex.text

				imgx = article.find("img")["data-src"]

				if not Headline.objects.filter(title=title).exists():
				   
					new_update = Headline()
					new_update.title = title
					new_update.url = link
					new_update.image = imgx
					new_update.notification_sent = False
					new_update.category = target_name
					new_update.save()

					send_notification(title, "New update!", str(new_update.id))

				else:
					logger.info(f"Skipping duplicate headline: {title}")
				
		except requests.RequestException as e:
			logger.error(f"Error during request: {e}")

		except Exception as e:
			logger.error(f"An unexpected error occurred: {e}")

		finally:
			pass

