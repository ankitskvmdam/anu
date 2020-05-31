"""Functions responsible for preparing input."""

import os
from statistics import mean

from Bio.PDB import PDBParser, Polypeptide
import vaex

from anu.constants.amino_acid import amino_acid


def build_matrix(path: str, filename: str) -> vaex.dataframe.DataFrame:
    """Build the input matrix for one protein.

    Args:
        path: path of the pdb file.
        filename: name of the file (without extension).

    Returns:
        vaex dataframe
    """
    PROTEIN_SEQ_MAX_LEN = 2000
    protein_matrix = [[0 for x in range(PROTEIN_SEQ_MAX_LEN)] for y in range(10)]
    protein_structure = PDBParser().get_structure(filename, path)
    protein_model = list(protein_structure.get_models())
    protein_chains = list(protein_model[0].get_chains())

    col = 0
    for chain in protein_chains:
        protein_residues = list(chain.get_residues())

        for residue in protein_residues:
            atoms = list(residue.get_atoms())
            x = []
            y = []
            z = []

            for atom in atoms:
                vec = atom.get_vector()
                x.append(vec.__getitem__(0))
                y.append(vec.__getitem__(1))
                z.append(vec.__getitem__(2))

            # calculate position of residue
            x = mean(x)
            y = mean(y)
            z = mean(z)

            # one letter code
            code = Polypeptide.three_to_one(residue.get_resname())

            aa = amino_acid[code]

            protein_matrix[0][col] = aa["code"]
            protein_matrix[1][col] = x
            protein_matrix[2][col] = y
            protein_matrix[3][col] = z
            protein_matrix[4][col] = aa["hydropathy"]
            protein_matrix[5][col] = aa["hydropathy_index"]
            protein_matrix[6][col] = aa["acidity_basicity"]
            protein_matrix[7][col] = aa["mass"]
            protein_matrix[8][col] = aa["isoelectric_point"]
            protein_matrix[9][col] = aa["charge"]

            col = col + 1

    # Prepare dict so it can be load to vaex dataframe
    dic = {}

    for i in range(PROTEIN_SEQ_MAX_LEN):
        dic[f"Seq {i}"] = [protein_matrix[x][i] for x in range(10)]

    df = vaex.from_dict(dic)
    return df


path = os.path.relpath(
    os.path.join("..", "..", "..", "data", "raw", "pdb", "from_apid", "A0A1I9LP65.pdb")
)
df = build_matrix(path, "A0A1I9LP65")

print(df)
