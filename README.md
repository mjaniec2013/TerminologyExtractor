# Automatic Extraction and Representation of Scientific Terminology
Final project for *Introduction to Computer Programming with Python* class (year 2022/23).

## Table of Contents

- [Introduction](#Introduction)
- [Aim and Scope of the Project](#Aim-and-Scope-of-the-Project)
- [Overview of Implementation Steps](#Overview-of-Implementation-Steps)
- [Step 1: Text Pre-Processing](#Step-1-Text-Pre-Processing)
- [Step 2: Data extraction for a terminological entry](#Step-2-Data-extraction-for-a-terminological-entry)
- [Step 3: Visual representation](#Step-3-Visual-representation)

## Introduction

**Terminology** has been defined by Ogden & Richards (1923) as the *"entirety of concepts, terms, and definitions in a particular scientific 
domain, as well as their systematic organization"*. For it to be relevant for a scientific domain, a **term** must be a linguistic symbol 
displaying the characteristics of *low ambiguity* and *high specificity*.  
  
Extracting terminology from a domain-specific corpus provides enhancement and organization of existing knowledge, and acquisition of new data; 
the purpose of this project is to provide a tool for terminology extraction adapted for English-language scientific papers.   

## Aim and Scope

The aim of the project is to enable fast and clear representation of terminology used in a scientific paper, and to 
facilitate terminology extraction for the creation of databanks.

Terminology extraction can be approached with different metholodogies, mainly: manual research of terms, statistical approaches, 
linguistic approach and hybrid approaches between statistical and linguistic methods. This tool will rely on **linguistic methods**. 
It extracts data:
* from an unstructured text (in this case, a scientific article);
* of different categories for a terminology entry template.
Entries are represented using data visualization and/or a GUI to allow editing of extracted data.

## Overview of Implementation Steps

Inspired by SketchEngine's [OneClickTerms](https://terms.sketchengine.eu/how-does-it-work), the codebase is organized around the following steps:  
1. Text pre-processing 
2. Data extraction for a terminological entry
3. Visual representation

## Step 1: Text Pre-Processing

It includes:
* Lowercasing;
* Stop-words removal;
* Phrase chunking; 
* Lemmatization; 
* POS tagging (to detect the relevant lexical structures in the text and treat them as term candidate).

## Step 2: Data extraction for a terminological entry

**Term format** is implemented as an English NP through *term grammars*, which are language-specific definitions of lexical structures allowed 
for terms in a given language. Leveraging on the list provided by the term grammars, term candidates are extracted through ("is_a" pattern?).
Terms candidates are then checked for the following categories:
* synonyms;
* example of context in which the term can appear;
* definition of term candidate;
* collocations.

## Step 3: Visual representation

The final output contains a list of terms appearing in the chosen paper. (GUI?)
