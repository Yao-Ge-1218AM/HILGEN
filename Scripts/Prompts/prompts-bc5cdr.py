import os
import openai
import json
import time

openai.api_type = "azure"
openai.api_base = ""
openai.api_version = "2023-07-01-preview"
openai.api_key = ""

#system_message = {"role": "system", "content": "You are a medical AI trained to identify and classify tokens into three categories: Clinical Impacts, Social Impacts, and Outside ('O'), with an understanding of medical concepts from the Unified Medical Language System (UMLS). You understand medical terminology and concepts. The data you are working with has been collected from 14 forums on Reddit (subreddits) that focused on prescription and illicit opioids, and medications for opioid use disorder. This dataset represents a social media context, coming from individuals who may use prescription and illicit opioids and stimulants. In this dataset, high-frequency clinical impacts include 'withdrawal', 'rehab', 'addicted', 'detox', 'overdosed', and 'rehabs'. High-frequency social impacts include 'lost', 'homeless', 'charged', 'streets', 'jail', and 'disorderly'.  Your task is to extract and classify the clinical and social impacts from this dataset, considering your knowledge of the lifestyle of this population and the potential clinical and social impacts they might experience.  'Clinical Impacts' refer to tokens describing the effects, consequences, or impacts of substance use on individual health or well-being, as defined in UMLS. 'Social Impacts' describe the societal, interpersonal, or community-level effects, also based on UMLS definitions. Any token not falling into these categories should be labeled as 'O'. Your task is to predict and return the label for each provided token, ensuring the number of output labels matches the number of input tokens exactly. The output format should be tokens with their labels: ['I-O', 'was-O', 'a-O', 'codeine-Clinical Impacts', 'addict-Clinical Impacts', '.-O']. Please strictly follow the output format to output the results. Please be sure to output each token and its corresponding label, and link them with '-'. When classifying tokens, consider the UMLS concepts and terminology, and the specific context of this social media dataset, to enhance the accuracy of your classifications. Please use the tokens I provided, do not use other tokenization mechanism."

    #}
system_message = {"role": "system", "content": "You are a medical AI trained to identify and classify tokens into three categories: 'Disease', 'Chemical' and Outside ('O'), with an understanding of medical concepts from the Unified Medical Language System (UMLS). You understand medical terminology and concepts. Your task is to extract and classify the Disease and Chemical related concepts from this dataset, considering your knowledge of UMLS. 'Disease' is a particular abnormal condition that adversely affects the structure or function of all or part of an organism and is not immediately due to any external injury. Diseases are often known to be medical conditions that are associated with specific signs and symptoms. A disease may be caused by external factors such as pathogens or by internal dysfunctions. For example, internal dysfunctions of the immune system can produce a variety of different diseases, including various forms of immunodeficiency, hypersensitivity, allergies, and autoimmune disorders. 'Chemical' in this context refers to substances or compounds with specific chemical properties and structures. These can include drugs, neurotransmitters, elements or ions, vitamins, and other medically relevant chemicals. Any token not falling into Disease categories should be labeled as 'O'. Each token, is provided separately and should be classified accordingly. For example, the sentence 'The hypotensive effect of 100 mg / kg alpha-methyldopa was also partially reversed by naloxone .' is tokenized and labeled as follows: ['The', 'hypotensive', 'effect', 'of', '100', 'mg', '/', 'kg', 'alpha-methyldopa', 'was', 'also', 'partially', 'reversed', 'by', 'naloxone', '.'] with labels ['O', 'Disease', 'O', 'O', 'O', 'O', 'O', 'O', 'Chemical', 'O', 'O', 'O', 'O', 'O', 'Chemical', 'O']. Your task is to predict and return the label for each provided token, ensuring the number of output labels matches the number of input tokens exactly. The output format should include two parts: 1. tokens with their labels: ['The-O', 'hypotensive-Disease', 'effect-O', 'of-O', '100-O', 'mg-O', '/-O', 'kg-O', 'alpha-methyldopa-Chemical', 'was-O', 'also-O', 'partially-O', 'reversed-O', 'by-O', 'naloxone-Chemical', '.-O'], tokens and labels in one sentence should be in one '[]', and within one line. 2. an empty line. Please strictly follow the output format to output the results. Please be sure to output each token and its corresponding label, and link them with '-'. When classifying tokens, consider the UMLS concepts and terminology, and the specific context of this social media dataset, to enhance the accuracy of your classifications.'}"}
"""
assistant_message_0u = {"role": "user", "content": "['HISTORY', 'OF', 'PRESENT', 'ILLNESS', '76', 'yo', 'F', 'walking', 'to', 'dentists', 'office', '3-22', 'and', 'had', 'SOB/CP/diaphoresis']"}
assistant_message_0a = {"role": "assistant", "content": "['HISTORY-O', 'OF-O', 'PRESENT-O', 'ILLNESS-O', '76-AGE', 'yo-O', 'F-GENDER', 'walking-O', 'to-O', 'dentists-LOCATION', 'office-LOCATION', '3-22-O', 'and-O', 'had-O', 'SOB/CP/diaphoresis-SYMPTOM']"}
assistant_message_1u = {"role": "user", "content": "['Pt', 'was', 'alert', 'upon', 'ems', 'arrival', 'and', 'became', 'unresponsive', 'enroute', 'to', 'hospital']"}
assistant_message_1a = {"role": "assistant", "content": "['Pt-O', 'was-O', 'alert-O', 'upon-O', 'ems-ORGANIZATION', 'arrival-O', 'and-O', 'became-O', 'unresponsive-SYMPTOM', 'enroute-TIME', 'to-O', 'hospital-LOCATION']"}
assistant_message_2u = {"role": "user", "content": "['HISTORY', 'OF', 'PRESENT', 'ILLNESS', '55', 'year-old', 'female', 'presents', 'with', '2/5', 'week', 'history', 'of', 'non-bloody', 'diarrhea']"}
assistant_message_2a = {"role": "assistant", "content": "['HISTORY-O', 'OF-O', 'PRESENT-O', 'ILLNESS-O', '55-AGE', 'year-old-O', 'female-GENDER', 'presents-O', 'with-O', '2/5-AMOUNT', 'week-AMOUNT', 'history-O', 'of-O', 'non-bloody-SYMPTOM', 'diarrhea-SYMPTOM']"}
assistant_message_3u = {"role": "user", "content": "['Today', 'he', 'slept', 'throughout', 'the', 'day', 'and', 'had', 'some', 'urinary', 'frequency/urgency', 'in', 'the', 'morning', 'that', 'resolved', 'this', 'afternoon']"}
assistant_message_3a = {"role": "assistant", "content": "['Today-O', 'he-O', 'slept-EVENT', 'throughout-TIME', 'the-TIME', 'day-TIME', 'and-O', 'had-O', 'some-O', 'urinary-SYMPTOM', 'frequency/urgency-SYMPTOM', 'in-TIME', 'the-TIME', 'morning-TIME', 'that-O', 'resolved-O', 'this-TIME', 'afternoon-TIME']"}
assistant_message_4u = {"role": "user", "content": "['This', 'morning', ',', 'he', 'took', 'all', 'his', 'medications', 'and', 'his', 'blood', 'pressures', 'have', 'been', 'in', 'the', 'SBP90s']"}
assistant_message_4a = {"role": "assistant", "content": "['This-TIME', 'morning-TIME', ',-O', 'he-O', 'took-O', 'all-O', 'his-O', 'medications-O', 'and-O', 'his-O', 'blood-MEASUREMENT', 'pressures-MEASUREMENT', 'have-MEASUREMENT', 'been-MEASUREMENT', 'in-MEASUREMENT', 'the-MEASUREMENT', 'SBP90s-MEASUREMENT']"}
assistant_message_5u = {"role": "user", "content": "['Upon', 'transfer', 'to', 'the', 'medical', 'floor', ',', 'vitals', 'were', 'T', '98.1', 'P', '88', 'BP', '103/45', 'RR', '25', 'SaO2', '95%', 'on', '2L', 'NC', 'does', 'not', 'use', 'oxygen', 'at', 'home', '.']"}
assistant_message_5a = {"role": "assistant", "content": "['Upon-O', 'transfer-EVENT', 'to-O', 'the-LOCATION', 'medical-LOCATION', 'floor-LOCATION', ',-O', 'vitals-O', 'were-O', 'T-MEASUREMENT', '98.1-MEASUREMENT', 'P-MEASUREMENT', '88-MEASUREMENT', 'BP-MEASUREMENT', '103/45-MEASUREMENT', 'RR-MEASUREMENT', '25-MEASUREMENT', 'SaO2-MEASUREMENT', '95%-MEASUREMENT', 'on-MEASUREMENT', '2L-MEASUREMENT', 'NC-MEASUREMENT', 'does-O', 'not-O', 'use-O', 'oxygen-DRUG', 'at-O', 'home-LOCATION', '.-O']"}
assistant_message_6u = {"role": "user", "content": "['The', 'patient's', 'wife', 'was', 'Name', 'NI', '653', 'by', 'the', 'Name', 'NI', 'QA', 'via', 'Name', 'NI', '595', 'interpreter', 'and', 'Cipro', '250mg', 'tablets', 'daily', 'X', '7', 'days', 'was', 'prescribed']"}
assistant_message_6a = {"role": "assistant", "content": "['The-O', 'patients-O', 'wife-O', 'was-O', 'Name-O', 'NO', '653-O', 'by-O', 'the-O', 'Name-O', 'NO', 'QA-O', 'via-O', 'Name-O', 'NO', '595-O', 'interpreter-O', 'and-O', 'Cipro-DRUG', '250mg-AMOUNT', 'tablets-AMOUNT', 'daily-FREQUENCY', 'X-AMOUNT', '7-AMOUNT', 'days-AMOUNT', 'was-O', 'prescribed-O']"}
assistant_message_7u = {"role": "user", "content": "['He', 'was', 'discharged', 'on', 'Macrobid', '100mg', 'twice', 'daily', 'X', '7', 'days']"}
assistant_message_7a = {"role": "assistant", "content": "['He-O', 'was-O', 'discharged-EVENT', 'on-O', 'Macrobid-DRUG', '100mg-AMOUNT', 'twice-FREQUENCY', 'daily-FREQUENCY', 'X-AMOUNT', '7-AMOUNT', 'days-AMOUNT']"}
assistant_message_8u = {"role": "user", "content": "['I', 'last', 'saw', 'him', 'on', '2149-11-17', 'and', 'his', 'head', 'CT', 'showed', 'growth', 'of', 'the', 'left', 'sphenoid', 'meningioma']"}
assistant_message_8a = {"role": "assistant", "content": "['O', 'last-O', 'saw-O', 'him-O', 'on-O', '2149-11-17-DATE', 'and-O', 'his-O', 'head-EVENT', 'CT-EVENT', 'showed-O', 'growth-O', 'of-O', 'the-O', 'left-SYMPTOM', 'sphenoid-SYMPTOM', 'meningioma-SYMPTOM']"}
assistant_message_9u = {"role": "user", "content": "['She', 'was', 'recently', 'seen', 'by', 'her', 'Primary', 'Care', 'Physician', 'for', 'evaluation', 'of', 'diarrhea', 'and', 'by', 'report', 'stool', 'O&P', 'cultures', 'were', 'negative', '.']"}
assistant_message_9a = {"role": "assistant", "content": "['She-O', 'was-O', 'recently-O', 'seen-O', 'by-O', 'her-O', 'Primary-ORGANIZATION', 'Care-ORGANIZATION', 'Physician-ORGANIZATION', 'for-O', 'evaluation-EVENT', 'of-O', 'diarrhea-SYMPTOM', 'and-O', 'by-O', 'report-O', 'stool-MEASUREMENT', 'O&P-MEASUREMENT', 'cultures-MEASUREMENT', 'were-MEASUREMENT', 'negative-MEASUREMENT', '.-O']"}
assistant_message_10u = {"role": "user", "content": "['The', 'patient', 'was', 'readmitted', 'to', 'the', 'hospital', 'on', '2195-6-6', 'due', 'to', 'fevers', 'to', '103', 'at', 'the', 'rehabilitation', 'facility', 'despite', 'being', 'on', 'intravenous', 'antibiotics']"}
assistant_message_10a = {"role": "assistant", "content": "['The-O', 'patient-O', 'was-O', 'readmitted-EVENT', 'to-O', 'the-LOCATION', 'hospital-LOCATION', 'on-O', '2195-6-6-O', 'due-O', 'to-O', 'fevers-MEASUREMENT', 'to-MEASUREMENT', '103-MEASUREMENT', 'at-O', 'the-LOCATION', 'rehabilitation-LOCATION', 'facility-LOCATION', 'despite-O', 'being-O', 'on-O', 'intravenous-DRUG', 'antibiotics-DRUG']"}
"""  

file_path = '/Users/yaoge/Downloads/bc5cdr_texts1.txt'

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
        #messages = [system_message, assistant_message_0u, assistant_message_0a, assistant_message_1u, assistant_message_1a, assistant_message_2u, assistant_message_2a, assistant_message_3u, assistant_message_3a, assistant_message_4u, assistant_message_4a, assistant_message_5u, assistant_message_5a, assistant_message_6u, assistant_message_6a, assistant_message_7u, assistant_message_7a, assistant_message_8u, assistant_message_8a, assistant_message_9u, assistant_message_9a, assistant_message_10u, assistant_message_10a, user_message]
        messages = [system_message, user_message]

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
        with open('/Users/yaoge/Downloads/bc5cdr_pred_UMLS.txt','a') as wf:
        	#print(user_message)
        	wf.write(completion['choices'][0]['message']['content'])
        #print(completion['choices'][0]['message']['content'])

        # Add a delay if needed to avoid rate limits
        time.sleep(1)


