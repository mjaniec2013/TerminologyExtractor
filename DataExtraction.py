'''Data Extraction Module

This module contains three functions needed for extracting data for terminology entry, such as 
terminology candidates, sentences in which they appear and possible definitions. It requires 
importing functions from text pre-processing module.

Functions
---------
get_chunks(chunked)
    Takes in a list of parse trees, returns a list of term candidates
extract_context(term_cand, sent_list)
    Takes in a terminology candidate and sentence list, returns context sentences
extract_def(term_cand, context)
    Takes in a terminology candidate and context sentences, returns definitions for terminology candidate
'''

from TextPreProcessing import *


def get_chunks(chunked):
    '''Takes in list of parse trees as input. The first list comprehension extracts NPs from parse trees, 
    the second one filters out terms shorter than two characters and those already present in all_terms list. 
    Returns list with filtered out terms.

    Parameters
    ----------
    chunked : list
        List of parse tree for terminology candidate extraction

    Returns
    -------
    all_terms : list
        List of terminology candidates
    '''
    all_chunks = []
    for tree in chunked:
        chunks = []
        # Iterate through subtrees to get individual chunks
        raw_chunks = [subtree.leaves() for subtree in tree.subtrees() if subtree.label() == 'NP']
        # Remove POS tags, keep words
        for raw_chunk in raw_chunks:
            chunk = [word_tag[0] for word_tag in raw_chunk]
            chunks.append(' '.join(chunk))
        if len(chunks) > 0:
            all_chunks.append(chunks)

    term_list = []
    # Remove sublists in all_chunks list, returns a list with chunks
    for sublist in all_chunks:
        term_list.extend(sublist)

    all_terms = []
    # Remove all one-character terminology candidates
    for t in term_list:
        if len(t) > 1 and t not in all_terms:
            all_terms.append(t)

    return all_terms


def extract_context(term_cand, sent_list):
    '''Takes in term candidate and list of sentences as inputs, returns all sentences in which
    the term candidate is mentioned.

    Parameters
    ----------
    term_cand : str
        Terminology candidate
    sent_list : list
        List of sentences to be checked for candidate and context

    Returns
    -------
    context : list
        List of sentences in which terminology candidate appears
    '''
    context = []
    
    for s in sent_list:
        # Checks presence of terminology candidate in the sentence regardless of case 
        if term_cand in s.casefold() and s not in context:
            # Checks if term in string is a separate word 
            true_term = re.findall(r'\b' + term_cand + r'\b', s.casefold())
            if term_cand not in true_term:
                continue
            else:
                first_letter = re.search(r'[A-Z0-9]', s)
                # Filters out sentences consisting only of terminology candidate and non-words
                if first_letter is not None:
                    context.append(s[s.index(first_letter.group()):])

    return context


def extract_def(term_cand, context):
    '''Takes in terminology candidate and list of sentences in which the candidate appears, 
    parses over it and finds definitions corresponding to defined patterns. 
    Returns list of possible definitions for terminology candidates.

    Parameters
    ----------
    term_cand : string
        Terminology candidate
    context : list
        List of sentences in which terminology candidate appears

    Returns
    -------
    definitions : list
        List of possible definitions for terminology candidate
    '''
    # Signal words and phrases preceding definition
    patterns_pre = [r'\s?—\s',
                    r'\sis\s',
                    r'\sare\s',
                    r'\,\sthat\sis\,?\s',
                    r'\,\snamely\s',
                    r'\scan\sbe\sdescribed\sas\s',
                    r'\srefers?\sto\s',
                    r'\smeans?\s',
                    r'\ssays?\sthat\s',
                    ]
    
    # Signal words and phrases following definition
    patterns_pos = [r'\,\sthat\sis\,?\s',
                    r'defines?\s',
                    r'describes?\s',
                    ]

    all_def = []
    
    # Loops over context sentences and finds all sentences corresponding to definition patterns
    for s in context:
      for pattern in patterns_pre:
          all_def.append(re.findall(term_cand + pattern + r'\b.+\Z', s, flags=re.IGNORECASE))
      for pattern in patterns_pos:
          all_def.append(re.findall(r'[A-Z0-9].+' + pattern + term_cand + r'\b.*\Z', s, flags=re.IGNORECASE))
    
    # Removes sublists in full_def list, returns a list with definitions
    full_def = []
    for d in all_def:
        full_def.extend(d)

    # Appends possible definitions to definition list after checking if they are not empty strings and are not
    # already present in the definition list
    definitions = []
    for def_cand in full_def:
        if def_cand == '':
            full_def.remove(def_cand)
        elif def_cand not in definitions:
            definitions.append(def_cand)    

    return definitions

