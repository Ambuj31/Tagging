# -*- coding: utf-8 -*-
"""Code2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Scvan9awY_AAX-PV-DuTJK6KJY8QV0Z
"""

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import string
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import WordNetLemmatizer

import numpy as np
import re
import nltk
import spacy
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
# Load the CSV file
df = pd.read_csv('/content/Tag_dataset_tags.csv')

# Data Cleaning
df.dropna(subset=['Description'], inplace=True)  # Drop rows with missing descriptions
df.drop_duplicates(subset=['Description'], keep='first', inplace=True)  # Remove duplicates

# Text Preprocessing with Lemmatization and Stopword Removal
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def lemmatize_text(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(lemmatized_tokens)

df['lemmatized_description'] = df['Description'].apply(lemmatize_text)

# Remove Stopwords from Lemmatized Text
def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    return ' '.join(filtered_tokens)

df['cleaned_lemmatized_description'] = df['lemmatized_description'].apply(remove_stopwords)

# Create Array of Words from Cleaned Lemmatized Description
def create_word_array(text):
    return word_tokenize(text)

df['word_array'] = df['cleaned_lemmatized_description'].apply(create_word_array)

# Perform POS Tagging on Each Word in Each Array
def pos_tag_words(word_array):
    return pos_tag(word_array)

df['pos_tagged_words'] = df['word_array'].apply(pos_tag_words)

# Create Separate Columns for Specific POS Tags
def extract_pos_tags(tagged_words, pos_tag):
    return ' '.join([word for word, tag in tagged_words if tag == pos_tag])

df['Nouns'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'NN') + ' ' + extract_pos_tags(x, 'NNS') + ' ' + extract_pos_tags(x, 'NNP') + ' ' + extract_pos_tags(x, 'NNPS'))
df['Verbs'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'VB') + ' ' + extract_pos_tags(x, 'VBD') + ' ' + extract_pos_tags(x, 'VBG') + ' ' + extract_pos_tags(x, 'VBN') + ' ' + extract_pos_tags(x, 'VBP') + ' ' + extract_pos_tags(x, 'VBZ'))
df['Adjectives'] = df['pos_tagged_words'].apply(lambda x: extract_pos_tags(x, 'JJ'))
# Save the preprocessed data with specific POS tagged words to a new CSV file
df.to_csv('Final_pd.csv', index=False)

import tensorflow as tf
from tensorflow import keras

df.head()

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Read the CSV file into a pandas DataFrame
file_path = "/content/Final_pd.csv"
data = pd.read_csv(file_path)

# Function to extract tags from description
def extract_tags(description):
    # Tokenize the description
    tokens = word_tokenize(description)
    # Perform Part-of-Speech tagging
    tagged_words = pos_tag(tokens)
    # Define your logic to extract tags, for simplicity, let's assume the first noun encountered is the tag
    tags = [word for word, tag in tagged_words if tag.startswith('N')]
    return tags

# Apply the function to each row to generate tags
data['Tags'] = data['Description'].apply(extract_tags)

# Save the updated DataFrame to a new CSV file if needed
output_file_path = "/content/Final_pd_with_tags.csv"
data.to_csv(output_file_path, index=False)

# Display the updated DataFrame
print(data)

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Read the CSV file into a pandas DataFrame
file_path = "/content/Final_pd.csv"
data = pd.read_csv(file_path)

# Function to extract tags from description
def extract_tags(description):
    # Tokenize the description
    tokens = word_tokenize(description)
    # Perform Part-of-Speech tagging
    tagged_words = pos_tag(tokens)
    # Define your logic to extract tags, for simplicity, let's assume the first noun encountered is the tag
    tags = [word for word, tag in tagged_words if tag.startswith('N')]
    return tags

# Create a dictionary to map names to tags
name_tag_dict = {}

# Iterate over each row to generate tags and map them to names
for index, row in data.iterrows():
    name = row['Name']
    description = row['Description']
    tags = extract_tags(description)
    name_tag_dict[name] = tags

# Display the dictionary
print(name_tag_dict)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sklearn.pipeline import Pipeline

# Read the CSV file into a pandas DataFrame
file_path = "/content/Final_pd.csv"
data = pd.read_csv(file_path)

# Function to extract tags from description
def extract_tags(description):
    # Tokenize the description
    tokens = word_tokenize(description)
    # Perform Part-of-Speech tagging
    tagged_words = pos_tag(tokens)
    # Define your logic to extract tags, for simplicity, let's assume the first noun encountered is the tag
    tags = [word for word, tag in tagged_words if tag.startswith('N')]
    return ' '.join(tags)

# Preprocess data
data['tags'] = data['Description'].apply(extract_tags)

# Split data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data['Description'], data['tags'], test_size=0.2, random_state=42)

# Create a pipeline with CountVectorizer and Multinomial Naive Bayes
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('clf', MultinomialNB())])

# Train the model
text_clf.fit(X_train, y_train)

# Test the model
predicted = text_clf.predict(X_test)

# Print accuracy
print("Accuracy:", text_clf.score(X_test, y_test))

# Example usage: Predict tags for a given phrase
def predict_tags(phrase):
    predicted_tags = text_clf.predict([phrase])
    return predicted_tags

# Example usage
phrase = "Student is very much interested in Mathematics and Physics"
predicted_tags = predict_tags(phrase)
print("Predicted tags for the phrase:", predicted_tags)

"""NEW APPROACH"""

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string
nltk.download('stopwords')
nltk.download('wordnet')
# Assuming 'Description' is a column in your DataFrame
# Load your dataset
df = pd.read_csv("/content/Final_pd.csv")

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_and_tokenize(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    words = word_tokenize(text)
    # Remove stop words and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return tokens

# Apply preprocessing
df['Processed'] = df['Description'].apply(preprocess_and_tokenize)

def score_terms(tokens):
    # Count term frequencies
    term_freq = Counter(tokens)
    # Sort terms by frequency
    sorted_terms = dict(sorted(term_freq.items(), key=lambda item: item[1], reverse=True))
    return sorted_terms

# Score and rank terms in descriptions
df['Ranked_Terms'] = df['Processed'].apply(score_terms)

def select_top_n_tags(ranked_terms, n=7):
    # Select the top N terms
    return list(ranked_terms.keys())[:n]

df['Top_7_Tags'] = df['Ranked_Terms'].apply(lambda x: select_top_n_tags(x, 7))
df.head()

# Map names to their top 5 tags
name_to_top_tags = pd.Series(df['Top_7_Tags'].values, index=df['Name']).to_dict()

print(name_to_top_tags)

from collections import defaultdict

# This defaultdict will store counts and names for each tag
tag_to_overall_count_and_names = defaultdict(lambda: {"count": 0, "names": defaultdict(int)})

for name, tags in name_to_top_tags.items():
    for tag in tags:
        # Increase the overall count for the tag
        tag_to_overall_count_and_names[tag]["count"] += 1
        # Increase the count for this tag under this specific name
        tag_to_overall_count_and_names[tag]["names"][name] += 1

# Now, printing results as per your format:
for tag, info in tag_to_overall_count_and_names.items():
    names_counts = ', '.join([f"{name} - {count}" for name, count in info["names"].items()])
    print(f"{tag.capitalize()} - {names_counts}; Total - {info['count']}")

