from bs4 import BeautifulSoup
from splinter import Browser
import os
import requests
import string
import pandas as pd 
import time


def scrape():

  executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
  browser = Browser('chrome', **executable_path, headless=False)
  url =f'https://mars.nasa.gov/news'
  browser.visit(url)
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')

  news_title = soup.find("div", class_="content_title").text
  # news_date = soup.find("div", class_="list_date").text
  # news_p = soup.find("div", class_="article_teaser_body").text


  # Dictionary entry from MARS NEWS
  # mars_info['news_title'] = news_title
  # mars_info['news_paragraph'] = news_p
  # mars_info['news_date'] = news_date
  # print(news_title)

  # Visit the url for JPL Featured Space Image
  url2 = (f"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
  browser.visit(url2)
  time.sleep(1)
  html2 = browser.html
  soup= BeautifulSoup(html2, 'html.parser')
  browser.click_link_by_id('full_image')
  time.sleep(3)
  html = browser.html
  soup = BeautifulSoup(html, "html.parser")
  image = soup.find("img", class_="fancybox-image")["src"]
  img_jpl = "https://www.jpl.nasa.gov" + image

  # visit the mars weather report twitter and scrape the latest tweet
  urlt =(f'https://twitter.com/marswxreport?lang=en')
  browser.visit(urlt)
  time.sleep(1)
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')
  mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
  # create dictionary entry
  # mars_info['mars_weather'] = mars_weather
  # print(mars_weather)
  
  # visit space facts and scrap the mars facts table
  url_fact=(f"https://space-facts.com/mars/")
  mars_facts = pd.read_html(url_fact)
  mars_df = mars_facts[0]
  mars_df.columns = ['Description','Value']
  mars_df.set_index('Description', inplace=True)
  
  mars_facts = mars_df.to_html()

  # scrape images of Mars' hemispheres from the USGS site
  urlmars= (f'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' )
  browser.visit(urlmars)
  time.sleep(1)
  htmlm = browser.html
  soup = BeautifulSoup(htmlm, 'html.parser')
  results = soup.find_all('h3')
  
  img_dict= []
  for r in results:
      text = r.get_text()
      title = text.strip('Enhanced')
      browser.click_link_by_partial_text(text)
      img_url = browser.find_link_by_partial_href('download')['href']
      img_dict.append({"title": title, "img_url": img_url})
      browser.back()
      # print(title)
      # print(img_url)
  mars_info = {
  "news_title": news_title,
  # "news_p": news_p,
  "img_jpl": img_jpl,
  "mars_weather": mars_weather,
  "mars_facts": mars_facts,
  "img_dict": img_dict,
  }

  # Close the browser after scraping
  browser.quit()
  
  # Return results
  # return mars_info
  return mars_info
        

if __name__ == "__main__":
   scrape()