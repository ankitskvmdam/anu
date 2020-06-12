"""Functions responsible for preparing input."""

import os
from statistics import mean
from typing import List, Tuple, TypedDict

from Bio.PDB import PDBParser, Polypeptide
import pyarrow
import tqdm
import vaex

from anu.constants.amino_acid import amino_acid
from anu.data.dataframe_operation import (
    save_dataframe_to_file,
    read_dataframes_from_file,
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


def build_matrix(path: str, filename: str, truncate_log: tqdm.tqdm) -> BuildMatrixDict:
    """Build the input matrix for one protein.

    Args:
        path: path of the pdb file.
        filename: name of the file (without extension).
        truncate_log: tqdm logger

    Returns:
        Build matrix dictionary
    """
    PROTEIN_SEQ_MAX_LEN = 4000
    protein_matrix = [[0 for x in range(PROTEIN_SEQ_MAX_LEN)] for y in range(10)]
    protein_structure = PDBParser().get_structure(filename, path)
    protein_model = list(protein_structure.get_models())
    protein_chains = list(protein_model[0].get_chains())

    col = 0

    try:
        for chain in protein_chains:
            protein_residues = list(chain.get_residues())

            for residue in protein_residues:
                if Polypeptide.is_aa(residue.get_resname(), standard=True):
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

                # Even if the current residue is not amino acid we increase the col.
                # 0 is save at this position if it is not an amino acid.
                col = col + 1

    except IndexError:
        truncate_log.set_description(
            f"Protein {filename} is truncated. Because its size exceeds {PROTEIN_SEQ_MAX_LEN}"
        )

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


def save_build_df(
    list_of_logs: List[tqdm.tqdm], prev_path: str, save_path: str
) -> None:
    """Saving progress of build input from json.
    
    Args:
        list_of_logs: list of tqdm logs.
        prev_path: path of last saved df.
        save_path: path to save new df.
    """

    for logger in list_of_logs:
        logger.close()

    df = read_dataframes_from_file(prev_path)
    save_dataframe_to_file(df, save_path)


def build_input_from_json_intermediate_step(
    protein_a: str,
    protein_b: str,
    pdb_file_path: str,
    current_log: tqdm.tqdm,
    truncate_log: tqdm.tqdm,
    interaction_type: bool,
) -> vaex.dataframe:
    """Intermediate step for build input from json.
    
    Args:
        protein_a: first protein id.
        protein_b: second protein id.
        pdb_file_path: root location of pdb files.
        current_log: tqdm logger for current status.
        truncate_log: tqdm logger for truncate status.
        interaction_type: interaction status of both protein

    Returns:
        vaex dataframe.
    """
    current_log.set_description(f"Processing  [{protein_a}, {protein_b}]")
    a = build_matrix(
        os.path.join(pdb_file_path, f"{protein_a}.pdb"), protein_a, truncate_log
    )
    b = build_matrix(
        os.path.join(pdb_file_path, f"{protein_b}.pdb"), protein_b, truncate_log
    )

    return build_df_from_dic(a, b, interaction_type)


def get_proteins_list_from_json(file_path: str) -> Tuple[List[str], List[str]]:
    """Get proteins list from json.
    
    Args:
        file_path: path of the json file.

    Returns:
        Tuple of protein list.
    """
    import json

    protein_json = {}

    with open(file_path) as fp:
        protein_json = json.load(fp)

    protein_list = []

    for _, value in protein_json.items():
        protein_list.append(value)

    return protein_list[0], protein_list[1]


def build_input_from_json(
    path: str, db_name: str, filename: str, interaction_type: bool
) -> None:
    """Build input from json file.

    Args:
        path: path of json file.
        db_name: name of the database.
        filename: name of the output file containing df.
    """
    import os, warnings

    warnings.simplefilter("ignore")
    BASE_DATA_DIR = os.path.realpath(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data")
        )
    )

    file_path = os.path.join(BASE_DATA_DIR, "processed", "protein_id", path)
    pdb_file_path = os.path.join(BASE_DATA_DIR, "raw", "pdb")

    protein_list_a, protein_list_b = get_proteins_list_from_json(file_path)

    total = min(len(protein_list_a), len(protein_list_b))

    current_log = tqdm.tqdm(total=0, position=1, bar_format="{desc}", leave=False)
    truncate_log = tqdm.tqdm(total=0, position=2, bar_format="{desc}", leave=False)

    loggers = [current_log, truncate_log]
    input_path = os.path.join("input", db_name, filename)

    prev_df_path = os.path.join("input", db_name, f"{filename}_prev_df")
    current_df_path = os.path.join("input", db_name, f"{filename}_cur_df")
    save_df_path = os.path.join("input", db_name, filename)

    row_already_processed_path = os.path.join(
        BASE_DATA_DIR, "input", db_name, f"{filename}_processed_row.txt"
    )
    start = 0

    if os.path.exists(row_already_processed_path):
        file_pointer = open(row_already_processed_path, "w")
        start = int(file_pointer.read())

    else:
        file_pointer = open(row_already_processed_path, "w")

    try:
        progress_log = tqdm.tqdm(total=total, position=0, leave=False)
        progress_log.update(start)
        loggers.append(progress_log)
        df = build_input_from_json_intermediate_step(
            protein_list_a[start],
            protein_list_b[start],
            pdb_file_path,
            current_log,
            truncate_log,
            interaction_type,
        )

        save_dataframe_to_file(df, prev_df_path)

        for i in range(start + 1, total):
            df = build_input_from_json_intermediate_step(
                protein_list_a[i],
                protein_list_b[i],
                pdb_file_path,
                current_log,
                truncate_log,
                interaction_type,
            )

            save_dataframe_to_file(df, current_df_path)
            df = vaex.open_many([prev_df_path, current_df_path])
            save_dataframe_to_file(df, prev_df_path)
            progress_log.update(1)

        print("Completed...")
        save_build_df(loggers, prev_df_path, save_df_path)

    except KeyboardInterrupt:
        save_build_df(loggers, prev_df_path, save_df_path)


build_input_from_json(
    "pickle/interacting-protein/pair_selected.json", "pickle", "pickle_input_df", True
)
