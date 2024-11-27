# SQLite3 Database Field Modifier

This script allows you to add, update, or delete fields (columns) in an SQLite3 database using command-line arguments.

## Features

- **Add a Field**: Add a new column to an existing table with a specified data type and initial value.
- **Delete a Field**: Remove a column from a table (requires SQLite version 3.35.0 or higher).
- **Update One Record**: Update a specific field in a single record identified by its `id`.
- **Update All Records**: Update a specific field in all records of a table.

## Usage

### Running the Script

```bash
python main.py --action <action> --table <table_name> --field <field_name> [additional arguments] 
```

- <mark> --db </mark>: (Optional) Path to the SQLite database file. Defaults to mlvt.db.

## Actions and Required Arguments

**1. Add a Field**

```bash
python main.py --action add --table <table_name> --field <field_name> --type <data_type> --init_value <initial_value>
```

--type: Data type of the new field (e.g., TEXT, INTEGER, REAL).
--init_value: Initial value for the new field.
2. Delete a Field
``` python main.py --action delete --table <table_name> --field <field_name> ```

Note: Deleting a field requires SQLite version 3.35.0 or higher.

3. Update One Record
``` python main.py --action update_one --table <table_name> --field <field_name> --id <record_id> --value <new_value> ```

--id: The id of the record to update.
--value: New value for the field.
4. Update All Records
``` python main.py --action update_all --table <table_name> --field <field_name> --value <new_value> ```

--value: New value for the field.
Examples
Add a Field status to the transcriptions Table
``` python main.py --action add --table transcriptions --field status --type TEXT --init_value 'raw' ```

Update the status Field for a Specific Record
``` python main.py --action update_one --table transcriptions --field status --id 1 --value 'processed' ```

Update the status Field for All Records
``` python main.py --action update_all --table transcriptions --field status --value 'processed' ```

Delete the status Field from the transcriptions Table
``` python main.py --action delete --table transcriptions --field status ```

Notes
Database File: If the specified database file does not exist, the script will create it automatically.

Table Creation: Ensure that the table exists in the database before performing actions. You may need to create the table using SQLite commands if it doesn't exist.

SQLite Version: Deleting a field requires SQLite version 3.35.0 or higher. Check your SQLite version with:

``` python -c "import sqlite3; print(sqlite3.sqlite_version)" ```

Python Version: Make sure you're using Python 3.x.

Permissions: Ensure you have read and write permissions for the database file.

Data Types: Use standard SQLite data types when specifying the --type argument.

Troubleshooting
Table Not Found: If you receive an error about a missing table, verify that the table exists in the database.
Field Already Exists: Attempting to add a field that already exists will result in an error.
SQLite Errors: Any SQLite errors encountered during execution will be printed to the console for debugging.
License
This project is licensed under the MIT License.