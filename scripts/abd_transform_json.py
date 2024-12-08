import json
import sys

def txt_to_json(txt_file_path, json_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines = [line.strip() for line in lines if line.strip()]
    
    data = {"content": lines}
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        
    print(f"Fichier JSON créé : {json_file_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <fichier_txt> <fichier_json>")
        sys.exit(1)
    
    txt_file_path = sys.argv[1]
    json_file_path = sys.argv[2]
    
    txt_to_json(txt_file_path, json_file_path)

if __name__ == "__main__":
    main()
