"""Create tables in database given sql scripts in folder"""

# pylint: disable=invalid-name

import os

import numpy as np
import pandas as pd


def insert_values(dummy_data_folder, conn, population_order, include_id):
    """Get CSV data from a folder and upload each CSV data to corresponding table in Postgres"""

    for table_name in population_order:
        file = os.path.join(dummy_data_folder, f"{table_name}.csv")

        print("TABLE:::", table_name)

        # Loading example to database:
        load_example(csv_path=file, table=table_name, conn=conn, include_id=include_id)


def load_example(csv_path, table, conn, include_id):
    """Receive csv path and upload data to Postgres"""

    csv_data = read_csv(csv_path)
    df = pd.DataFrame(csv_data)

    insert_dataframe(
        conn,
        df,
        table,
        drop_id=table not in include_id,  # for some tables, set drop_id = False
    )


def read_csv(path):
    """Read csv file"""

    with open(path, encoding="utf-8") as file:
        csv_data = pd.read_csv(file)

    return csv_data


def insert_dataframe(conn, df, table, drop_id=True):
    """Using cursor.executemany() to insert the dataframe"""

    cursor = conn.cursor()

    # Removing index from data (since ID is autogenerated by Postgres):
    if drop_id:
        df = df.drop("ID", axis=1)
        df = df.fillna(value="NULL")

    # Writing query string for values:
    insert_values_str = ""
    arr_data = df.to_numpy()
    for record in arr_data:
        insert_values_str += "("
        for element in record:
            if isinstance(element, str) and element != "NULL":
                insert_values_str += f"'{str(element)}',"
            elif element is None or np.isnan(element):
                insert_values_str += "NULL,"
            else:
                insert_values_str += f"{str(element)},"
        insert_values_str = insert_values_str.rstrip(",")
        insert_values_str += "),"
    insert_values_str = insert_values_str.rstrip(",")

    # Comma-separated dataframe columns:
    cols = ",".join(df.columns)

    # SQL query to insert data into database:
    query_insert = f"INSERT INTO {table} ({cols}) VALUES {insert_values_str}"
    print(query_insert, "\n")
    cursor.execute(query_insert)

    cursor.close()
