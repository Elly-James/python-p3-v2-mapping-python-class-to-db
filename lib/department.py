from __init__ import CURSOR, CONN


class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"


# Why are the create_table() and drop_table() methods class methods? Well, it is not the responsibility of an individual department object to create the table it will eventually be saved into, it is the job of the class as a whole.
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

# Editting the Department class to add methods to update and delete the database row associated an object that is an instance of the Department class:
    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()


# Notice the insert statement contains two question marks rather than string literals for the name and location values. We need to pass in, or interpolate, the name and location of a given Department object into our Python string that represents the SQL insert statement.

# We use something called bound parameters to achieve this.

# Important: using f-strings or the str.format() method will not work with statements sent through the sqlite3 module. sqlite3 will interpret any values interpolated in this fashion as columns. Weird

#Bound parameters protect our program from getting confused by SQL injectionsLinks to an external site. and special characters. Instead of interpolating variables into a Python string containing SQL syntax, we use the ? characters as placeholders. Then, the special magic provided to us by the sqlite3 module's Cursor.execute() method will take the values we pass in as an argument tuple (self.name, self.location) and apply them as the values of the question marks.

# We can step through this process by instantiating and saving objects that are instances of the Department class, printing the object state before and after saving to the database. Update debug.py as shown below, then execute python lib/debug.py to see the result of each print statement (make sure to exit out of ipdb with exit() or ctrl+D in order to reload the code if you left it open earlier).





    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid


        #Creating Instances vs. Creating Table Rows
# The moment in which we create a new object that is an instance of the Department class with the __init__ method is different than the moment in which we save a representation of that department object to our database.

# The __init__ method creates a new Python object, an instance of the Department class.
# The save() method takes the attributes that characterize the Python object and saves them in a new row in the database "departments" table.
# While it is possible to update the __init__ method to immediately save the object's attributes as a new table row, this is not a great idea. We don't want to force our objects to be saved every time they are created, or make the creation of an object dependent upon/always coupled with saving a row to the database. So, we'll keep our __init__ and save() methods separate, allowing the programmer to decide when each method should be called.

# The create() Method
# Method	Return	Description
# create(cls, attributes)	an object that is an instance of cls	Create a new object that is an instance of cls and save its attributes as a new table row.
# The save() method requires two steps to persist an object to the database:

# Create an object that is an instance of the Department class, then
# Call the save() method to insert a new row containing the object's attribute values to the database.
# Let's define a new class method named create() that does just that in one step. We use a class method because our object does not exist at the time the method is called.



    
    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department


# Here, we use arguments to pass a name and location into our create() method. We use that name and location to instantiate an object that is a new instance of the Department class. Then, we call the save() method to persist the new object's attributes to the database.

# Notice that at the end of the method, we are returning the Department object that we instantiated.

# Edit debug.py and let's use the create() method to instantiate and save the payroll and human resources departments:
