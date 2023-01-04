# Text Pre-Processing: Lowercasing, tokenization, POS tagging, phrase chunking, lemmatization.
# cd Documents/GitHub/CogSciTerminology
import fitz, nltk, re


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
    text = ''
    if word_division != None:
        text = re.sub(r'-\n', '', lowercase)
    else:
        text = lowercase
    # Substitute break lines with a space
    no_breakline = re.sub(r'\n', ' ', text)
    # Split the text into sentences
    sentences = re.findall(r'[^.!?]+', no_breakline)

    return sentences


def pos_tagging(sentence_list):
    '''Takes in a list of sentences, removes punctuation and returns tagged tokens.
    '''
    # Tokenize sentences into words
    tokens = []
    # Split sentences from sentence list and remove empty strings from token list
    for sentence in sentence_list:
        word_token = sentence.split(' ')
        clean_token = [t for t in word_token if t != '']
        tokens.append(clean_token)
    # POS tag tokens
    tagged = [nltk.pos_tag(token) for token in tokens if token != '']

    return tagged

def chunking(tagged_sents):
    '''
    '''

    # defines grammar for chunking noun phrases
    chunk_grammar_rules = r"""
        NP: {<DT\$>?<JJ>*<NN.*>+} # noun phrase
            {<DT\$>?<JJ>*<NN.*>*<of><JJ>*<NN.*>*}
	    """
    chunker = nltk.RegexpParser(chunk_grammar_rules)
    chunked_sents = [chunker.parse(tagged_sent) for tagged_sent in tagged_sents]

    return chunked_sents


def get_chunks(chunked):
    all_chunks = []
    # chunked sentences are in the form of nested trees
    for tree in chunked:
        chunks = []
        # iterate through subtrees / leaves to get individual chunks
        raw_chunks = [subtree.leaves() for subtree in tree.subtrees() if subtree.label() == 'NP']
        for raw_chunk in raw_chunks:
            chunk = []
            for word_tag in raw_chunk:
                # drop POS tags, keep words
                chunk.append(word_tag[0])
            chunks.append(' '.join(chunk))
        all_chunks.append(chunks)

    return all_chunks

file = 'sample1.pdf'
txt = pdf_to_text(file)
clean = clean_text(txt)
tagged = pos_tagging(clean)
chunks = chunking(tagged)
term_cand = get_chunks(chunks)
print(term_cand)
