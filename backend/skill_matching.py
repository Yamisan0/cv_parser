from cv_extractor import CvExtractor
from sys import argv
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Liste de compétences que vous souhaitez détecter
skills = [
    'Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis',
    'C++', 'C#', 'JavaScript', 'HTML', 'CSS', 'R', 'Go', 'Ruby', 'PHP',
    'Swift', 'Kotlin', 'Django', 'Flask', 'React', 'Angular', 'Vue.js', 'Next.js', 'NestJS', 'Nuxt'
]


def clean_text(text):
    # Supprimer les caractères spéciaux et les chiffres, sauf les points et les tirets
    text = re.sub(r'[^a-zA-Z\s\.-]', '', text)
    # Supprimer les points et les tirets isolés
    text = re.sub(r'\s*[\.-]\s*', ' ', text)
    return text

def generate_ngrams(text, n):
    words = text.split()
    ngrams = zip(*[words[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]

# Fonction pour extraire les compétences avec recherche floue
def extract_skills(cv_text):
    cv_text = clean_text(cv_text)
    
    # Liste pour stocker les compétences trouvées
    found_skills = []
    
    # Générer des 1-grams, 2-grams, et 3-grams
    ngrams = generate_ngrams(cv_text, 1) + generate_ngrams(cv_text, 2) + generate_ngrams(cv_text, 3)
    
    # Parcourir chaque n-gram et vérifier la similarité avec les compétences listées
    for ngram in ngrams:
        # Trouver la meilleure correspondance avec une limite de score de 80
        best_match = process.extractOne(ngram, skills, scorer=fuzz.token_set_ratio, score_cutoff=80)
        if best_match:
            found_skills.append(best_match[0])
    
    # Retourner une liste unique de compétences trouvées
    return list(set(found_skills))

# Exemple d'utilisation
cv_text = """
John Doe
1234 Elm Street, Springfield, IL 62704

Experience:
- Software Engineer at Tech Company (2018-2021)
- Developed applications using Python and Java
- Experience with SQL databases and Machine Learning

Skills:
- Python, Java, Machine Learning, Data Analysis, HTML, CSS, JavaScript, Nextjs, React.js

Education:
- BSc in Computer Science from University of Springfield
"""

# Extraire les compétences du texte du CV
# skills_found = extract_skills(cv_text)
# print(skills_found)


if __name__ == "__main__":
    file_path = argv[1]
    cv = CvExtractor(file_path=file_path)
    cv.extract()
    skills = extract_skills(cv.text)
    print(skills)
    # print(cv.text)
