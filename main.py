#!/usr/bin/env python3

import argparse
import sqlite3
import sys
import os
import shutil

def backup_database(db_file):
    # Create a backup of the database file
    base_name = os.path.splitext(db_file)[0]
    backup_file = f"{base_name}_backup.db"
    try:
        shutil.copyfile(db_file, backup_file)
        print(f"Backup created: '{backup_file}'")
    except IOError as e:
        print(f"An error occurred while creating the backup: {e}")
        sys.exit(1)

def add_field(db_file, table, field_name, data_type, init_value):
    backup_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Add the new column
    alter_table_sql = f"ALTER TABLE {table} ADD COLUMN {field_name} {data_type} DEFAULT {init_value};"
    try:
        cursor.execute(alter_table_sql)
        conn.commit()
        print(f"Field '{field_name}' added to table '{table}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    conn.close()

def delete_field(db_file, table, field_name):
    backup_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # SQLite does not support DROP COLUMN directly before version 3.35.0
    sqlite_version = sqlite3.sqlite_version_info
    if sqlite_version >= (3, 35, 0):
        alter_table_sql = f"ALTER TABLE {table} DROP COLUMN {field_name};"
        try:
            cursor.execute(alter_table_sql)
            conn.commit()
            print(f"Field '{field_name}' deleted from table '{table}'.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    else:
        print("SQLite version does not support DROP COLUMN. Please upgrade to version 3.35.0 or higher.")
    conn.close()

def update_one(db_file, table, field_name, record_id, value):
    backup_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    update_sql = f"UPDATE {table} SET {field_name} = ? WHERE id = ?;"
    try:
        cursor.execute(update_sql, (value, record_id))
        conn.commit()
        print(f"Record with id {record_id} updated in table '{table}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    conn.close()

def update_all(db_file, table, field_name, value):
    backup_database(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    update_sql = f"UPDATE {table} SET {field_name} = ?;"
    try:
        cursor.execute(update_sql, (value,))
        conn.commit()
        print(f"All records updated in table '{table}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='SQLite3 Database Field Modifier')
    parser.add_argument('--db', default='mlvt.db', help='Path to the SQLite database file (default: mlvt.db)')
    parser.add_argument('--action', required=True, choices=['add', 'delete', 'update_one', 'update_all'], help='Action to perform')
    parser.add_argument('--table', required=True, help='Table name')
    parser.add_argument('--field', required=True, help='Field (column) name')
    parser.add_argument('--type', help='Data type of the new field (for add action)')
    parser.add_argument('--init_value', help='Initial value of the new field (for add action)')
    parser.add_argument('--id', type=int, help='Record ID (for update_one action)')
    parser.add_argument('--value', help='Value to set (for update actions)')

    args = parser.parse_args()

    # Ensure the database file exists or create a new one
    if not os.path.exists(args.db):
        print(f"Database file '{args.db}' does not exist. Creating a new database.")
        open(args.db, 'w').close()

    if args.action == 'add':
        if not args.type or args.init_value is None:
            print("For 'add' action, --type and --init_value are required.")
            sys.exit(1)
        add_field(args.db, args.table, args.field, args.type, args.init_value)
    elif args.action == 'delete':
        delete_field(args.db, args.table, args.field)
    elif args.action == 'update_one':
        if args.id is None or args.value is None:
            print("For 'update_one' action, --id and --value are required.")
            sys.exit(1)
        update_one(args.db, args.table, args.field, args.id, args.value)
    elif args.action == 'update_all':
        if args.value is None:
            print("For 'update_all' action, --value is required.")
            sys.exit(1)
        update_all(args.db, args.table, args.field, args.value)
    else:
        print("Invalid action specified.")
        sys.exit(1)

if __name__ == '__main__':
    main()
