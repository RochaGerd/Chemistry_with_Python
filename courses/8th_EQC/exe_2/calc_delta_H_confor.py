import pandas as pd

# Carregar o arquivo CSV em um DataFrame do pandas
df = pd.read_csv('heat_of_formation_exe_2.csv')

# Criar um novo DataFrame para armazenar os resultados
results = pd.DataFrame(columns=['Molécula', 'Método', 
                                'Calor de Reação (kcal/mol)'])

# Definir os métodos semiempíricos
methods = ['AM1', 'PM3', 'RM1']

# Definir as moléculas
molecules = ['MOL_CH3', 'MOL_TBUTIL']

# Loop sobre cada molécula e cada método semiempírico
for molecule in molecules:
    for method in methods:
        # Filtrar o DataFrame para obter as linhas correspondentes à molécula 
        # e método atual
        filtered_df = df[df['Filename'].str.startswith(method) 
        & df['Filename'].str.contains(molecule)]

        # Obter os valores de calor de formação para as formas equatorial e axial
        equatorial_heat = \
        filtered_df[filtered_df['Filename'].str.contains('EQUATORIAL')] \
         ['Heat of Formation (kcal/mol)'].values[0]
        axial_heat = \
        filtered_df[filtered_df['Filename'].str.contains('AXIAL')] \
         ['Heat of Formation (kcal/mol)'].values[0]

        # Calcular o calor de reação (axial - equatorial)
        heat_of_reaction = axial_heat - equatorial_heat  

        # Adicionar os resultados ao DataFrame de resultados
        results = pd.concat([results, pd.DataFrame(
            {'Molécula': [molecule], 'Método': [method], 
             'Calor de Reação (kcal/mol)': [heat_of_reaction]})], 
                            ignore_index=True)

# Exibir o DataFrame de resultados
print(results)

# Salvar o DataFrame de resultados em um arquivo CSV
results.to_csv('heat_of_reaction_results_exe_2.csv', index=False)
