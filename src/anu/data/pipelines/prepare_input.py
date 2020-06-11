"""Functions responsible for preparing input."""

import os
from statistics import mean
from typing import List, TypedDict

from Bio.PDB import PDBParser, Polypeptide
import pyarrow

import vaex


from anu.constants.amino_acid import amino_acid
from anu.data.dataframe_operation import (
    save_dataframe_to_file,
    read_dataframe_from_file,
)


# Dictionary keys
col_name = [
    "seq",
    "x_pos",
    "y_pos",
    "z_pos",
    "hydropathy",
    "hydropathy_index",
    "acidity_basicity",
    "mass",
    "isoelectric_point",
    "charge",
]


class BuildMatrixDict(TypedDict):
    """Dictionary shape for build matrix class."""

    seq: List[List[int]]
    x_pos: List[List[int]]
    y_pos: List[List[int]]
    z_pos: List[List[int]]
    hydropathy: List[List[int]]
    hydropathy_index: List[List[int]]
    acidity_basicity: List[List[int]]
    mass: List[List[int]]
    isoelectric_point: List[List[int]]
    charge: List[List[int]]


def build_matrix(path: str, filename: str) -> BuildMatrixDict:
    """Build the input matrix for one protein.

    Args:
        path: path of the pdb file.
        filename: name of the file (without extension).

    Returns:
        Build matrix dictionary
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
            if Polypeptide.is_aa(residue.get_resname()):
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
                x = round(mean(x))
                y = round(mean(y))
                z = round(mean(z))

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
    dic: BuildMatrixDict = {
        "seq": [[]],
        "x_pos": [[]],
        "y_pos": [[]],
        "z_pos": [[]],
        "hydropathy": [[]],
        "hydropathy_index": [[]],
        "acidity_basicity": [[]],
        "mass": [[]],
        "isoelectric_point": [[]],
        "charge": [[]],
    }

    for i in range(10):
        dic[col_name[i]] = pyarrow.array(
            [[protein_matrix[i][x] for x in range(PROTEIN_SEQ_MAX_LEN)]]
        )

    return dic


def build_df_from_dic(
    protein_a: BuildMatrixDict, protein_b: BuildMatrixDict, interaction_type: bool
) -> vaex.dataframe.DataFrame:
    """Build dataframe using protein dict.

    Args:
        protein_a: Protein A in the form of BuildMatrixDict.
        protein_b: Protein B in the form of BuildMatrixDict.

    Returns:
        vaex dataframe.
    """
    interaction_array = (
        pyarrow.array([[1, 0]]) if interaction_type else pyarrow.array([[0, 1]])
    )

    return vaex.from_arrays(
        proteinA_seq=protein_a[col_name[0]],
        proteinB_seq=protein_b[col_name[0]],
        proteinA_x=protein_a[col_name[1]],
        proteinB_x=protein_b[col_name[1]],
        proteinA_y=protein_a[col_name[2]],
        proteinB_y=protein_b[col_name[2]],
        proteinA_z=protein_a[col_name[3]],
        proteinB_z=protein_b[col_name[3]],
        proteinA_hydropathy=protein_a[col_name[4]],
        proteinB_hydropathy=protein_b[col_name[4]],
        proteinA_hydropathy_index=protein_a[col_name[5]],
        proteinB_hydropathy_index=protein_b[col_name[5]],
        proteinA_acidity_basicity=protein_a[col_name[6]],
        proteinB_acidity_basicity=protein_b[col_name[6]],
        proteinA_mass=protein_a[col_name[7]],
        proteinB_mass=protein_b[col_name[7]],
        proteinA_isoelectric_point=protein_a[col_name[8]],
        proteinB_isoelectric_point=protein_b[col_name[8]],
        proteinA_charge=protein_a[col_name[9]],
        proteinB_charge=protein_b[col_name[9]],
        interaction=interaction_array,
    )


# print("Loading first file")

# path = os.path.relpath(
#     os.path.abspath(
#         os.path.join("..", "..", "..", "data", "raw", "pdb", "A0A178U6H4.pdb")
#     )
# )
# protein_a = build_matrix(path, "A0A178U6H4")

# print("Loading second file")

# path = os.path.relpath(
#     os.path.abspath(os.path.join("..", "..", "..", "data", "raw", "pdb", "Q9AT76.pdb"))
# )
# protein_b = build_matrix(path, "Q9AT76")

# final_df = build_df_from_dic(protein_a, protein_b, True)
# new_df = build_df_from_dic(protein_b, protein_a, False)

# print("Loading complete")

# final_df = vaex.concat([final_df, new_df, final_df])

# print("saving to file")

# path = os.path.join("test", "test_1")
# save_dataframe_to_file(final_df, path)

# print(final_df)

# print("Completed successfully")

df = read_dataframe_from_file("test/test_1")

print(df)
