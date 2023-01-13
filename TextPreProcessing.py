'''Text Pre-Processing Module

This module takes in text from a .PDF file, elaborates it as plain text and cleans it into a consistent format
that can be used for terminology candidate class implementation. It requires PyMuPDF, NLTK and re libraries.
Pre-processing pipeline consists of: removing word divisions, line breaks and double spaces; cleaning up text; 
POS tagging; chunking.

Functions
---------
pdf_to_text(pdf)
    Takes in a .PDF file, returns content as plain text
remove_division(text)
    Takes in a string of text, returns text cleaned up from word divisions, line breaks and double spaces
get_sentences(flow_text)
    Takes in a flow of text, returns list of sentences cleaned up from URLs, DOIs, emails, non-alphanumeric characters,
    expands abbreviations
sents_for_pos(raw_sents)
    Takes in a list of sentences, returns it cleaned up from non-words, non-spaces, double spaces
pos_tagging(scraped_sents)
    Takes in a list of sentences, returns POS tagged words from sentences
chunking(tagged_sents)
    Takes in a list of POS-tagged words, returns chunked Noun Phrases
'''

import fitz, nltk, re


def pdf_to_text(pdf):
    '''Takes in a .PDF file, opens it with PyMuPDF and extracts text from it.

    Parameters
    ----------
    pdf : .PDF file
        File to be pre-processed

    Returns
    -------
    text : str
        Plain text extracted from .PDF file
    '''
    doc = fitz.open(pdf)
    text = ''
    # Loops over every page in .PDF file, gets text and appends it to empty string
    for page in doc:
        text += page.get_text()

    return text


def remove_division(text):
    '''Takes in text. It uses regular expressions to substitute word divisions with an empty string and
    line breaks with a space, then removes any double space. Returns cleaned-up text as a string.

    Parameters
    ----------
    text : str
        Plain text to be processed
    
    Returns
    -------
    clean_text : str
        Text cleaned up from word divisions, line breaks, double spaces
    '''
    # Substitutes word divisions with empty string
    no_division = re.sub(r'-\n', '', text)

    # Substitutes break lines with a space
    no_breaklines = re.sub(r'\n', ' ', no_division)

    # Removes double spacing
    clean_text = re.sub(r'\s+', ' ', no_breaklines)

    return clean_text


def get_sentences(flow_text):
    '''Takes flow of text as input. It substitutes URLs, DOIs and email addresses with a space; it maps abbreviations
    to their own expansions and replace them; it replaces every non-alphanumeric character with a space, 
    removes double spacing and splits sentences. Returns list of sentences whose length is longer than one character.

    Parameters
    ----------
    flow_text : str
        Text to be cleaned

    Returns
    -------
    sentences : list
        List of sentences cleaned up from URLs, DOIs, emails, abbreviations, non-alphanumeric characters
    '''
    # Substitutes URLs with a space
    no_url = re.sub(r'https?:\S+', ' ', flow_text, flags=re.IGNORECASE)
    
    # Substitutes DOIs with a space
    no_doi = re.sub(r'doi:\S+', ' ', no_url, flags=re.IGNORECASE)
    
    # Substitutes e-mail addresses with a space
    no_email = re.sub(r'\S+@\S+', ' ', no_doi, flags=re.IGNORECASE)
    
    # Defines dictionary with abbreviations as keys and their expansions as values
    abbreviations = {
        r'\banon\.': 'anonymous',
        r'\bca\.': 'circa',
        r'\bcf\.': 'compare to',
        r'\bdef\.\s?\:?': 'definition: ',
        r'\be\.\s?g\.': 'for example',
        r'\bed\.': 'edition',
        r'\beds\.': 'editions',
        r'\bet\sal\.': 'et alia',
        r'\betc\.' : 'et cetera',
        r'\bi\.\s?e\.\,?': 'that is,',
        r'\bibid\.': 'ibidem',
        r'\billus\.': 'illustration',
        r'\bn\.\s?b\.': 'nota bene',
        r'\bn\.\s?d\.': 'not determined',
        r'\bno\.': 'number',
        r'\bvol\.': 'volume',
        r'\bvs\.': 'versus'
    }
    no_abb = no_email
    
    # Replaces abbreviations with expansions
    for abb, exp in abbreviations.items():
        no_abb = re.sub(abb, exp, no_abb)
    
    # Substitutes all non-letters, non-digits, non-punctuation marks with a space
    only_text = re.sub(r'[^\w\s!"#$€%&\'()*+,-—./:;<=>?@[\\]^_`´°{|}~]', ' ', no_abb)
    no_signs_text = only_text.replace('�', '')

    
    # Removes double spacing
    cleaned_txt = re.sub(r'\s+', ' ', no_signs_text)
   
    # Splits the text into sentences
    split_sent = re.findall(r'[^.!?]+', cleaned_txt)

    sentences = []
    for sent in split_sent:
        # Compiles a list of sentences longer than one character
        if len(sent) > 1:
            sentences.append(sent.strip(' '))

    return sentences


def sents_for_pos(raw_sents):
    '''Takes in a list of sentences as input. It lowercases the list, replaces non-word and non-space 
    characters with a space, and substitutes double spaces with a single space. Returns list of cleaned-up sentences.

    Parameters
    ----------
    raw_sents : list
        List of sentences to be processed
    
    Returns
    -------
    clean_sent : list
        List of sentences cleaned up from non-words, non-spaces, double spaces
    '''
    clean_sent = []
    for s in raw_sents:
        # Lowercase sentences
        lowercased_s = s.lower()
        # Substitute non-words and non-spaces with space
        no_punct = re.sub(r'[^\w\s-]', ' ', lowercased_s)
        # Substitute double spaces with single space
        clean_sent.append(re.sub(r'\s+', ' ', no_punct))
        
    return clean_sent


def pos_tagging(scraped_sents):
    '''Takes in list of sentences as input. It tokenizes each sentence and removes empty strings from list of tokens, 
    then tags tokens. Returns list of tuples sublists, each of them made of a word and the corresponding POS tag.

    Parameters
    ----------
    scraped_sents : list
        List of sentences to be POS tagged

    Returns
    -------
    tagged : list
        List of lists of tuples containing POS-tagged words
    '''
    tokens = []
    # Split sentences from sentence list and remove empty strings from token list
    for sentence in scraped_sents:
        word_token = sentence.split(' ')
        clean_token = [t for t in word_token if t != '']
        tokens.append(clean_token)
    # POS tag tokens
    tagged = [nltk.pos_tag(token) for token in tokens if token != '']

    return tagged


def chunking(tagged_sents):
    '''Takes in a list of POS tagged words, defines chunk grammar and returns parse trees for sentences.

    Parameters
    ----------
    tagged_sents : list
        List of POS tagged word tokens
    Returns
    -------
    chunked_sents : list
        List of parsed sentences
    '''
    # Define grammar for chunking noun phrases
    grammar_rules = r''' 
        NP: {<DT\$>?<JJ>*<NN.*>+}  
	    '''
    chunker = nltk.RegexpParser(grammar_rules)
    chunked_sents = [chunker.parse(tagged_sent) for tagged_sent in tagged_sents if len(tagged_sent) > 0]

    return chunked_sents
