import os
import pathlib
import shutil
import sqlite3
import sys
import time
import pandas


def printToInfoFile(path: str, content: str):
    if os.path.isfile(path):
        read_file = open(path, 'r')
        file_content = read_file.read()
        if len(file_content) > 0:
            last_char = file_content[-1]
        else:
            last_char = '\n'
        read_file.close()
    else:
        last_char = '\n'

    file = open(path, 'a')
    if last_char == '\n' or last_char == '\r':
        file.write(content)
    else:
        file.write('\n' + content)
    file.close()


def parseCsvFile(path: str, delimiter: str) -> pandas.DataFrame:
    try:
        return pandas.read_csv(path, delimiter=delimiter)
    except BaseException as ex:
        raise ex


def parseDbFile(path: str, table_name: str) -> pandas.DataFrame:
    conn = sqlite3.connect(path)
    c = conn.cursor()

    all_tables = c.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name ='{table_name}'")
    if c.fetchone()[0] < 1:
        raise ValueError(f"Table name {table_name} could not be found in file {path}");

    data_frame = pandas.read_sql(f"select * from {table_name}", conn)
    conn.close()
    return data_frame


def parseJsonFile(path: str) -> pandas.DataFrame:
    try:
        return pandas.read_json(path, orient='records')
    except BaseException as ex:
        raise ex


def updateFile(file_path: str, content: pandas.DataFrame):
    path = pathlib.Path(file_path)
    file_name = path.name
    file_type = path.suffix
    try:
        if file_type == '.csv' or file_type == '.txt':
            content.to_csv(path, ";", index=False)
        elif file_type == '.db':
            conn = sqlite3.connect(path)
            try:
                content.to_sql(name=file_name, con=conn)
            except ValueError as err:
                # Table already exists, drop table and try again
                c = conn.cursor()
                c.execute(f"DROP TABLE {file_name}")
                content.to_sql(name=file_name, con=conn)
        else:
            content.to_json(path, orient='records')
    except BaseException as exc:
        print(f"Error updating file: {exc}")
        sys.exit()


def exportFiles(content: pandas.DataFrame, file_path: pathlib.Path, delimiter: str = ";", table_name: str = "Table"):
    dir_name, file_suffix = os.path.splitext(file_path)
    valid_file_types = ['.csv', '.txt', '.json', '.db']
    try:
        os.makedirs(dir_name)
        os.makedirs(os.path.join(dir_name, "out"))
    except OSError as err:
        print(f"Directory '{dir_name}' already exists, contents will be overwritten")

    # Writing output
    file_name = file_path.name
    for file_type in [x for x in valid_file_types if x != file_suffix]:
        out_file = os.path.join(dir_name, "out", file_name + file_type)
        try:
            if file_type == '.csv' or file_type == '.txt':
                content.to_csv(out_file, delimiter, index=False)
            elif file_type == '.db':
                conn = sqlite3.connect(out_file)
                try:
                    content.to_sql(name=table_name, con=conn)
                except ValueError as err:
                    # Table already exists, drop table and try again
                    c = conn.cursor()
                    c.execute(f"DROP TABLE {table_name}")
                    content.to_sql(name=table_name, con=conn)
            else:
                content.to_json(out_file, orient='records')
        except BaseException as exc:
            print("[Error] " + exc.args.__str__())
            sys.exit()

def convertFiles(file_path: str, delimiter: str, table_name: str):
    file_path = ""

    # See if input exists and has valid format and create necessary output folders
    path = file_path
    if not os.path.isfile(path):
        print(f"File {path} could not be found")
    else:
        dir_name, file_suffix = os.path.splitext(file_path)
        # Parsing input:
        try:
            if file_suffix == '.csv' or file_suffix == '.txt':
                data_frame = parseCsvFile(file_path, delimiter)
            elif file_suffix == '.db':
                data_frame = parseDbFile(file_path, table_name)
            else:
                data_frame = parseJsonFile(file_path)

            exportFiles(data_frame, path, delimiter, table_name)
        except ValueError as err:
            # input file is invalid, exiting script
            print(f"Error, exiting script")
            sys.exit()
        except BaseException as exc:
            print(f"An unexpected error occurred, exiting script")
            print(exc)
            sys.exit()


