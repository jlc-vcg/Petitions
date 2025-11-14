import requests
from bs4 import BeautifulSoup

def scrape_titles(url):
    """
    Scrapes and prints article titles from the given URL.
    """
    try:
        # Send HTTP GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []

    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Find all <h1> tags with class 'title'
    titles = [tag.get_text(strip=True) for tag in soup.find_all('h1')]

    return titles

if __name__ == "__main__":
    # Example site (replace with your target site)
    target_url = "https://example.com"

    titles = scrape_titles(target_url)

    if titles:
        print("Found article titles:")
        for idx, title in enumerate(titles, start=1):
            print(f"{idx}. {title}")
    else:
        print("No titles found.")