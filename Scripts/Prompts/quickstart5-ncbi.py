import os
import openai
import json
import time

openai.api_type = "azure"
openai.api_base = "https://yguo262.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "c4019382c2d447b3beccf75ce0ddf76d"

#system_message = {"role": "system", "content": "You are a medical AI trained to identify and classify tokens into three categories: Clinical Impacts, Social Impacts, and Outside ('O'), with an understanding of medical concepts from the Unified Medical Language System (UMLS). You understand medical terminology and concepts. The data you are working with has been collected from 14 forums on Reddit (subreddits) that focused on prescription and illicit opioids, and medications for opioid use disorder. This dataset represents a social media context, coming from individuals who may use prescription and illicit opioids and stimulants. In this dataset, high-frequency clinical impacts include 'withdrawal', 'rehab', 'addicted', 'detox', 'overdosed', and 'rehabs'. High-frequency social impacts include 'lost', 'homeless', 'charged', 'streets', 'jail', and 'disorderly'.  Your task is to extract and classify the clinical and social impacts from this dataset, considering your knowledge of the lifestyle of this population and the potential clinical and social impacts they might experience.  'Clinical Impacts' refer to tokens describing the effects, consequences, or impacts of substance use on individual health or well-being, as defined in UMLS. 'Social Impacts' describe the societal, interpersonal, or community-level effects, also based on UMLS definitions. Any token not falling into these categories should be labeled as 'O'. Your task is to predict and return the label for each provided token, ensuring the number of output labels matches the number of input tokens exactly. The output format should be tokens with their labels: ['I-O', 'was-O', 'a-O', 'codeine-Clinical Impacts', 'addict-Clinical Impacts', '.-O']. Please strictly follow the output format to output the results. Please be sure to output each token and its corresponding label, and link them with '-'. When classifying tokens, consider the UMLS concepts and terminology, and the specific context of this social media dataset, to enhance the accuracy of your classifications. Please use the tokens I provided, do not use other tokenization mechanism."

    #}
system_message = {"role": "system", "content": "You are a medical AI trained to identify and classify tokens into three categories: DiseaseClass, SpecificDisease, Modifier, CompositeMention and Outside ('O'). with an understanding of medical concepts from the Unified Medical Language System (UMLS). You understand medical terminology and concepts. Your task is to extract and classify the DiseaseClass, SpecificDisease, Modifier and CompositeMention from this dataset, considering your knowledge of UMLS. NCBI disease corpus, a collection of 793 PubMed abstracts fully annotated at the mention and concept level to serve as a research resource for the biomedical natural language processing community. Each PubMed abstract was manually annotated by two annotators with disease mentions and their corresponding concepts in Medical Subject Headings (MeSH) or Online Mendelian Inheritance in Man (OMIM). The public release of the NCBI disease corpus contains 6892 disease mentions, which are mapped to 790 unique disease concepts. Of these, 88 percent link to a MeSH identifier, while the rest contain an OMIM identifier. We were able to link 91 percent of the mentions to a single disease concept, while the rest are described as a combination of concepts. 'DiseaseClass' refers to a classification system or category used to group various medical conditions or diseases based on certain characteristics, such as their nature, affected biological systems, or underlying causes. 'SpecificDisease' appears to describe particular diseases that are identified and classified based on their specific clinical features, genetic origins, or biochemical abnormalities. 'Modifier' refers to specific attributes or variations or conditions that can modify or influence the presentation, progression, or characteristics of a disease, alter the manifestation or course of a disease, potentially affecting its diagnosis, treatment, and prognosis. 'CompositeMention' describe medical conditions or characteristics that are composed of several elements or features, often involving multiple tissues, organs, or systems. Any token not falling into these categories should be labeled as 'O'. Each token, is provided separately and should be classified accordingly. For example, the sentence 'Histidinemia. Classical and atypical form in siblings.' is tokenized and labeled as follows: ['Histidinemia.', 'Classical', 'and', 'atypical', 'form', 'in', 'siblings.'] with labels ['SpecificDisease', 'O', 'O', 'O', 'O', 'O', 'O']. In this dataset, high-frequency DiseaseClass include 'disorder', 'abnormalities', 'tumors', 'mental', 'disorders', 'retardation'. High-frequency SpecificDisease include 'deficiency', 'syndrome', 'dystrophy', 'familial', 'myotonic', 'colorectal'.High-frequency Modifier include 'tumor', 'tumour', 'APC', 'choroideremia', 'DM', 'DMD'. High-frequency CompositeMention include 'breast', 'ovarian', 'cancer', 'muscular', 'andor', 'becker'.Your task is to predict and return the label for each provided token, ensuring the number of output labels matches the number of input tokens exactly. The output format should include two parts: 1. tokens with their labels: ['Histidinemia.-SpecificDisease', 'Classical-O', 'and-O', 'atypical-O', 'form-O', 'in-O', 'siblings.-O'], tokens and labels in one sentence should be in one '[]', and within one line. 2. an empty line. Please strictly follow the output format to output the results. Please be sure to output each token and its corresponding label, and link them with '-'. When classifying tokens, consider the UMLS concepts and terminology, and the specific context of this social media dataset, to enhance the accuracy of your classifications.'}"}
assistant_message_0u = {"role": "user", "content": "['1', 'megabase', 'pairs', 'of', 'DNA', 'around', 'the', 'MCC', '(for', 'mutated', 'in', 'colorectal', 'carcinoma)', 'and', 'APC', '(for', 'adenomatous', 'polyposis', 'coli)', 'genes', 'at', '5q21', 'have', 'been', 'isolated', 'and', 'characterized.']"}
assistant_message_0a = {"role": "assistant", "content": "['1-O', 'megabase-O', 'pairs-O', 'of-O', 'DNA-O', 'around-O', 'the-O', 'MCC-O', '(for-O', 'mutated-O', 'in-O', 'colorectal-SpecificDisease', 'carcinoma)-SpecificDisease', 'and-O', 'APC-Modifier', '(for-O', 'adenomatous-Modifier', 'polyposis-Modifier', 'coli)-Modifier', 'genes-O', 'at-O', '5q21-O', 'have-O', 'been-O', 'isolated-O', 'and-O', 'characterized.-O']"}
assistant_message_1u = {"role": "user", "content": "['Mice', 'with', 'a', 'partial', 'or', 'complete', 'deficiency', 'of', 'Hmgic', 'resisted', 'diet-induced', 'obesity.', 'Disruption', 'of', 'Hmgic', 'caused', 'a', 'reduction', 'in', 'the', 'obesity', 'induced', 'by', 'leptin', 'deficiency', '(Lepob/Lepob)', 'in', 'a', 'gene-dose-dependent', 'manner.']"}
assistant_message_1a = {"role": "assistant", "content": "['Mice-O', 'with-O', 'a-O', 'partial-CompositeMention', 'or-CompositeMention', 'complete-CompositeMention', 'deficiency-CompositeMention', 'of-CompositeMention', 'Hmgic-CompositeMention', 'resisted-O', 'diet-induced-O', 'obesity.-SpecificDisease', 'Disruption-O', 'of-O', 'Hmgic-O', 'caused-O', 'a-O', 'reduction-O', 'in-O', 'the-O', 'obesity-SpecificDisease', 'induced-O', 'by-O', 'leptin-SpecificDisease', 'deficiency-SpecificDisease', '(Lepob/Lepob)-O', 'in-O', 'a-O', 'gene-dose-dependent-O', 'manner.-O']"}
assistant_message_2u = {"role": "user", "content": "['omatic', 'mutations', 'in', 'the', 'BRCA1', 'gene', 'in', 'sporadic', 'ovarian', 'tumours.', 'The', 'BRCA1', 'gene', 'on', 'chromosome', '17q21', 'is', 'responsible', 'for', 'an', 'autosomal', 'dominant', 'syndrome', 'of', 'increased', 'susceptibility', 'to', 'breast', 'and', 'ovarian', 'cancer', 'but', 'no', 'somatic', 'mutations', 'in', 'tumours', 'have', 'yet', 'been', 'described.']"}
assistant_message_2a = {"role": "assistant", "content": "['omatic-O', 'mutations-O', 'in-O', 'the-O', 'BRCA1-O', 'gene-O', 'in-O', 'sporadic-SpecificDisease', 'ovarian-SpecificDisease', 'tumours.-SpecificDisease', 'The-O', 'BRCA1-O', 'gene-O', 'on-O', 'chromosome-O', '17q21-O', 'is-O', 'responsible-O', 'for-O', 'an-O', 'autosomal-DiseaseClass', 'dominant-DiseaseClass', 'syndrome-DiseaseClass', 'of-O', 'increased-O', 'susceptibility-O', 'to-O', 'breast-CompositeMention', 'and-CompositeMention', 'ovarian-CompositeMention', 'cancer-CompositeMention', 'but-O', 'no-O', 'somatic-O', 'mutations-O', 'in-O', 'tumours-DiseaseClass', 'have-O', 'yet-O', 'been-O', 'described.-O']"}
assistant_message_3u = {"role": "user", "content": "['A', 'transgene', 'insertion', 'creating', 'a', 'heritable', 'chromosome', 'deletion', 'mouse', 'model', 'of', 'Prader-Willi', 'and', 'angelman', 'syndromes.', 'Prader-Willi', 'syndrome', '(PWS)', 'and', 'Angelman', 'syndrome', '(AS)', 'result', 'from', 'the', 'loss', 'of', 'function', 'of', 'imprinted', 'genes', 'in', 'human', 'chromosome', '15q11-q13.']"}
assistant_message_3a = {"role": "assistant", "content": "['A-O', 'transgene-O', 'insertion-O', 'creating-O', 'a-O', 'heritable-O', 'chromosome-O', 'deletion-O', 'mouse-O', 'model-O', 'of-O', 'Prader-Willi-CompositeMention', 'and-CompositeMention', 'angelman-CompositeMention', 'syndromes.-CompositeMention', 'Prader-Willi-SpecificDisease', 'syndrome-SpecificDisease', '(PWS)-O', 'and-O', 'Angelman-SpecificDisease', 'syndrome-SpecificDisease', '(AS)-O', 'result-O', 'from-O', 'the-O', 'loss-O', 'of-O', 'function-O', 'of-O', 'imprinted-O', 'genes-O', 'in-O', 'human-O', 'chromosome-O', '15q11-q13.-O']"}
assistant_message_4u = {"role": "user", "content": "['Von', 'Hippel-Lindau', 'disease', 'maps', 'to', 'the', 'region', 'of', 'chromosome', '3', 'associated', 'with', 'renal', 'cell', 'carcinoma.', 'Von', 'Hippel-Lindau', 'disease', '(VHL)', 'is', 'an', 'autosomal', 'dominant', 'disorder', 'with', 'inherited', 'susceptibility', 'to', 'various', 'forms', 'of', 'cancer,', 'including', 'hemangioblastomas', 'of', 'the', 'central', 'nervous', 'system,', 'phaeochromocytomas,', 'pancreatic', 'malignancies,', 'and', 'renal', 'cell', 'carcinomas.', 'Renal', 'cell', 'carcinomas', 'constitute', 'a', 'particularly', 'frequent', 'cause', 'of', 'death', 'in', 'this', 'disorder,', 'occurring', 'as', 'bilateral', 'and', 'multifocal', 'tumours,', 'and', 'presenting', 'at', 'an', 'earlier', 'age', 'than', 'in', 'sporadic,', 'non-familial', 'cases', 'of', 'this', 'tumour', 'type.']"}
assistant_message_4a = {"role": "assistant", "content": "['Von-SpecificDisease', 'Hippel-Lindau-SpecificDisease', 'disease-SpecificDisease', 'maps-O', 'to-O', 'the-O', 'region-O', 'of-O', 'chromosome-O', '3-O', 'associated-O', 'with-O', 'renal-SpecificDisease', 'cell-SpecificDisease', 'carcinoma.-SpecificDisease', 'Von-SpecificDisease', 'Hippel-Lindau-SpecificDisease', 'disease-SpecificDisease', '(VHL)-O', 'is-O', 'an-O', 'autosomal-DiseaseClass', 'dominant-DiseaseClass', 'disorder-DiseaseClass', 'with-O', 'inherited-O', 'susceptibility-O', 'to-O', 'various-O', 'forms-O', 'of-O', 'cancer,-DiseaseClass', 'including-O', 'hemangioblastomas-SpecificDisease', 'of-O', 'the-O', 'central-O', 'nervous-O', 'system,-O', 'phaeochromocytomas,-SpecificDisease', 'pancreatic-SpecificDisease', 'malignancies,-SpecificDisease', 'and-O', 'renal-SpecificDisease', 'cell-SpecificDisease', 'carcinomas.-SpecificDisease', 'Renal-SpecificDisease', 'cell-SpecificDisease', 'carcinomas-SpecificDisease', 'constitute-O', 'a-O', 'particularly-O', 'frequent-O', 'cause-O', 'of-O', 'death-O', 'in-O', 'this-O', 'disorder,-O', 'occurring-O', 'as-O', 'bilateral-CompositeMention', 'and-CompositeMention', 'multifocal-CompositeMention', 'tumours,-CompositeMention', 'and-O', 'presenting-O', 'at-O', 'an-O', 'earlier-O', 'age-O', 'than-O', 'in-O', 'sporadic,-O', 'non-familial-O', 'cases-O', 'of-O', 'this-O', 'tumour-Modifier', 'type.-O']"}
assistant_message_5u = {"role": "user", "content": "['Mutations', 'in', 'BRCA1', 'account', 'for', 'at', 'least', '80%', 'of', 'families', 'with', 'both', 'breast', 'and', 'ovarian', 'cancer,', 'as', 'well', 'as', 'some', 'non-familial', 'sporadic', 'ovarian', 'cancers.', 'The', 'loss', 'of', 'wild-type', 'BRCA1', 'in', 'tumours', 'of', 'individuals', 'carrying', 'one', 'nonfunctional', 'BRCA1', 'allele', 'suggests', 'that', 'BRCA1', 'encodes', 'a', 'tumour', 'suppressor', 'that', 'may', 'inhibit', 'the', 'proliferation', 'of', 'mammary', 'epithelial', 'cells.']"}
assistant_message_5a = {"role": "assistant", "content": "['Mutations-O', 'in-O', 'BRCA1-O', 'account-O', 'for-O', 'at-O', 'least-O', '80%-O', 'of-O', 'families-O', 'with-O', 'both-O', 'breast-CompositeMention', 'and-CompositeMention', 'ovarian-CompositeMention', 'cancer,-CompositeMention', 'as-O', 'well-O', 'as-O', 'some-O', 'non-familial-O', 'sporadic-O', 'ovarian-SpecificDisease', 'cancers.-SpecificDisease', 'The-O', 'loss-O', 'of-O', 'wild-type-O', 'BRCA1-O', 'in-O', 'tumours-DiseaseClass', 'of-O', 'individuals-O', 'carrying-O', 'one-O', 'nonfunctional-O', 'BRCA1-O', 'allele-O', 'suggests-O', 'that-O', 'BRCA1-O', 'encodes-O', 'a-O', 'tumour-Modifier', 'suppressor-O', 'that-O', 'may-O', 'inhibit-O', 'the-O', 'proliferation-O', 'of-O', 'mammary-O', 'epithelial-O', 'cells.-O']"}
assistant_message_6u = {"role": "user", "content": "['Seven', 'classical', 'cases', 'had', 'facial', 'features', 'suggestive', 'of', 'frontonasal', 'dysplasia', 'and', 'coronal', 'craniosynostosis.', 'Extracranial', 'abnormalities', 'such', 'as', 'brittle', 'nails', 'with', 'prominent', 'longitudinal', 'grooves', 'or', 'syndactyly', 'of', 'fingers', 'and', 'toes', 'were', 'observed', 'in', 'individual', 'patients.']"}
assistant_message_6a = {"role": "assistant", "content": "['Seven-O', 'classical-O', 'cases-O', 'had-O', 'facial-O', 'features-O', 'suggestive-O', 'of-O', 'frontonasal-SpecificDisease', 'dysplasia-SpecificDisease', 'and-O', 'coronal-SpecificDisease', 'craniosynostosis.-SpecificDisease', 'Extracranial-DiseaseClass', 'abnormalities-DiseaseClass', 'such-O', 'as-O', 'brittle-SpecificDisease', 'nails-SpecificDisease', 'with-SpecificDisease', 'prominent-SpecificDisease', 'longitudinal-SpecificDisease', 'grooves-SpecificDisease', 'or-O', 'syndactyly-CompositeMention', 'of-CompositeMention', 'fingers-CompositeMention', 'and-CompositeMention', 'toes-CompositeMention', 'were-O', 'observed-O', 'in-O', 'individual-O', 'patients.-O']"}
assistant_message_7u = {"role": "user", "content": "['A', 'germ', 'line', 'mutation', 'within', 'the', 'coding', 'sequence', 'for', 'the', 'putative', '5-phosphoribosyl-1-pyrophosphate', 'binding', 'site', 'of', 'hypoxanthine-guanine', 'phosphoribosyltransferase', '(HPRT)', 'in', 'a', 'Lesch-Nyhan', 'patient:', 'missense', 'mutations', 'within', 'a', 'functionally', 'important', 'region', 'probably', 'cause', 'disease.']"}
assistant_message_7a = {"role": "assistant", "content": "['A-O', 'germ-O', 'line-O', 'mutation-O', 'within-O', 'the-O', 'coding-O', 'sequence-O', 'for-O', 'the-O', 'putative-O', '5-phosphoribosyl-1-pyrophosphate-O', 'binding-O', 'site-O', 'of-O', 'hypoxanthine-guanine-O', 'phosphoribosyltransferase-O', '(HPRT)-O', 'in-O', 'a-O', 'Lesch-Nyhan-Modifier', 'patient:-O', 'missense-O', 'mutations-O', 'within-O', 'a-O', 'functionally-O', 'important-O', 'region-O', 'probably-O', 'cause-O', 'disease.-O']"}
assistant_message_8u = {"role": "user", "content": "['Using', 'DNA', 'as', 'the', 'starting', 'material,', 'we', 'screened', 'the', 'ATM', 'gene', 'in', '92', 'A-T', 'patients,', 'using', 'an', 'optimized', 'single-strand', 'conformation', 'polymorphism', '(SSCP)', 'technique', 'that', 'detected', 'all', 'previously', 'known', 'mutations', 'in', 'the', 'polymerase', 'chain', 'reaction', '(PCR)', 'segments', 'being', 'analyzed.']"}
assistant_message_8a = {"role": "assistant", "content": "['Using-O', 'DNA-O', 'as-O', 'the-O', 'starting-O', 'material,-O', 'we-O', 'screened-O', 'the-O', 'ATM-O', 'gene-O', 'in-O', '92-O', 'A-T-Modifier', 'patients,-O', 'using-O', 'an-O', 'optimized-O', 'single-strand-O', 'conformation-O', 'polymorphism-O', '(SSCP)-O', 'technique-O', 'that-O', 'detected-O', 'all-O', 'previously-O', 'known-O', 'mutations-O', 'in-O', 'the-O', 'polymerase-O', 'chain-O', 'reaction-O', '(PCR)-O', 'segments-O', 'being-O', 'analyzed.-O']"}
assistant_message_9u = {"role": "user", "content": "['These', 'results', 'provide', 'evidence', 'that', 'the', 'DM', 'mutation', 'acts', 'in', 'cis', 'to', 'reduce', 'protein', 'production', '(consistent', 'with', 'DMPK', 'haploinsufficiency)', 'and', 'in', 'trans', 'as', 'a', 'riboregulator', 'to', 'inhibit', 'myogenesis..']"}
assistant_message_9a = {"role": "assistant", "content": "['These-O', 'results-O', 'provide-O', 'evidence-O', 'that-O', 'the-O', 'DM-Modifier', 'mutation-O', 'acts-O', 'in-O', 'cis-O', 'to-O', 'reduce-O', 'protein-O', 'production-O', '(consistent-O', 'with-O', 'DMPK-SpecificDisease', 'haploinsufficiency)-SpecificDisease', 'and-O', 'in-O', 'trans-O', 'as-O', 'a-O', 'riboregulator-O', 'to-O', 'inhibit-O', 'myogenesis..-O']"}
   

file_path = '/Users/yaoge/Downloads/ncbi_texts2.txt'

# Read each line from the file and make an API call
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Strip newline characters from the end of the line
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Create a new user message with the current line
        user_message = {"role": "user", "content": line}
        
        # Construct messages for the current iteration
        messages = [system_message, assistant_message_0u, assistant_message_0a, assistant_message_1u, assistant_message_1a, assistant_message_2u, assistant_message_2a, assistant_message_3u, assistant_message_3a, assistant_message_4u, assistant_message_4a, assistant_message_5u, assistant_message_5a, assistant_message_6u, assistant_message_6a, assistant_message_7u, assistant_message_7a, assistant_message_8u, assistant_message_8a, assistant_message_9u, assistant_message_9a, user_message]
        #messages = [system_message, user_message]

        # Make the API call
        completion = openai.ChatCompletion.create(
            engine="app0212",
            messages=messages,
            temperature=0.2,
            max_tokens=500,
            top_p=0.1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        
        # Process the response
        with open('/Users/yaoge/Downloads/ncbi_pred_all.txt','a') as wf:
        	print(user_message)
        	wf.write(completion['choices'][0]['message']['content'])
        #print(completion['choices'][0]['message']['content'])

        # Add a delay if needed to avoid rate limits
        time.sleep(1)


