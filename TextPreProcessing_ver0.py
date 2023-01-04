# Text Pre-Processing: Lowercasing, tokenization, POS tagging, phrase chunking, lemmatization.

import fitz, nltk, re, string


def pdf_to_text(document):
    '''Takes in a .pdf document, returns it as plain text.
    '''
    # Open a .pdf file with PyMuPDF
    doc = fitz.open(document)
    text = ''
    # Loop over every page in .pdf file, get text and append it to the empty string
    for page in doc:
        text += page.get_text()
    return text


def clean_text(document):
    '''Returns lowercased text.
    '''
    lowercase = document.lower()
    # Substitute word divisions with empty string
    word_division = re.findall(r'.-\n.', lowercase)
    if word_division != None:
        lowercase = re.sub(r'-\n', '', lowercase)
    # Substitute punctuation with a space
    no_punct = re.sub(r'[^\w\s\-]|[\n\r]', ' ', lowercase)
    # Remove double spacing
    no_punct = re.sub(r'\s+', ' ', no_punct)

    return no_punct


def pos_tagging(document):
    '''Removes punctuation and returns tagged tokens.
    '''
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    # Filters out everything that is not alphabetic
    filtered = [token for token in tokens if token.isalpha()]
    # POS tagging tokens
    tagged = nltk.pos_tag(filtered)

    #    for sentence in sentences:
    #        sentence_tokens = nltk.word_tokenize(sentence)
    # Find the tagged tokens that belong to the sentence
    #        sentence_tagged_tokens = [tagged for tagged in tagged if tagged[0] in sentence_tokens]
    #    return sentence_tagged_tokens
    return tagged


#    print(sentences)

file = 'sample1.pdf'
print(clean_text(pdf_to_text(file)))


# print(pos_tagging(clean_text(pdf_to_text((file)))))

def chunking(document):
    '''
    '''

    # defines grammar for chunking noun phrases
    chunk_grammar_rules = r'''
        NP: {<DT\$>?<JJ>*<NN.*>+} # noun phrase
            {<DT\$>?<JJ>*<NN.*>*<of><JJ>*<NN.*>*}
	    '''
    chunk_parser = nltk.RegexpParser(chunk_grammar_rules)
    chunked = chunk_parser.parse(tagged)  # chunk tagged tokens
    # print(chunked)


def get_chunks(chunked, chunk_type='NP'):
    all_chunks = []
    # chunked sentences are in the form of nested trees
    for tree in chunked:
        chunks = []
        # iterate through subtrees / leaves to get individual chunks
        raw_chunks = [subtree.leaves() for subtree in tree.subtrees()
                      if subtree.node == chunk_type]
        for raw_chunk in raw_chunks:
            chunk = []
            for word_tag in raw_chunk:
                # drop POS tags, keep words
                chunk.append(word_tag[0])
            chunks.append(' '.join(chunk))
        all_chunks.append(chunks)

    return all_chunks
# print(get_chunks(chunked))