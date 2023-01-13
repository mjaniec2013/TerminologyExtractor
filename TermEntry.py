from DataExtraction import *

class TermEntry:
    '''Class for representing terminology entry.

    Attributes
    ----------
    term_candidate : str
        Terminology candidate
    definition : list
        Terminology candidate definition(s)
    context : list
        Sentence context in which terminology candidate appears

    Methods
    -------
    get_term_candidate(self):
        Retrieves terminology candidate
    set_term_candidate(self, term):
        Sets terminology candidate
    get_definition(self):
        Retrieves definition list
    set_definition(self, def_list):
        Sets definition list
    get_context(self):
        Retrieves context sentences
    set_context(self, contxt_list):
        Sets context sentences
    '''

    def __init__(self, term_candidate, definition, context):
        '''Construct attributes for terminology entry object.

        Parameters
        ----------
        term_candidate : str
            Terminology candidate
        definition : list
            Terminology candidate definition
        context : list
            Sentence context in which terminology candidate appears

        Returns
        -------
        None
        '''
        self.term_candidate = term_candidate
        self.definition = definition
        self.context = context


    def get_term_candidate(self):
        '''Retrieves terminology candidate.

        Returns
        -------
        term_candidate : str
            Terminology candidate
        '''
        return self.term_candidate


    def set_term_candidate(self, term):
        '''Sets terminology candidate.

        Parameters
        ----------
        term : str
            Terminology candidate

        Returns
        -------
        None
        '''
        self.term_candidate = term


    def get_definition(self):
        '''Retrieves terminology candidate definition(s).

        Returns
        -------
        definition : list
            Terminology candidate definition(s)
        '''
        return self.definition


    def set_definition(self, def_list):
        '''Sets terminology candidate definition.

        Parameters
        ----------
        def_list : list
            List of terminology candidate definitions

        Returns
        -------
        None
        '''
        self.definition = def_list


    def get_context(self):
        '''Retrieves sentences in which terminology candidate appears.

        Returns
        -------
        context : list
            Sentences in which terminology candidate appears
        '''
        return self.context


    def set_context(self, contxt_list):
        '''Sets context sentences.

        Parameters
        ----------
        contxt_list : list
            List of context sentences

        Returns
        -------
        None
        '''
        self.context = contxt_list


def create_entry(file):
    '''Takes in .PDF file. It opens it, reads it and converts it to plain text. It pre-processes the text,
    extracts terminology candidates, their definition(s) and context sentences.

    Parameters
    ----------
    file : .PDF file
    
    Returns
    -------
    entries : list
        List of TermEntry objects
    '''
    # Text pre-processing
    txt = pdf_to_text(file)
    plain_text = remove_division(txt)
    all_sents = get_sentences(plain_text)
    cleaned_s = sents_for_pos(all_sents)
    tagged = pos_tagging(cleaned_s)
    chunks = chunking(tagged)
    
    # Extracts terminology candidates
    term_candidates = get_chunks(chunks)

    entries = []
    for candidate in term_candidates:
        # Extracts context and definition(s) for terminology candidate
        contxt = extract_context(candidate, all_sents)
        definitions = extract_def(candidate, contxt)
        # Instantiates class for terminology candidate with definition(s)
        if len(definitions) > 0:
            term_entry = TermEntry(candidate, [], [])
            term_entry.set_definition(definitions)
            term_entry.set_context(contxt)
            entries.append(term_entry)
    
    return entries

