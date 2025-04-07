import sqlite3

try:
# Connect to the database (or create it if it doesn't exist)
    connection = sqlite3.connect('/teamspace/studios/this_studio/conv_analytics/database/chinook.db')
    cursor = connection.cursor()
    print("Database connection successful!")

    # Execute a simple query
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Table list: {tables}")
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
        formatted_output += "-" * (len(f"Table: {table_name}") ) + "\n"
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
    print(formatted_output)

except sqlite3.Error as error:
    print(f"Error occurred: {error}")

finally:
    if connection:
        connection.close()
    print("SQLite connection closed.")

