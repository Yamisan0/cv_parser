import json
import re
import sys
import os
from cv_extractor import CvExtractor
from scripts.abd_better_parse import WordSearcher

class CvLittleParser:
    @staticmethod
    def read_keywords(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                keywords = [line.strip() for line in file]
            return keywords
        except Exception as e:
            print(f"Erreur lors de la lecture des mots-clés: {e}")
            return None

    @staticmethod
    def verifier_pertinence_mots_cles(cv_text, mots_cles):
        cv_text = cv_text.lower()
        mots_cles_trouves = []
        score = 0

        for mot in mots_cles:
            if re.search(r'\b' + re.escape(mot.lower()) + r'\b', cv_text):
                mots_cles_trouves.append(mot)
                score += 1

        return {
            "Concordances": mots_cles_trouves,
            "Score": score
        }

if __name__ == "__main__":
    def process_cv_file(cv_text, keywords_path):
        if cv_text is None:
            print(f"Erreur: Impossible de lire le fichier CV {cv_text}.")
            return None

        mots_cles = CvLittleParser.read_keywords(keywords_path)
        if mots_cles is None:
            print("Erreur: Impossible de lire les mots-clés.")
            return None

        #word_searcher = WordSearcher(mots_cles)  # Utilisation de WordSearcher
        #mots_cles_utilises = word_searcher.get_words()

        cv_extractor = CvExtractor(cv_text)
        cv_extractor.extract()

        resultat = CvLittleParser.verifier_pertinence_mots_cles(cv_extractor.text, mots_cles)
        #resultat_json = json.dumps(resultat, ensure_ascii=False, indent=4)
        #print(f"Résultats pour {index}:\n{resultat_json}\n")

        return resultat

    if len(sys.argv) < 3:
        print("Usage: python script.py <directory_or_file_path> <mots_cles>")
        sys.exit(1)

    path = sys.argv[1]
    keywords_path = sys.argv[2]

    index = 1
    results = []

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                result = process_cv_file(file_path, keywords_path)
                if result is not None:
                    results.append((file_path, result["Score"]))
                index += 1
    elif os.path.isfile(path):
        result = process_cv_file(path, keywords_path)
        
    if result is not None:
        results.append((path, result["Score"]))
    else:
        print("Erreur: Le chemin spécifié n'est ni un fichier ni un répertoire.")
        sys.exit(1)

    results.sort(key=lambda x: x[1], reverse=True)
    for rank, (file_path, score) in enumerate(results, start=1):
        print(f"{rank}. Score: \033[1;32m{score}\033[0m")
        