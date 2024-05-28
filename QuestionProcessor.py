import os
import sys
import subprocess
import pkg_resources

def install(package):
    try:
        pkg_resources.get_distribution(package)
        print(f"{package} is already installed.")
    except pkg_resources.DistributionNotFound:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Installed {package}.")
        except Exception as e:
            print(f"Failed to install {package}. Error: {str(e)}")

# Install necessary packages
packages = ['nltk', 'textblob', 'spacy']
for package in packages:
    install(package)

# Import installed packages
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob
import spacy

# Ensure NLTK resources are downloaded with error handling
def download_nltk_resource(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource)

download_nltk_resource('wordnet')
download_nltk_resource('averaged_perceptron_tagger')
download_nltk_resource('punkt')

# Ensure spaCy model is downloaded and load it
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Define your responses
responses = {
    'name': 'your name',
    'location': 'your location',
    'age': 'your age',
    'occupation': 'your job',
    'height': 'your height',
    'physical activity': 'your level of physical actvities',
    'educational level': 'your educational level',
    'drinking habit': 'your drinking frequency',
    'smoking habit': 'your smoking frequency',
    'gender identity': 'your gender',
    'seeking': 'what you seek from your partner',
    'want children': 'if you want children or not',
    'star sign': 'your horoscope sign',
    'politics': 'how political are you',
    'religion': 'your religion or lack of',
    'tribe': 'your tribe if you have one',
    'hobbies': 'your hobbies',
    'passion': 'your passion',
    'dreams': 'what you dream of doing or being',
    'expectations in a relationship': 'what you expect in a relationship',
    'favorite food': 'best food',
    'favorite color': 'best color',
    'favorite animal': 'best animal',
    'favorite movie': 'best movie',
    'favorite book': 'best book',
    'favorite music genre': 'best music type',
    'favorite artist': 'best musician ',
    'favorite travel destination': 'best place to travel',
    'favorite sport': 'best sport',
    'favorite team': 'best team',
    'favorite player': 'best player',
    'favorite subject in school': 'best subject',
    'favorite type of music': 'best music type',
    'favorite type of food': 'best food type',
    'favorite type of movie': 'best movie type',
    'favorite type of book': 'best book type',
    'favorite type of sport': 'best sport type',
    'favorite type of travel': 'best travel type',
    'do you prefer being the one to start chats the most or your man?': 'no',
}



# Convert the keys in the responses dictionary to lowercase
responses = {key.lower(): value for key, value in responses.items()}

# Function to translate Penn Treebank tags to WordNet tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# Function to lemmatize verbs to their related noun if possible
def verb_to_noun(verb):
    synsets = wordnet.synsets(verb, pos=wordnet.VERB)
    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.derivationally_related_forms():
                for related_lemma in lemma.derivationally_related_forms():
                    if related_lemma.synset().pos() == 'n':
                        return related_lemma.name()
            elif lemma.name().endswith('d'):
                return lemma.name()[:-1]
            elif lemma.name().endswith('ed'):
                return lemma.name()[:-2]
    return verb

while True:
    question = input("Ask me anything: ")

    # Correct the question using TextBlob
    blob = TextBlob(question)
    corrected_question = str(blob.correct())

    # Convert the corrected question to lowercase and split it into words
    keywords = corrected_question.lower().split()

    # List to store matching responses
    matching_responses = []

    # Tokenize and process the corrected question
    tokens = nltk.word_tokenize(corrected_question)
    pos_tags = nltk.pos_tag(tokens)

    for token, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos)
        if wordnet_pos:
            lemma = nltk.WordNetLemmatizer().lemmatize(token, pos=wordnet_pos)
        else:
            lemma = token

        if wordnet_pos == wordnet.VERB:
            noun_form = verb_to_noun(lemma)
            if noun_form in responses:
                matching_responses.append(responses[noun_form])
        elif lemma in responses:
            matching_responses.append(responses[lemma])

    # Prefix matching for additional flexibility
    for keyword in keywords:
        keyword_prefix = keyword[:3]
        for response_key in responses:
            if response_key.startswith(keyword_prefix):
                matching_responses.append(responses[response_key])
                break

    # Process the corrected question with spaCy
    doc = nlp(corrected_question)
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in responses:
            matching_responses.append(responses[lemma])

    # Print all unique responses
    unique_responses = set(matching_responses)
    for response in unique_responses:
        print(response)
    if not unique_responses:
        print("I don't have an answer for that.")

