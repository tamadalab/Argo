import pandas as pd

def extract_name_column(csv_file_path):
    df = pd.read_csv(csv_file_path,encoding="utf-8")
    
    name_column = df["name"]
    
    with open("big_project.txt", 'w', encoding="utf-8") as output_file:
            name_column.to_string(output_file, index=False)
extract_name_column("big_projects.csv")