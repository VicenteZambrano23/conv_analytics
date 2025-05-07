import sqlite3
from config.config import db_path

def get_sql_tables():

    """
    Retrieves and formats the schema of a SQLite database located at 
    '/teamspace/studios/this_studio/conv_analytics/database/chinook.db'.

    This function connects to the specified SQLite database, queries the database
    to get a list of tables, and then retrieves detailed information about each table,
    including column names, data types, constraints (NOT NULL, DEFAULT, PRIMARY KEY),
    and foreign key relationships.

    The schema information is then formatted into a human-readable string,
    which includes the table names, column definitions, and foreign key constraints.

    Returns:
        str: A formatted string describing the schema of the SQLite database.
             Returns an empty string or an error message if an error occurs.
    """
    try:
        prompt_path_1 = '/teamspace/studios/this_studio/conv_analytics/prompts/query_agent_prompt.txt'
        prompt_path_2 = '/teamspace/studios/this_studio/conv_analytics/prompts/graph_agent_prompt.txt'


        with open(prompt_path_1, 'r') as file:
            lines = file.readlines()

        if len(lines) >= 21:
            with open(prompt_path_1, 'w') as file:
                file.writelines(lines[:21])  # Write only the first three lines
            print(f"Lines after the third line deleted from '{prompt_path_1}'.")
        else:
            print(f"File '{prompt_path_1}' has less than 4 lines. No lines deleted.")
        
        with open(prompt_path_2, 'r') as file:
            lines = file.readlines()

        if len(lines) >= 100:
            with open(prompt_path_2, 'w') as file:
                file.writelines(lines[:85])  # Write only the first three lines
            print(f"Lines after the third line deleted from '{prompt_path_2}'.")
        else:
            print(f"File '{prompt_path_2}' has less than 4 lines. No lines deleted.")
            
# Connect to the database (or create it if it doesn't exist)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print("Database connection successful!")

        # Execute a simple query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        schema = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            schema[table] = columns
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            foreign_keys = cursor.fetchall()
            schema[table].append(("foreign_keys", foreign_keys))

        formatted_output = ""
        for table_name, columns_and_fk in schema.items():
            formatted_output += f"Table: {table_name}\n"
            formatted_output = formatted_output + ("-" * (len(f"Table: {table_name}") ) + "\n")
            foreign_keys = [] #initialize the foreign keys list for this table.
            for column in columns_and_fk:
                if(column[0] == "foreign_keys"):
                    foreign_keys = column[1]
                    continue #skip the foreign key tuple.
                cid, name, type_, notnull, dflt_value, pk = column
                formatted_output += f"  {name} {type_}"
                if notnull:
                    formatted_output += " NOT NULL"
                if dflt_value is not None:
                    formatted_output += f" DEFAULT {dflt_value}"
                if pk:
                    formatted_output += " PRIMARY KEY"
                formatted_output += "\n"

            if foreign_keys:
                formatted_output += "\n  Foreign Keys:\n"
                for fk in foreign_keys:
                    id_, seq, table_, from_, to_, on_update, on_delete, match = fk
                    formatted_output += f"    {from_} -> {table_}({to_}) ON UPDATE {on_update} ON DELETE {on_delete}\n"

            formatted_output += "\n"

        with open(prompt_path_1, 'a') as file:  # 'a' mode for appending
            file.write(formatted_output)
        
        with open(prompt_path_2, 'a') as file:  # 'a' mode for appending
            file.write(formatted_output)
        

        return 
    except sqlite3.Error as error:
        print(f"Error occurred: {error}")

    finally:
        if connection:
            connection.close()
        print("SQLite connection closed.")
