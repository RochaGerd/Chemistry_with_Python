import pandas as pd
from ase import Atoms
from ase.optimize import BFGS
from ase.calculators.mopac import MOPAC
from rdkit import Chem
from rdkit.Chem import AllChem

# Função para converter SMILES para objeto Atoms do ASE
def smiles_to_ase_atoms(smiles):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    positions = mol.GetConformer().GetPositions()
    return Atoms(symbols=atoms, positions=positions)

# Lista de SMILES das moléculas com identificação
molecules = [
    {'smiles': 'C', 'id': 'molecule_1'},  # Metano
    {'smiles': 'CC(=O)C', 'id': 'molecule_2'},  # Acetona
    {'smiles': 'CC', 'id': 'molecule_3'},  # Etano
    {'smiles': 'CC=O', 'id': 'molecule_4'}  # Etanal
]

# Inicializar dicionário para armazenar resultados
results = {'Molecule': [], 'SMILES': []}

# Adicionar colunas para cada método
methods = ['AM1', 'PM3', 'RM1']
for method in methods:
    results[method] = []

# Loop sobre cada molécula e cada método semiempírico
for mol in molecules:
    mol_id = mol['id']
    smiles = mol['smiles']
    ase_atoms = smiles_to_ase_atoms(smiles)

    # Adicionar informações básicas da molécula
    results['Molecule'].append(mol_id)
    results['SMILES'].append(smiles)

    for method in methods:
        # Configurar o calculador MOPAC
        calc = MOPAC(label=mol_id, task='GRADIENTS XYZ GNORM=0.01', method=method)
        ase_atoms.set_calculator(calc)

        # Otimizar a geometria
        opt = BFGS(ase_atoms)
        opt.run(fmax=0.05)

        # Obter o calor de formação da última linha do arquivo .out
        with open(f'{mol_id}.out', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'FINAL HEAT OF FORMATION' in line:
                    heat_of_formation = float(line.split()[-2])
                    break

        # Armazenar os resultados no dicionário
        results[method].append(heat_of_formation)

# Criar DataFrame do pandas
df = pd.DataFrame(results)
#print(df)

# Salvar DataFrame em um arquivo CSV
df.to_csv('heat_of_formation_results.csv', index=False)
