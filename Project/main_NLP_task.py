import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import os
# Download NLTK resources (only required if not already downloaded)
nltk.download('punkt')


def clean_text(text, stop_words):
    words = word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha()
                     and word not in stop_words]
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text


def extract_personal_pronouns(text):
    personal_pronouns_count = len(re.findall(
        r'\b(I|we|my|ours|us)\b', text, flags=re.IGNORECASE))
    return personal_pronouns_count


def analyze_sentiment(text, positive_dict, negative_dict):
    positive_score = sum(1 for word in text.split() if word in positive_dict)
    negative_score = sum(1 for word in text.split()
                         if word in negative_dict) * -1
    # Use abs to avoid negative total
    total_words = positive_score + abs(negative_score)
    polarity_score = (positive_score - abs(negative_score)) / \
        (total_words + 0.000001)
    subjectivity_score = (positive_score + abs(negative_score)
                          ) / (len(text.split()) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score


def analyze_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    complex_words = [word for word in words if len(word) > 2]
    percentage_complex_words = len(complex_words) / len(words) if words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    return avg_sentence_length, percentage_complex_words, fog_index, len(complex_words), len(words)


def syllable_count(word):
    vowels = "aeiouy"
    count = sum(1 for char in word if char.lower() in vowels)
    return count if count > 0 else 1  # at least one syllable for any word


def avg_syllables_per_word(text):
    words = word_tokenize(text)
    total_syllables = sum(syllable_count(word) for word in words)
    # Prevent division by zero
    return total_syllables / len(words) if words else 0


def avg_word_length(text):
    words = word_tokenize(text)
    total_characters = sum(len(word) for word in words)
    # Prevent division by zero
    return total_characters / len(words) if words else 0


# Load URLs from Input.xlsx
input_data = pd.read_excel("Input.xlsx")
urls = input_data["URL"].tolist()

# Load stop words
for file in os.listdir(os.path.join(os.path.dirname("StopWords/"))):
    filename = f"./StopWords/{file}"
    with open(filename, "r") as stop_words_file:
        stop_words = stop_words_file.read().splitlines()


# Load positive and negative dictionaries
with open("MasterDictionary/positive-words.txt", "r") as positive_file:
    positive_dict = positive_file.read().splitlines()

with open("MasterDictionary/negative-words.txt", "r") as negative_file:
    negative_dict = negative_file.read().splitlines()

# Initialize the output DataFrame
output_data = pd.DataFrame(columns=["URL_ID","URLs","POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE",
                                    "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
                                    "FOG INDEX", "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABLE PER WORD",
                                    "PERSONAL PRONOUNS", "AVG WORD LENGTH"])

# Extract and analyze data for each URL
for index, url in enumerate(urls):
    url_id = input_data.loc[index, "URL_ID"]

    # Read article text from the corresponding file
    try:
        with open(f"data/{url_id}.txt", "r", encoding="utf-8") as file:
            article_text = file.read()
    except FileNotFoundError:
        print(f"File for URL ID {url_id} not found. Skipping.")
        continue

    # Clean text
    cleaned_text = clean_text(article_text, stop_words)

    # Analyze sentiment
    sentiment_results = analyze_sentiment(
        cleaned_text, positive_dict, negative_dict)

    # Analyze readability
    readability_results = analyze_readability(cleaned_text)

    # Calculate syllable per word
    syllable_per_word = avg_syllables_per_word(cleaned_text)

    # Count personal pronouns
    personal_pronouns_count = extract_personal_pronouns(article_text)

    # Calculate average word length
    avg_word_length_result = avg_word_length(cleaned_text)

    # Create a new DataFrame for the results
    new_data = pd.DataFrame({
        "URL_ID": [url_id],
        "URLs": [url],
        "POSITIVE SCORE": [sentiment_results[0]],
        "NEGATIVE SCORE": [sentiment_results[1]],
        "POLARITY SCORE": [sentiment_results[2]],
        "SUBJECTIVITY SCORE": [sentiment_results[3]],
        "AVG SENTENCE LENGTH": [readability_results[0]],
        "PERCENTAGE OF COMPLEX WORDS": [readability_results[1]],
        "FOG INDEX": [readability_results[2]],
        "COMPLEX WORD COUNT": [readability_results[3]],
        "WORD COUNT": [readability_results[4]],
        "SYLLABLE PER WORD": [syllable_per_word],
        "PERSONAL PRONOUNS": [personal_pronouns_count],
        "AVG WORD LENGTH": [avg_word_length_result]
    })

    # Append the new data to output_data
    output_data = pd.concat([output_data, new_data], ignore_index=True)

# Save the results to "Output Data Structure.xlsx"
output_data.to_excel("Output Data Structure.xlsx", index=False)
