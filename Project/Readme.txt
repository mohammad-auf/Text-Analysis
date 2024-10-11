Program Overview
This project consists of two main components:

Text Analysis: Analyzes the textual content of articles to generate metrics such as sentiment scores, readability, personal pronoun counts, syllable counts, and more.

Web Scraping: Scrapes articles from URLs and extracts the title and post content, which are then saved as text files for further analysis.

Features

1) Web Scraping:
Scrapes article titles and content from given URLs.
Saves each article to a .txt file named according to its URL_ID.

2) Text Analysis:

Cleans text by removing stopwords and non-alphabetical characters.
Analyzes sentiment using a predefined dictionary of positive and negative words.
Measures readability (average sentence length, complex word percentage, Fog Index).
Calculates average syllables per word, word length, and personal pronoun count.


Prerequisites:
Python 3.x installed on your system.

Required Libraries: Install the necessary libraries using pip:

pip install pandas nltk requests beautifulsoup4

Files and Directory Structure:

Input.xlsx: Contains URLs and URL_IDs for scraping and analysis.
StopWords/: Contains text files with stopwords (e.g., stopwords.txt).
MasterDictionary/: Contains sentiment dictionaries positive-words.txt and negative-words.txt.
data/: Stores the article text files after analysis.

How to Run:
1)Ensure that the required text files (Input.xlsx, stopwords, and dictionaries) are in place.
2)Run the text analysis script : - python text_analysis.py
3)The analysis results will be saved in an Excel file named Output Data Structure.xlsx.


Conclusion:
This project allows you to scrape and analyze textual data from websites, providing insights into the sentiment, readability, and linguistic features of the text.

