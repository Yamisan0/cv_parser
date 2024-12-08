import json
import re
import sys
import os
from cv_extractor import CvExtractor

class CvLittleParser:
    @staticmethod
    def read_keywords(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                keywords = json.load(file)
            return keywords
        except Exception as e:
            print(f"Erreur lors de la lecture des mots-clés: {e}")
            return None

    @staticmethod
    def verifier_pertinence_mots_cles(cv_text, keywords):
        cv_text = cv_text.lower()
        mots_cles_trouves = {"Fort": [], "Moyen": [], "Faible": []}
        score = 0
        has_fort = False
        
        for category, mots_cles in keywords.items():
            for mot in mots_cles:
                if re.search(r'\b' + re.escape(mot.lower()) + r'\b', cv_text):
                    mots_cles_trouves[category].append(mot)
                    if category == "Fort":
                        score += 3
                        has_fort = True
                    elif category == "Moyen":
                        score += 2
                    elif category == "Faible":
                        score += 1

        result = {
            "Concordances": mots_cles_trouves,
            "Score": score,
            "AlerteFort": not has_fort
        }

        return result

if __name__ == "__main__":
    def process_cv_file(cv_text, keywords_path):
        if cv_text is None:
            print(f"Erreur: Impossible de lire le fichier CV {cv_text}.")
            return None

        mots_cles = CvLittleParser.read_keywords(keywords_path)
        if mots_cles is None:
            print("Erreur: Impossible de lire les mots-clés.")
            return None

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
                    results.append((file_path, result["Score"], result["AlerteFort"]))
                index += 1
    elif os.path.isfile(path):
        result = process_cv_file(path, keywords_path)
        if result is not None:
            results.append((path, result["Score"], result["AlerteFort"]))
    else:
        print("Erreur: Le chemin spécifié n'est ni un fichier ni un répertoire.")
        sys.exit(1)

    results.sort(key=lambda x: x[1], reverse=True)
    ranked_results = []
    for rank, (file_path, score, has_fort) in enumerate(results, start=1):
        ranked_results.append({
            "rank": rank,
            "file_path": file_path,
            "score": score,
            "alerteFort": has_fort,
        })

    print(json.dumps(ranked_results, ensure_ascii=False, indent=4))
