import os
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def read_content_from_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"File '{filepath}' does not exist.")
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return data.get("content", [])


    def create_file(self, fort_file, moyen_file, faible_file):
        fort_content = self.read_content_from_file(fort_file)
        moyen_content = self.read_content_from_file(moyen_file)
        faible_content = self.read_content_from_file(faible_file)

        data = {
            "Fort": fort_content,
            "Moyen": moyen_content,
            "Faible": faible_content
        }

        with open(self.filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"File '{self.filename}' created successfully.")

    def read_file(self):
        if not os.path.exists(self.filename):
            print(f"File '{self.filename}' does not exist.")
            return None
        
        with open(self.filename, 'r') as f:
            content = f.read()
        
        #print(f"Content of '{self.filename}':")
        #print(content)
        
        return content

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 5:
        print("Usage: python3 file_manager.py <filename> <fort file> <moyen file> <faible file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    fort_file = sys.argv[2]
    moyen_file = sys.argv[3]
    faible_file = sys.argv[4]
    
    file_manager = FileManager(filename)
    
    file_manager.create_file(fort_file, moyen_file, faible_file)
    
    file_manager.read_file()
