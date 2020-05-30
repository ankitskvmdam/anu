"""Pipeline to process raw apid data."""

import json
from os.path import basename, exists, join, realpath, splitext
from typing import List, Tuple

import vaex

from anu.data.data_operations import (
    extract_proteins_id_from_dataframe,
    fetch_pdb_using_uniprot_id,
)
from anu.data.dataframe_operation import (
    convert_apid_to_dataframe,
    read_dataframe_from_file,
    save_dataframe_to_file,
)


def process_raw_apid_data(path: str) -> None:
    """Process raw apid data.

    This function first read the raw data the save the dataframe
    to /data/processed/apid folder

    Args:
        path: path or raw apid file relative to /data/raw folder.
    """
    df = convert_apid_to_dataframe(path)

    # Get file name from path by removing extension
    filename = splitext(basename(path))[0]

    filepath = join("apid", filename)
    save_dataframe_to_file(df, filepath)


def extract_protein_id_from_df_and_save(
    path: str, db_name: str, first_col_name: str, second_col_name: str
) -> None:
    """Extract protein id from dataframe and then save.

    Save protein id dataframe to /data/processed/protein_id_dataframes.
    Don't include extension of file.

    Args:
        path: path of dataframe. path must be relative to /data/processed
        db_name: name of the database
        first_col_name: name of the first col where we get the protein id.
        second_col_name: name of the second col where we get the protein id.
    """
    df = extract_proteins_id_from_dataframe(
        read_dataframe_from_file(path), first_col_name, second_col_name
    )
    filename = f"{basename(path)}"
    filepath = join("protein_dataframes", db_name, filename)
    save_dataframe_to_file(df, filepath)


def save_all_progess(path_list: List[Tuple[str, dict]]) -> None:
    """Save the progress of fetch_pdb_from_df.

    Args:
        path_list: list of tuples. each tuple contains path and content
    """
    for item in path_list:
        with open(item[0], "w") as file:
            json.dump(item[1], file)


def fetch_pdb_from_df(path: str, db_name: str) -> None:
    """Fetch pdb file using df.

    This will fetch pdb and also create 2 file in /data/processed.
    First file will be list of ids whose pdb file fetched successfully,
    and second is the list of ids whose pdb file didn't fetched successfully.

    Also, this function assumes that dataframe only have two columns both of
    them have protein having uniprot id.

    Args:
        path: path of dataframe. path must be relative to /data/processed
        db_name: name of the database
    """
    import pathlib

    base_path_for_pdb_files = realpath(
        join("..", "..", "..", "data", "raw", "pdb", f"from_{db_name}")
    )

    filename = splitext(basename(path))[0]

    base_path_for_processed_protein_id = realpath(
        join("..", "..", "..", "data", "processed", "protein_id", db_name, filename)
    )

    # Creating path
    pathlib.Path(base_path_for_pdb_files).mkdir(exist_ok=True, parents=True)
    pathlib.Path(base_path_for_processed_protein_id).mkdir(exist_ok=True, parents=True)

    # Load the dataframe
    df = read_dataframe_from_file(path)

    processed_protein_ids = {}
    protein_fetched_ok = {}
    protein_missing = {}
    pair_selected = {}

    for col_name in df.column_names:
        pair_selected[col_name] = []

    processed_protein_ids_file_path = join(
        base_path_for_processed_protein_id, "processed.json"
    )
    protein_fetched_ok_file_path = join(
        base_path_for_processed_protein_id, "fetched_ok.json"
    )
    protein_missing_file_path = join(base_path_for_processed_protein_id, "missing.json")
    pair_selected_path = join(base_path_for_processed_protein_id, "pair_selected.json")

    # check if we have a file containing list of processed protein id
    if exists(processed_protein_ids_file_path):
        with open(processed_protein_ids_file_path) as file:
            processed_protein_ids = json.load(file)

    # check if we have a file containing list of protein fetched successfully.
    if exists(protein_fetched_ok_file_path):
        with open(protein_fetched_ok_file_path) as file:
            protein_fetched_ok = json.load(file)

    # check if we have a file containing list of protein missing pdb.
    if exists(protein_missing_file_path):
        with open(protein_missing_file_path) as file:
            protein_missing = json.load(file)

    # check if we have a file containing list of protein missing pdb.
    if exists(pair_selected_path):
        with open(pair_selected_path) as file:
            pair_selected = json.load(file)

    try:
        for index, row in df.iterrows():

            ids = list(row.values())
            flag = True

            for id in ids:
                if id in protein_missing:
                    print(f"{id} is in missing list. So it is not processing.")
                    flag = False
                    break
            if flag is False:
                continue

            flag = True

            for id in ids:

                print(f"Row: {index}, Protein id: {id}")

                if id not in processed_protein_ids:
                    file, status = fetch_pdb_using_uniprot_id(id)
                    processed_protein_ids[id] = id

                    if status == 200:
                        print(
                            f"{id} fetched successfully. Moving it to fetched ok list"
                        )
                        protein_fetched_ok[id] = id
                        pdb_file_location = join(base_path_for_pdb_files, f"{id}.pdb")

                        with open(pdb_file_location, "w") as pdb:
                            pdb.write(file)

                    else:
                        print(f"{id} is missing. Moving {id} to missing list")
                        protein_missing[id] = id
                        flag = False

            if flag is True:
                print(f"Moving pair {ids} to pair selected list.")
                i = 0
                for col_name in df.column_names:
                    pair_selected[col_name].append(ids[i])
                    i = i + 1

            if index % 100 == 0:
                print("Saving data. Please wait...")
                path_list = [
                    (pair_selected_path, pair_selected),
                    (processed_protein_ids_file_path, processed_protein_ids),
                    (protein_fetched_ok_file_path, protein_fetched_ok),
                    (protein_missing_file_path, protein_missing),
                ]

                save_all_progess(path_list)

                print("Saving completed")

        print("All completed. Saving data. Please wait...")
        path_list = [
            (pair_selected_path, pair_selected),
            (processed_protein_ids_file_path, processed_protein_ids),
            (protein_fetched_ok_file_path, protein_fetched_ok),
            (protein_missing_file_path, protein_missing),
        ]

        save_all_progess(path_list)

        print("Saving completed")

        final_df = vaex.from_dict(pair_selected)
        file_path = join("final_protein_dataframes", db_name, filename)
        save_dataframe_to_file(final_df, file_path)

    except KeyboardInterrupt:

        print("Saving data. Please wait...")
        path_list = [
            (pair_selected_path, pair_selected),
            (processed_protein_ids_file_path, processed_protein_ids),
            (protein_fetched_ok_file_path, protein_fetched_ok),
            (protein_missing_file_path, protein_missing),
        ]

        save_all_progess(path_list)

        print("Saving completed")


fetch_pdb_from_df(join("protein_dataframes", "apid", "3702_Q3"), "apid")
