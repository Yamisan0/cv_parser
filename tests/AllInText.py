from pathlib import Path


def combine_files(input_dir: Path, output_file: Path) -> None:
#Recupere tout le texte des fichiers csv dans un dossier et les combine dans un fichier texte
    try:
        if not isinstance(input_dir, Path):
            raise TypeError("input_dir must be a Path object")
        if not isinstance(output_file, Path):
            raise TypeError("output_file must be a Path object")
        if not input_dir.exists():
            raise ValueError("input_dir does not exist")
        
        with open(output_file, 'w') as outfile:
            for file in input_dir.glob("*.csv"):
                if file.is_file():
                    with open(file, 'r') as infile:
                        outfile.write(infile.read() + "\n")
        
        print(f"All files in {input_dir} have been combined into {output_file}")
    
    except Exception as error:
        print(f"An error occurred: {error}")

combine_files(Path("../../cv_parser/backend/src/skills_csv/"), Path("./test.txt"))
