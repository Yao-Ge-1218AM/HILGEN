# HILGEN: Hierarchically-Informed Data Generation for Biomedical NER Using Knowledgebases and LLMs

## Overview

HILGEN is a novel approach designed to improve the performance of few-shot learning (FSL) in biomedical Named Entity Recognition (NER) by leveraging domain knowledge from the Unified Medical Language System (UMLS) and the generative capabilities of Large Language Models (LLMs) such as GPT-3.5. This project aims to address the challenges of limited annotated data in medical NLP tasks by generating synthetic training examples that enrich the representation of rare medical concepts.

## Key Features

**UMLS Integration:** Uses UMLS's hierarchical structure to enhance training data with domain-specific knowledge.

**Synthetic Data Generation:** Leverages GPT-3.5 to create contextually rich examples, improving model performance in few-shot settings.

**Improved NER Performance:** Demonstrates significant improvements in recognizing biomedical entities in text, particularly with limited training data.

## Datasets

HILGEN has been tested on several biomedical datasets, including:

**1. MIMIC III:** A large database containing de-identified health-related data from critical care patients.
**2. BC5CDR:** A dataset focused on extracting relationships between chemicals and diseases.
**3. NCBI Disease:** PubMed abstracts annotated with disease names.
**4. MedMentions:** A large biomedical corpus annotated with UMLS concepts.

## Requirements

· Python 3.x   
· Hugging Face’s Transformers library  
· UMLS access (for domain knowledge integration)  

## Usage

To replicate the experiments:

**1. Install Dependencies:** Ensure Python 3.x, Hugging Face’s Transformers library, and access to UMLS are set up.
**2. Run the Scripts:** Follow the provided notebooks to generate synthetic data and train the NER models using HILGEN.
**3. Evaluate Performance:** Compare the results with baseline models to observe the improvements brought by HILGEN.

## 
