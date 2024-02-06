from django.urls import path
from news.views import (
    scrape, 
    homepage, 
    test_scrape_news, 
    aboutproject, 
    contact, 
    check_for_updates
)


urlpatterns = [
  path('scrape/<str:name>', scrape, name="scrape"),
  path('test_scrape_news/', test_scrape_news, name='test_scrape_news'),
  path('', homepage, name="home"),
  path('aboutproject/', aboutproject, name='aboutproject'),
  path('contact/', contact, name='contact'),
  path('check_for_updates/', check_for_updates, name='check_for_updates'),

]