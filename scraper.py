# Theoretically, scrapes change.org for animal welfare petitions.
# Fails because it's using a Mozilla agent rather than Edge

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# ---- CONFIGURATION ----
KEYWORDS = ["animal welfare"]
NUM_RESULTS = 5  # per keyword
OUTPUT_FILE = "petitions.csv"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (compatible; PetitionFinder/1.0)"}

# ---- HELPER FUNCTIONS ----
def google_search(query, num_results=5):
  """Search Google for change.org petitions matching a keyword."""
  urls = []
  search_url = "https://www.google.com/search"
  params = {"q": f"site:change.org {query}", "num": num_results}

  response = requests.get(search_url, params=params, headers=USER_AGENT)
  soup = BeautifulSoup(response.text, "html.parser")

  # Open a text file in write mode
  with open("output.txt", "w") as file:
    # Write the variable to the file
    file.write(str(soup))

  for link in soup.select("a"):
      href = link.get("href", "")
      if "change.org/p/" in href:
          clean_url = re.findall(r"https://www\.change\.org/p/[^\&]+", href)
          if clean_url:
              urls.append(clean_url[0])
  return list(set(urls))  # remove duplicates


def scrape_petition(url):
    """Extract petition title and summary from a Change.org page."""
    try:
        resp = requests.get(url, headers=USER_AGENT, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.find("h1")
        if title:
            title = title.get_text(strip=True)
        else:
            title = "N/A"

        summary = soup.find("p")
        if summary:
            summary = summary.get_text(strip=True)
        else:
            summary = "N/A"

        return {"url": url, "title": title, "summary": summary}
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {"url": url, "title": "Error", "summary": str(e)}


# ---- MAIN SCRAPER ----
if __name__ == "__main__":
  all_results = []

  # Does a Google Search for the relevant keywords
  for kw in KEYWORDS:
    print(f"\n🔍 Searching for petitions about '{kw}'...")
    urls = google_search(kw, NUM_RESULTS)
    print(f"Found {len(urls)} petitions.")

    for u in urls:
      print(f"  Scraping: {u}")
      data = scrape_petition(u)
      data["keyword"] = kw
      all_results.append(data)
      time.sleep(2)  # be gentle to servers

  df = pd.DataFrame(all_results)
  df.to_csv(OUTPUT_FILE, index=False)
  print(f"\n✅ Done! Results saved to {OUTPUT_FILE}")
