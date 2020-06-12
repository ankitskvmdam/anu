"""Pipeline to process raw apid data."""

import json
from os.path import abspath, basename, dirname, exists, join, realpath, splitext
from typing import List, Tuple

import click
from tqdm import tqdm
import vaex

from anu.data.data_operations import (
    extract_proteins_id_from_dataframe,
    fetch_pdb_using_uniprot_id,
)
from anu.data.dataframe_operation import (
    convert_csv_to_dataframe,
    read_dataframe_from_file,
    save_dataframe_to_file,
)


from multiprocessing import Pool, Process, Queue, freeze_support, cpu_count, Lock


def process_raw_csv_data(path: str, db_name: str, sep: str = "\t") -> None:
    """Process raw apid data.

    This function first read the raw data the save the dataframe
    to /data/processed/{db_name} folder

    Args:
        path: path or raw apid file relative to /data/raw folder.
        db_name: name of the database
    """
    df = convert_csv_to_dataframe(path)

    # Get file name from path by removing extension
    filename = splitext(basename(path))[0]

    filepath = join(db_name, filename)
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

    This will fetch pdb and also create 2 file in /data/processed.5
    First file will be list of ids whose pdb file fetched successfully,
    and second is the list of ids whose pdb file didn't fetched successfully.

    Also, this function assumes that dataframe only have two columns both of
    them have protein having uniprot id.

    Args:
        path: path of dataframe. path must be relative to /data/processed
        db_name: name of the database
    """
    import pathlib

    BASE_DATA_DIR = realpath(
        abspath(join(dirname(__file__), "..", "..", "..", "..", "data"))
    )

    base_path_for_pdb_files = join(BASE_DATA_DIR, "raw", "pdb")

    filename = splitext(basename(path))[0]

    base_path_for_processed_protein_id = join(
        BASE_DATA_DIR, "processed", "protein_id", db_name, filename
    )

    base_path_for_processed = join(BASE_DATA_DIR, "processed", "protein_id")

    # Creating path
    pathlib.Path(base_path_for_pdb_files).mkdir(exist_ok=True, parents=True)
    pathlib.Path(base_path_for_processed).mkdir(exist_ok=True, parents=True)
    pathlib.Path(base_path_for_processed_protein_id).mkdir(exist_ok=True, parents=True)

    try:
        # Load the dataframe
        df = read_dataframe_from_file(path)

        processed_protein_ids = {}
        protein_fetched_ok = {}
        protein_missing = {}
        pair_selected = {}

        for col_name in df.column_names:
            pair_selected[col_name] = []

        processed_protein_ids_file_path = join(
            base_path_for_processed, "processed.json"
        )
        protein_fetched_ok_file_path = join(base_path_for_processed, "fetched_ok.json")
        protein_missing_file_path = join(base_path_for_processed, "missing.json")
        pair_selected_path = join(
            base_path_for_processed_protein_id, "pair_selected.json"
        )

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
            current_id_log = tqdm(total=0, position=0, bar_format="{desc}")
            missing_log = tqdm(total=0, position=2, bar_format="{desc}")
            fetched_log = tqdm(total=0, position=3, bar_format="{desc}")
            processed_ok_log = tqdm(total=0, position=4, bar_format="{desc}")
            saving_log = tqdm(total=0, position=5, bar_format="{desc}")

            for index, row in tqdm(
                df.iterrows(), total=len(df), unit="files", position=1
            ):
                ids = list(row.values())
                flag = True

                for id in ids:
                    id = str.strip(id)
                    if id in protein_missing:
                        missing_log.set_description(
                            f"{id} is in missing list. Not processing this id."
                        )
                        flag = False
                        break
                if flag is False:
                    continue

                flag = True

                for id in ids:
                    id = str.strip(id)
                    current_id_log.set_description(
                        f"Currently downloading protein id is: {id}"
                    )

                    if id not in processed_protein_ids:
                        file, status = fetch_pdb_using_uniprot_id(id)
                        processed_protein_ids[id] = id

                        if status == 200:
                            fetched_log.set_description(
                                f"Protein id: {id} fetched successfully."
                            )
                            protein_fetched_ok[id] = id
                            pdb_file_location = join(
                                base_path_for_pdb_files, f"{id}.pdb"
                            )

                            with open(pdb_file_location, "w") as pdb:
                                pdb.write(file)

                        else:
                            missing_log.set_description(
                                f"Unable to download pdb file with uniport id: {id}. Moving {id} to missing list"
                            )
                            protein_missing[id] = id
                            flag = False
                    else:
                        fetched_log.set_description(f"{id} is already downloaded.")

                if flag is True:
                    processed_ok_log.set_description(
                        f"Moving pair [{str.strip(ids[0])}, {str.strip(ids[1])}] to pair selected list."
                    )
                    i = 0
                    for col_name in df.column_names:
                        pair_selected[col_name].append(str.strip(ids[i]))
                        i = i + 1

                if index % 100 == 0:
                    saving_log.set_description("Saving data. Please wait...")
                    path_list = [
                        (pair_selected_path, pair_selected),
                        (processed_protein_ids_file_path, processed_protein_ids),
                        (protein_fetched_ok_file_path, protein_fetched_ok),
                        (protein_missing_file_path, protein_missing),
                    ]

                    save_all_progess(path_list)

                    saving_log.set_description("Saving completed")

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

    except OSError:
        raise OSError

