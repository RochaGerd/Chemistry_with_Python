import os
import csv

# Função para extrair o valor de "FINAL HEAT OF FORMATION" de um arquivo txt
def extract_heat_of_formation(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "FINAL HEAT OF FORMATION" in line:
                # Extrair o valor depois do "="
                value = line.split('=')[1].strip().split()[0]
                return value
    return None

# Diretório contendo os arquivos out 
# Esse dado precisa ser editado
directory = "/home/rochagb/my_files/Minicurso/exercicio2"

# Lista para armazenar os dados
data = []

# Percorrer todos os arquivos no diretório
for filename in os.listdir(directory):
    if filename.endswith(".out"):
        file_path = os.path.join(directory, filename)
        value = extract_heat_of_formation(file_path)
        if value:
            data.append([filename, value])

# Escrever os dados em um arquivo CSV
csv_file = "heat_of_formation.csv"
with open(csv_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Filename", "Heat of Formation (KCAL/MOL)"])
    csvwriter.writerows(data)

print(f"Data extracted and saved to {csv_file}")

