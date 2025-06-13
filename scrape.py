import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def scrape_pdf_links(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with href attributes
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Check if the link ends with .pdf (case-insensitive)
            if re.search(r'\.pdf$', href, re.IGNORECASE):
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(url, href)
                pdf_links.append(absolute_url)

        # Return the list of PDF links
        if pdf_links:
            """

            print("Found PDF links:")
            for pdf in pdf_links:
                print(pdf)
            """
            return pdf_links
        else:
            print("No PDF links found on the page.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    target_url = "https://nou.edu.ng/ecourseware-faculty-of-sciences/"  # Replace with your target URL
    scrape_pdf_links(target_url)