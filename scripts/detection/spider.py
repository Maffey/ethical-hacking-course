#! /usr/bin/env python
# Compatibility: Python 3.x

import requests
import re
from urllib.parse import urljoin


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)(?:")', response.content.decode(errors="ignore"))


def crawl(url):

    href_links = extract_links_from(url)

    for link in href_links:
        link = urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


# Can be tested at: https://www.crawler-test.com/
target_url = "http://10.0.2.4"
target_links = []

crawl(target_url)
