#!/usr/bin/env python3
"""
Baidu Push Script for aitoolbox.hk (English Site)
Push all URLs from sitemap.xml to Baidu.
"""
import requests
import re
import os

# Configuration
TOKEN = "SQjY1PUxykFOlFUk"  # Replace with your actual token
SITE = "https://www.aitoolbox.hk"
SITEMAP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sitemap.xml")

def get_urls_from_sitemap(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"<loc>(https?://[^<]+)</loc>", content)

def push_to_baidu(urls):
    if not TOKEN or "YOUR_BAIDU_TOKEN" in TOKEN:
        print("[ERROR] Please provide your Baidu token in the script.")
        return

    # Respect Baidu's 10-link limit for unverified sites
    limited_urls = urls[:10]
    print(f"Pushing top {len(limited_urls)} URLs (Home + latest) to Baidu...")
    
    api_url = f"http://data.zz.baidu.com/urls?site={SITE}&token={TOKEN}"
    data = "\n".join(limited_urls)
    try:
        response = requests.post(api_url, data=data, headers={"Content-Type": "text/plain"})
        print(f"Baidu Push Result: {response.text}")
    except Exception as e:
        print(f"Baidu Push Error: {e}")

if __name__ == "__main__":
    if os.path.exists(SITEMAP_PATH):
        urls = get_urls_from_sitemap(SITEMAP_PATH)
        print(f"Found {len(urls)} URLs in sitemap.xml")
        push_to_baidu(urls)
    else:
        print(f"[ERROR] Sitemap not found at {SITEMAP_PATH}")
