#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image scraping script using Selenium and requests.

Credits:
Original inspiration from:
https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d

Special thanks to Debjyoti Paul.
"""

import time
import requests
import io
import hashlib
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def fetch_image_urls_util(url, driver_path):
    images = []
    service = Service(executable_path=driver_path)
    with webdriver.Chrome(service=service) as wd:
        try:
            wd.get(url)
        except:
            return []

        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img[class='irc_mi']")
        for img in thumbnail_results:
            src = img.get_attribute('src')
            if src and 'http' in src:
                images.append(src)
    return images


def fetch_image_urls(query: str, max_links_to_fetch: int, wd, sleep_between_interactions: int = 1,
                     driver_path=None, target_path=None, search_term=None):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=query))

    image_urls = set()
    # print("image_urls", image_urls)
    image_count = 0
    d = {}

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
        number_results = len(thumbnail_results)
        print(f"Found: {number_results} search results. Extracting links...")

        for img in thumbnail_results[50:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception as e:
                print(f"Thumbnail click failed: {e}")
                continue

            links = wd.find_elements(By.CSS_SELECTOR, "a[jsname='sTFXNd']")
            print("links", links)
            for link in links:
                href = link.get_attribute('href')
                if href and 'http' in href and href not in d:
                    d[href] = True
                    getactualurl = fetch_image_urls_util(href, driver_path) or []
                    for imageurl in getactualurl:
                        if imageurl:
                            image_urls.add(imageurl)

            if len(image_urls) >= max_links_to_fetch / 10:
                print(f"Collected {len(image_urls)} image links. Saving...")
                try:
                    for elem in image_urls:
                        persist_image(target_folder, elem)
                except Exception as e:
                    print(f"Error saving images: {e}")
                image_urls.clear()
                d.clear()

            image_count += len(image_urls)

        if image_count >= max_links_to_fetch:
            print(f"Done! Collected {image_count} image links.")
            break
        else:
            print(f"Found {image_count} so far, looking for more...")
            time.sleep(10)

    return image_urls


def persist_image(folder_path: str, url: str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Status code: {response.status_code}")
        image_content = response.content
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        return

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./datasets', number_images=2):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    service = Service(executable_path=driver_path)
    with webdriver.Chrome(service=service) as wd:
        res = fetch_image_urls(
            search_term,
            number_images,
            wd=wd,
            sleep_between_interactions=0.5,
            driver_path=driver_path,
            target_path=target_path,
            search_term=search_term
        )

    try:
        for elem in res:
            persist_image(target_folder, elem)
    except Exception as e:
        print(e)


# -----------------------------
# Run the scraper for a query
# -----------------------------
if __name__ == "__main__":
    queries = ["Virat kohli"]  # Add more if needed
    driver_path = "C:/Windows/chromedriver.exe"  # Make sure this path is correct

    for query in queries:
        search_and_download(query, driver_path)
