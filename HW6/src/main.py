import os
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


if __name__ == "__main__":
    # Get important parameters via arguments or console input
    file_path = ""
    args = sys.argv
    if len(args) < 2:
        file_path = input("Please provide the input file name: ")
    else:
        file_path = args[1]
    if len(args) < 3:
        delimiter = input("Please provide the separator used for the CSV-File: ")
    else:
        delimiter = args[2]
    if len(args) < 4:
        table_name = input("Please provide the Tablename used by the Database-File: ")
    else:
        table_name = args[3]

    start = time.time()

    # See if input exists and has valid format and create necessary output folders
    path = file_path
    if not os.path.isfile(path):
        print(f"File {path} could not be found")
    else:
        dir_name, file_suffix = os.path.splitext(file_path)
        valid_file_types = ['.csv', '.txt', '.json', '.db']
        if file_suffix not in valid_file_types:
            print(f"{file_suffix} is not a valid file type. Valid types are {valid_file_types}")
        else:
            info_file_path = os.path.join(dir_name, "information.txt")
            try:
                os.makedirs(dir_name)
                os.makedirs(os.path.join(dir_name, "out"))
                printToInfoFile(info_file_path, f"Directory '{dir_name}' created")
            except OSError as err:
                printToInfoFile(info_file_path, f"Directory '{dir_name}' already exists, contents will be overwritten")

            complete_file_path = os.path.join(os.getcwd(), file_path)
            os.chdir(dir_name)
            # Change info file path to current working directory
            info_file_path = "information.txt"
            input_file_path = os.path.join(os.getcwd(), file_path)

            try:
                shutil.copyfile(complete_file_path, input_file_path)
                printToInfoFile(info_file_path, f"Input file copied to folder")
            except IOError as err:
                printToInfoFile(info_file_path, f"Error copying input file: {err}")

            # Parsing input:
            try:
                printToInfoFile(info_file_path, f"Parsing input file")
                if file_suffix == '.csv' or file_suffix == '.txt':
                    data_frame = parseCsvFile(file_path, delimiter)
                elif file_suffix == '.db':
                    data_frame = parseDbFile(file_path, table_name)
                else:
                    data_frame = parseJsonFile(file_path)
            except ValueError as err:
                # Is raised if the Table does not exist in the DB-File
                printToInfoFile(info_file_path, err.args[0])
                # input file is invalid, exiting script
                print(f"Error, exiting script")
                sys.exit()
            except BaseException as exc:
                print(f"An unexpected error occurred, exiting script (see {info_file_path} for more information)")
                printToInfoFile(info_file_path, exc)
                sys.exit()

            # Writing output
            file_name = os.path.splitext(file_path)[0]
            for file_type in [x for x in valid_file_types if x != file_suffix]:
                out_file = os.path.join("out", file_name + file_type)
                printToInfoFile(info_file_path, f"Creating File '{out_file}'")
                try:
                    if file_type == '.csv' or file_type == '.txt':
                        data_frame.to_csv(out_file, delimiter, index=False)
                    elif file_type == '.db':
                        conn = sqlite3.connect(out_file)
                        try:
                            data_frame.to_sql(name=table_name, con=conn)
                        except ValueError as err:
                            # Table already exists, drop table and try again
                            c = conn.cursor()
                            c.execute(f"DROP TABLE {table_name}")
                            data_frame.to_sql(name=table_name, con=conn)
                    else:
                        data_frame.to_json(out_file, orient='records')
                except BaseException as exc:
                    print(f"An unexpected error occurred, exiting script (see {info_file_path} for more information)")
                    printToInfoFile(info_file_path, "[Error] " + exc.args.__str__())
                    sys.exit()

            end = time.time()

            printToInfoFile(info_file_path, f"Successfully converted {file_suffix}-File to other storage files")
            printToInfoFile(info_file_path, f"Found {len(data_frame)} rows")
            printToInfoFile(info_file_path, f"Found {len(data_frame.columns)} columns")
            printToInfoFile(info_file_path, f"Columns: {data_frame.columns}")
            printToInfoFile(info_file_path, f"Total time taken: {round(end - start, 3)} seconds")
