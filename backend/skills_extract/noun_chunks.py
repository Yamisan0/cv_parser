import spacy
import re
import pandas as pd
import os
from fuzzywuzzy import fuzz

# Charger le modèle spaCy pour l'anglais
nlp = spacy.load('en_core_web_sm')

def normalize_skill(skill):
    """
    Normalize the skill name by converting to lower case and replacing common separators with spaces.
    """
    return re.sub(r'[-_.]', ' ', skill.lower()).strip()

def extract_skills(nlp_text, noun_chunks, skills_file=None, threshold=80):
    '''
    Helper function to extract skills from spacy nlp text using normalization and fuzzy matching.

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :param skills_file: path to the CSV file containing skills
    :param threshold: fuzzy matching threshold (default is 80)
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    if not skills_file:
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), 'skills.csv')
        )
    else:
        data = pd.read_csv(skills_file, header=None)
    skills = list(data[0])
    # Normalize skills list
    normalized_skills = {skill: normalize_skill(skill) for skill in skills}
    
    skillset = []

    # Function to check fuzzy match
    def is_fuzzy_match(candidate, skill):
        ratio = fuzz.ratio(candidate, skill)
        
        if ratio > threshold:
            print(f'Candidate: {candidate}, Skill: {skill}, Ratio: {ratio}')
        return ratio >= threshold

    # Check for one-grams (mots uniques)
    for token in tokens:
        normalized_token = normalize_skill(token)
        for skill, normalized_skill in normalized_skills.items():
            # print(f'Normalized Token: {normalized_token}, original token = {token} Normalized Skill: {normalized_skill}')
            if is_fuzzy_match(normalized_token, normalized_skill):
                skillset.append(skill)
                break

    # Check for bi-grams and tri-grams (groupes nominaux)
    for chunk in noun_chunks:
        normalized_chunk = normalize_skill(chunk.text)
        for skill, normalized_skill in normalized_skills.items():
            if is_fuzzy_match(normalized_chunk, normalized_skill):
                skillset.append(skill)
                break
    
    # Additional check for patterns in the text using regex
    pattern = re.compile(r'\b(' + '|'.join(re.escape(skill) for skill in skills) + r')\b', re.IGNORECASE)
    matches = pattern.findall(nlp_text.text)
    for match in matches:
        skillset.append(match)

    # Normalize and remove duplicates
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# Exemple de texte
text = "Proficient in Python, data analysis, machine learning, SQL, NestJS, Nest.js, Nest js, Ruby on Rails, and C. nextjs"
nlp_text = nlp(text)
noun_chunks = list(nlp_text.noun_chunks)

skills = extract_skills(nlp_text, noun_chunks, skills_file='skills.csv', threshold=80)
print(skills)
