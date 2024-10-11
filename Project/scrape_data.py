# Required Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Define function for scraping data


def scrape_data(url_list, url_id):
    count = 0
    for url_link in url_list:
        response = requests.get(url_link)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Initialize variables
        title = ""
        extracted_text = ""

        # Get title
        try:
            title_element = soup.find(
                'h1', class_='entry-title') or soup.find('h1', class_='tdb-title-text')
            if title_element:
                title = title_element.text.strip()
            print(f"Title: {title}\n")
        except Exception as e:
            print(f"Error fetching title for {url_link}: {e}")
            title = ""

        # Get post content
        try:
            post_content = soup.find('div', class_='td-post-content')

            if post_content:
                # Remove 'pre' tags with class 'wp-block-preformatted' if they exist
                pre_tag = post_content.find('pre')
                if pre_tag:
                    pre_tag.extract()

                extracted_text = post_content.get_text().strip()
                # Show a snippet of the extracted text
                print(f"Extracted Text: {extracted_text[:100]}...\n")
            else:
                print(f"No post content found for {url_link}")
                extracted_text = ""
        except Exception as e:
            print(f"Error fetching post content for {url_link}: {e}")
            extracted_text = ""

        # Define path for exporting file in folder
        path = f"./data/{url_id[count]}.txt"

        # Export data in txt file
        try:
            with open(path, 'w', encoding="utf-8") as file:
                # Write title and content to the file
                file.write(f"{title}\n\n")
                file.write(f"{extracted_text}")
            print(f"Data saved to {path}")
        except Exception as e:
            print(f"Error saving data for {url_link}: {e}")

        count += 1


# Read data from Excel file
input_data = pd.read_excel("Input.xlsx")
urls = input_data["URL"]
url_id = input_data['URL_ID']
path = os.path.join(os.getcwd(), 'data')
# Ensure output directory exists
if not os.path.exists(path):
    os.makedirs(path)
    print(f"Directory '{path}' created.")
else:
    print(f"Directory '{path}' already exists.")

# Call the scrape_data function
scrape_data(urls, url_id)

print("\n\nData extracted successfully...")
