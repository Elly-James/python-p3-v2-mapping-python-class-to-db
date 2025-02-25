#!/usr/bin/env python3
#lib/testing/debug.py





#In this file, we're importing in the sqlite3.Connection and sqlite3.
# Cursor objects that we instantiated in lib/__init__.py.
#  We're also importing the Department class so that we can use its methods during our ipdb session.

# Run python debug.py to enter the ipdb session:

# python lib/debug.py
# then run the create_table() class method:

# ipdb>  Department.create_table()


# Creating a table doesn't return any data, so SQLite returns None. If you'd like to confirm that the table was created successfully, you can run a special PRAGMA command to show the information about the departments table:

# ipdb>  CURSOR.execute("PRAGMA table_info(departments)").fetchall()
# # => [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'location', 'TEXT', 0, None, 0)]
# The output isn't easy to read, but you'll see the column names (id, name, location) along with their data types (INTEGER, TEXT, TEXT).



from __init__ import CONN, CURSOR
from department import Department

import ipdb

Department.drop_table()
Department.create_table()
payroll = Department.create("Payroll", "Building A, 5th Floor")
print(payroll)  # <Department 1: Payroll, Building A, 5th Floor>

hr = Department.create("Human Resources", "Building C, East Wing")
print(hr)  # <Department 2: Human Resources, Building C, East Wing>

hr.name = 'HR'
hr.location = "Building F, 10th Floor"
hr.update()
print(hr)  # <Department 2: HR, Building F, 10th Floor>

print("Delete Payroll")
payroll.delete()  # delete from db table, object still exists in memory
print(payroll)  # <Department 1: Payroll, Building A, 5th Floor>

ipdb.set_trace()

# Prior to calling the save() method, the print statement shows the newly instantiated Department object's id attribute initially has the value of None.
# After the save method is executed, the print statement shows the Department object's id attribute has been updated to contain an integer value corresponding to the primary key of the new table row.
# The save() method does not return a value, but we can query the database table and create a list from the result.

# Execute this code by entering one statement at a time to the ipbd> prompt:

# ipdb> departments = CURSOR.execute('SELECT * FROM departments')
# ipdb> [row for row in departments]
# # => [(1, 'Payroll', 'Building A, 5th Floor'), (2, 'Human Resources', 'Building C, East Wing')]




# lastly
# You can use the SQLITE EXPLORER extension to confirm the table contents, or use ipdb to query the table and confirm the updated/deleted table rows. Enter the following statements one at a time at the ipbd> prompt.

# ipdb> departments = CURSOR.execute('SELECT * FROM departments')
# ipdb> [row for row in departments]
# # => [(2, 'HR', 'Building F, 10th Floor')]
# Try to use the ipdb session to experiment with creating/updating/deleting additional Department objects in the database.

