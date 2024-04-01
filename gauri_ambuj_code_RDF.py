# -*- coding: utf-8 -*-
"""Gauri_Ambuj_Code.ipynb

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
nltk.download('averaged_perceptron_tagger')

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

"""## 1st Solutions"""

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
df['Processed'] = df['cleaned_lemmatized_description'].apply(preprocess_and_tokenize)

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

"""## 2 Solution - Custom Stopwords"""

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from collections import defaultdict

# Assuming data is loaded into a DataFrame `data`
data = pd.read_csv("/content/Final_pd.csv")

# Custom stopwords
custom_stopwords = {'dedicated', 'life', 'passion', 'interest'}  # Extend as needed
stop_words = set(stopwords.words('english')).union(custom_stopwords)

# Function to tokenize, remove custom stopwords and verbs
def tokenize_and_filter(text):
    tokens = word_tokenize(text.lower())  # Tokenize and lower case
    filtered_tokens = [word for word in tokens if word not in stop_words]  # Remove custom stopwords
    # POS tagging and filter out verbs (keep nouns, NN; you might also keep adjectives, JJ)
    tagged = pos_tag(filtered_tokens)
    nouns_adjectives = [word for word, tag in tagged if tag.startswith('NN') or tag.startswith('JJ')]
    return ' '.join(nouns_adjectives)

# Apply the function to the descriptions
data['filtered_description'] = data['Description'].apply(tokenize_and_filter)

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit TF-IDF on the filtered descriptions
tfidf_matrix = tfidf_vectorizer.fit_transform(data['filtered_description'])

# Extract feature names to map back to words
features = tfidf_vectorizer.get_feature_names_out()

### Step 3: Extracting Top 7 Tags

def get_top_n_tags(row_data, features, n=7):
    # Get indices sorted by value in descending order
    sorted_indices = row_data.argsort()[-n:][::-1]
    return [features[i] for i in sorted_indices]

# Extract top 7 tags for each row
data['Top_7_Tags'] = [get_top_n_tags(row, features) for row in tfidf_matrix.toarray()]

### Step 4: Map Names to Tags and Count

name_to_top_tags = pd.Series(data['Top_7_Tags'].values, index=data['Name']).to_dict()

print(name_to_top_tags)

tag_to_names = defaultdict(lambda: defaultdict(int))

# Populate tag_to_names
for name, tags in name_to_top_tags.items():
    for tag in tags:
        tag_to_names[tag][name] += 1

# Consolidate counts and print
for tag, names in tag_to_names.items():
    count = sum(names.values())  # Total count for the tag
    names_str = ', '.join([f"{name} {names[name]}" for name in names])
    print(f"{tag.capitalize()} - {names_str}; Total: {count}")


output_file_path = "/content/Final_pd_with_top_tagged.csv"
data.to_csv(output_file_path, index=False)

"""## 3 Solutions - implemented tf-id vectorisations

"""

import pandas as pd
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

# Load data
data = pd.read_csv("/content/Final_pd.csv")

# Function to preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    # Filter out stopwords, verbs, and adjectives
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english') and pos_tag([word])[0][1] not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ']]
    return ' '.join(filtered_tokens)

# Preprocess descriptions
data['processed_description'] = data['Description'].apply(preprocess_text)

# TF-IDF vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['processed_description'])
features = tfidf_vectorizer.get_feature_names_out()

# Function to extract top 7 tags
def extract_top_tags(row_data, features, n=7):
    sorted_indices = row_data.argsort()[-n:][::-1]
    return [features[i] for i in sorted_indices]

# Extract top tags for each row
data['top_tags'] = [extract_top_tags(row, features) for row in tfidf_matrix.toarray()]

# Update CSV with tags and ranks
for i, tags in enumerate(data['top_tags']):
    for j, tag in enumerate(tags):
        data.at[i, f"Tag{j+1}"] = tag

# Map names to tags
name_to_tags = defaultdict(list)
for idx, row in data.iterrows():
    name = row['Name']
    tags = row['top_tags']
    for tag in tags:
        name_to_tags[name].append(tag)

# Count occurrences of each tag across all names
tag_to_names = defaultdict(lambda: defaultdict(int))
for name, tags in name_to_tags.items():
    for tag in tags:
        tag_to_names[tag][name] += 1

# Print tag occurrences and associated names
for tag, names in tag_to_names.items():
    count = sum(names.values())
    names_str = ', '.join([f"{name} - {count}" for name, count in names.items()])
    print(f"{tag.capitalize()} - {names_str}; Total: {count}")

# Function to search for tags and update the dictionary
def search_tags(tag):
    tag_dict = defaultdict(list)
    for name, tags in name_to_tags.items():
        if tag in tags:
            tag_dict[tag].append(name)
    return tag_dict

# Example: Search for a tag
tag_to_search = "Physics"
search_result = search_tags(tag_to_search)
print(f"Search Result for Tag '{tag_to_search}': {search_result}")

# Save updated CSV
data.to_csv("/content/updated_csv_file.csv", index=False)

"""## 4th Solutions - Implementaed Spacy with tf-id

"""

import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the CSV file into a pandas DataFrame
file_path = "/content/Final_pd.csv"
data = pd.read_csv(file_path)

# Function to preprocess text and extract features using TF-IDF
def preprocess_and_extract_features(text):
    # Tokenize text and filter out stopwords and irrelevant words
    tokens = [token.text for token in nlp(text) if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Preprocess descriptions and extract features using TF-IDF
data['processed_description'] = data['Description'].apply(preprocess_and_extract_features)
tfidf_vectorizer = TfidfVectorizer(max_features=10000)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['processed_description'])

# Get feature names
feature_names = tfidf_vectorizer.get_feature_names_out()

# Map names to their top 7 tags with weights
name_to_top_tags = defaultdict(lambda: defaultdict(float))
for i, row in data.iterrows():
    doc_weights = tfidf_matrix[i].toarray()[0]
    top_indices = doc_weights.argsort()[-7:][::-1]
    for idx in top_indices:
        name_to_top_tags[row['Name']][feature_names[idx]] = doc_weights[idx]

# Map tags to names and count occurrences
tag_to_names = defaultdict(lambda: defaultdict(int))
for name, tags in name_to_top_tags.items():
    for tag, weight in tags.items():
        tag_to_names[tag][name] += 1

# Update the DataFrame with top tags and weights
top_tags = []
tag_weights = []
for index, row in data.iterrows():
    tags = list(name_to_top_tags[row['Name']].keys())
    weights = list(name_to_top_tags[row['Name']].values())
    if len(tags) < 7:
        tags += [''] * (7 - len(tags))  # Fill missing tags with empty strings
        weights += [0.0] * (7 - len(weights))  # Fill missing weights with zeros
    top_tags.append(tags)
    tag_weights.append(weights)

data['Top_7_Tags'] = top_tags
data['Tag_Weights'] = tag_weights

# Save the updated DataFrame to a new CSV file
new_file_path = "/content/New_Final_pd1.csv"
data.to_csv(new_file_path, index=False)

# Print tag-to-names mapping with occurrences
for tag, names in tag_to_names.items():
    count = sum(names.values())
    print(f"{tag.capitalize()} - {names} - Total: {count}")

"""## 5. COMBINING TWO APPROACHES




"""

import pandas as pd
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string
import nltk
from collections import defaultdict

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load your dataset
df = pd.read_csv("/content/Final_pd.csv")

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_and_tokenize(text):
    # Tokenize text using spaCy
    doc = nlp(text)
    # Filter out stopwords, punctuation, and lemmatize tokens
    tokens = [token.lemma_ for token in doc if token.text.lower() not in stop_words and token.text not in string.punctuation]
    return tokens

# Apply preprocessing
df['Processed'] = df['cleaned_lemmatized_description'].apply(preprocess_and_tokenize)

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

# Select top 7 tags for each description
df['Top_7_Tags'] = df['Ranked_Terms'].apply(lambda x: select_top_n_tags(x, 7))

# Map names to their top 7 tags
name_to_top_tags = pd.Series(df['Top_7_Tags'].values, index=df['Name']).to_dict()

# Initialize defaultdict to store counts and names for each tag
tag_to_overall_count_and_names = defaultdict(lambda: {"count": 0, "names": defaultdict(int)})

# Update counts and names for each tag
for name, tags in name_to_top_tags.items():
    for tag in tags:
        # Increase the overall count for the tag
        tag_to_overall_count_and_names[tag]["count"] += 1
        # Increase the count for this tag under this specific name
        tag_to_overall_count_and_names[tag]["names"][name] += 1

# Add tag counts and names to DataFrame
df['Tag_Counts'] = df['Top_7_Tags'].apply(lambda tags: {tag: tag_to_overall_count_and_names[tag]["count"] for tag in tags})
df['Tag_Names'] = df['Top_7_Tags'].apply(lambda tags: {tag: ", ".join([f"{name} - {count}" for name, count in tag_to_overall_count_and_names[tag]["names"].items()]) for tag in tags})

for tag, info in tag_to_overall_count_and_names.items():
    names_counts = ', '.join([f"{name} - {count}" for name, count in info["names"].items()])
    print(f"{tag.capitalize()} - {names_counts}; Total - {info['count']}")

# Save DataFrame to a new CSV file
new_file_path = "/content/New_Final_pd_with_tags.csv"
df.to_csv(new_file_path, index=False)

"""##RDF Method 1 -> convert RDF to csv and use it"""

!pip install rdfpandas

!pip install pandas

!pip install rdflib

import rdflib

# Read the RDF data from a file
graph = rdflib.Graph()
graph.parse("/content/school.rdf")

# Convert the RDF data to a CSV file
with open("my_csv_file.csv", "w") as f:
    for subject, predicate, object in graph:
        f.write(f"{subject},{predicate},{object}\n")

"""## Directly Process the RDF Dataset"""

import rdflib
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

# Load RDF data
g = rdflib.Graph()
g.parse("/content/school.rdf", format="application/rdf+xml")

# Namespace definition may vary based on your RDF/XML structure
NS = rdflib.Namespace("http://www.semanticweb.org/guptgau03/ontologies/2024/2/school/")

# SPARQL query to fetch names and descriptions
query = """
PREFIX school: <http://www.semanticweb.org/guptgau03/ontologies/2024/2/school/>
SELECT ?name ?description
WHERE {
    ?s a ?type .
    ?s rdfs:label ?name .
    ?s school:description ?description .
}
"""

results = g.query(query)

# Process query results
data = [{'Name': str(row.name), 'Description': str(row.description)} for row in results]
df = pd.DataFrame(data)

df.head(10)

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_and_tokenize(text):
    # Convert to lowercase, remove punctuation, tokenize, remove stop words, and lemmatize
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return tokens

# Apply preprocessing and other processing steps as before
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

import pandas as pd
from collections import Counter, defaultdict
import rdflib
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Assuming you have loaded your RDF data into the graph 'g'
g = rdflib.Graph()
g.parse("/content/gauri.xml", format="xml")

# Adjusting the SPARQL query
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX school: <http://www.semanticweb.org/guptgau03/ontologies/2024/2/school/>

SELECT ?name ?description
WHERE {
    ?s rdf:type ?type .
    ?s rdfs:label ?name .
    OPTIONAL { ?s school:description ?description . }
}
"""

results = g.query(query)

# Prepare the data
data = [{'Name': str(row.name), 'Description': str(row.description) if row.description else ''} for row in results]
df = pd.DataFrame(data)

# Print the DataFrame to verify the data is loaded correctly
print(df.head())

def preprocess_and_tokenize(text):
    # Convert to lowercase, remove punctuation, tokenize, remove stop words, and lemmatize
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return tokens

# Apply preprocessing and other processing steps as before
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

# Select top 7 tags for each description
df['Top_7_Tags'] = df['Ranked_Terms'].apply(lambda x: select_top_n_tags(x, 7))

# Map names to their top 7 tags
name_to_top_tags = pd.Series(df['Top_7_Tags'].values, index=df['Name']).to_dict()

# Initialize defaultdict to store counts and names for each tag
tag_to_overall_count_and_names = defaultdict(lambda: {"count": 0, "names": defaultdict(int)})

# Update counts and names for each tag
for name, tags in name_to_top_tags.items():
    for tag in tags:
        # Increase the overall count for the tag
        tag_to_overall_count_and_names[tag]["count"] += 1
        # Increase the count for this tag under this specific name
        tag_to_overall_count_and_names[tag]["names"][name] += 1

# Print results
for tag, info in tag_to_overall_count_and_names.items():
    names_counts = ', '.join([f"{name} - {count}" for name, count in info["names"].items()])
    print(f"{tag.capitalize()} - {names_counts}; Total - {info['count']}")

import pandas as pd
from collections import Counter, defaultdict
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import rdflib

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load RDF data from XML file
g = rdflib.Graph()
g.parse("/content/gauri1.rdf", format="xml")

# Adjusting the SPARQL query
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX school: <http://www.semanticweb.org/guptgau03/ontologies/2024/2/school/>

SELECT ?name ?description
WHERE {
    ?s rdf:type ?type .
    ?s school:name ?name .
    OPTIONAL { ?s school:description ?description . }
}
"""

results = g.query(query)

# Prepare the data
data = [{'Name': str(row.name), 'Description': str(row.description) if row.description else ''} for row in results]
df = pd.DataFrame(data)

# Print the DataFrame to verify the data is loaded correctly
print(df.head(10))

def preprocess_and_tokenize(text):
    # Convert to lowercase, remove punctuation, tokenize, remove stop words, and lemmatize
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return tokens

# Apply preprocessing and other processing steps as before
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

# Select top 7 tags for each description
df['Top_7_Tags'] = df['Ranked_Terms'].apply(lambda x: select_top_n_tags(x, 7))

# Map names to their top 7 tags
name_to_top_tags = pd.Series(df['Top_7_Tags'].values, index=df['Name']).to_dict()

# Initialize defaultdict to store counts and names for each tag
tag_to_overall_count_and_names = defaultdict(lambda: {"count": 0, "names": defaultdict(int)})

# Update counts and names for each tag
for name, tags in name_to_top_tags.items():
    for tag in tags:
        # Increase the overall count for the tag
        tag_to_overall_count_and_names[tag]["count"] += 1
        # Increase the count for this tag under this specific name
        tag_to_overall_count_and_names[tag]["names"][name] += 1

# Print results
for tag, info in tag_to_overall_count_and_names.items():
    names_counts = ', '.join([f"{name} - {count}" for name, count in info["names"].items()])
    print(f"{tag.capitalize()} - {names_counts}; Total - {info['count']}")

