import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills', 'feedback', 'users']
        
        # NEW IN HW 3 - Encryption configuration
        self.encryption     = {
            'oneway': {
                'salt': b'averysaltysailortookalongwalkoffashortbridge',
                'n': int(pow(2,5)),
                'r': 9,
                'p': 1
            },
            'reversible': {
                'key': '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='
            }
        }

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row
    

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info


    def createTables(self, purge=False, data_path='flask_app/database/'):
        """Create all tables and populate w/ initial data (FROM HW2)"""
        print('Creating and populating database tables...')
        
        # If purge is True, drop all existing tables first
        if purge:
            print('Purging existing tables...')
            # Drop tables in reverse order to avoid foreign key constraints
            self.query("SET FOREIGN_KEY_CHECKS = 0")
            for table in self.tables[::-1]:
                self.query(f"DROP TABLE IF EXISTS {table}")
            self.query("SET FOREIGN_KEY_CHECKS = 1")
        
        # Create tables in order (dependencies first)
        for table in self.tables:
            sql_file = data_path + f'create_tables/{table}.sql'
            print(f'Creating table from {sql_file}...')
            
            try:
                with open(sql_file, 'r') as f:
                    sql_statement = f.read()
                    self.query(sql_statement)
                print(f'  ✓ Table {table} created successfully')
            except FileNotFoundError:
                print(f'  ⚠ Warning: {sql_file} not found, skipping...')
            except Exception as e:
                print(f'  ✗ Error creating table {table}: {e}')
        
        # Populate tables w/ initial data (skip users table - created programmatically)
        for table in self.tables:
            if table == 'users':
                print(f'Skipping initial data for {table} (will be created by createUser)')
                continue
                
            csv_file = data_path + f'initial_data/{table}.csv'
            
            try:
                print(f'Populating table {table} from {csv_file}...')
                
                # Read CSV file
                with open(csv_file, 'r') as f:
                    csv_reader = csv.DictReader(f)
                    
                    # Get column names from CSV header
                    columns = csv_reader.fieldnames
                    
                    # Collect all rows
                    rows = []
                    for row in csv_reader:
                        # Convert 'NULL' strings to None
                        row_values = [None if value == 'NULL' else value for value in row.values()]
                        rows.append(row_values)
                    
                    # Insert all rows at once
                    if rows:
                        self.insertRows(table=table, columns=columns, parameters=rows)
                        print(f'  ✓ Inserted {len(rows)} rows into {table}')
                    else:
                        print(f'  ⚠ No data to insert into {table}')
            
            except FileNotFoundError:
                print(f'  ⚠ Warning: {csv_file} not found, skipping...')
            except Exception as e:
                print(f'  ✗ Error populating table {table}: {e}')
        
        print('Database tables created and populated successfully!')


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        """Insert multiple rows into a table (FROM HW2)"""
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query, parameters)[0]['LAST_INSERT_ID()']         
        return insert_id


    def getResumeData(self):
        """Query database and return nested dictionary of resume data (FROM HW2)"""
        print('Fetching resume data from database...')
        
        resume_data = {}
        
        institutions = self.query("SELECT * FROM institutions ORDER BY inst_id")
        
        for inst in institutions:
            inst_id = inst['inst_id']
            
            # Add institution data to result
            resume_data[inst_id] = {
                'inst_id': inst['inst_id'],
                'type': inst['type'],
                'name': inst['name'],
                'department': inst['department'],
                'address': inst['address'],
                'city': inst['city'],
                'state': inst['state'],
                'zip': inst['zip'],
                'positions': {}
            }
            
            # Get all positions for this institution
            positions = self.query(
                "SELECT * FROM positions WHERE inst_id = %s ORDER BY start_date DESC",
                parameters=[inst_id]
            )
            
            for pos in positions:
                position_id = pos['position_id']
                
                # Add position data
                resume_data[inst_id]['positions'][position_id] = {
                    'position_id': pos['position_id'],
                    'title': pos['title'],
                    'responsibilities': pos['responsibilities'],
                    'start_date': pos['start_date'],
                    'end_date': pos['end_date'],
                    'experiences': {}
                }
                
                # Get all experiences for this position
                experiences = self.query(
                    "SELECT * FROM experiences WHERE position_id = %s ORDER BY start_date DESC",
                    parameters=[position_id]
                )
                
                for exp in experiences:
                    experience_id = exp['experience_id']
                    
                    # Add experience data
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id] = {
                        'experience_id': exp['experience_id'],
                        'name': exp['name'],
                        'description': exp['description'],
                        'hyperlink': exp['hyperlink'],
                        'start_date': exp['start_date'],
                        'end_date': exp['end_date'],
                        'skills': {}
                    }
                    
                    # Get all skills for this experience
                    skills = self.query(
                        "SELECT * FROM skills WHERE experience_id = %s ORDER BY skill_level DESC",
                        parameters=[experience_id]
                    )
                    
                    for skill in skills:
                        skill_id = skill['skill_id']
                        
                        # Add skill data
                        resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = {
                            'skill_id': skill['skill_id'],
                            'name': skill['name'],
                            'skill_level': skill['skill_level']
                        }
        
        print('Resume data fetched successfully!')
        return resume_data


#######################################################################################
# AUTHENTICATION RELATED (NEW IN HW3)
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        """
        Create a new user in the database with encrypted password.
        Only creates user if email doesn't already exist.
        Returns success status.
        """
        # Check if user already exists
        check_query = "SELECT * FROM users WHERE email = %s"
        existing_user = self.query(check_query, parameters=[email])
        
        if existing_user:
            print(f'User {email} already exists')
            return {'success': 0, 'message': 'User already exists'}
        
        # Encrypt the password using one-way encryption
        encrypted_password = self.onewayEncrypt(password)
        
        # Insert the new user
        insert_query = """
            INSERT INTO users (email, password, role) 
            VALUES (%s, %s, %s)
        """
        
        try:
            self.query(insert_query, parameters=[email, encrypted_password, role])
            print(f'User {email} created successfully with role: {role}')
            return {'success': 1, 'message': 'User created successfully'}
        except Exception as e:
            print(f'Error creating user {email}: {e}')
            return {'success': 0, 'message': str(e)}


    def authenticate(self, email='me@email.com', password='password'):
        """
        Authenticate a user by checking email and encrypted password.
        Returns True if authentication succeeds, False otherwise.
        """
        # Encrypt the provided password
        encrypted_password = self.onewayEncrypt(password)
        
        # Query for user with matching email and encrypted password
        auth_query = """
            SELECT * FROM users 
            WHERE email = %s AND password = %s
        """
        
        result = self.query(auth_query, parameters=[email, encrypted_password])
        
        if result:
            print(f'Authentication successful for {email}')
            return True
        else:
            print(f'Authentication failed for {email}')
            return False


    def onewayEncrypt(self, string):
        """
        One-way encryption using scrypt for password hashing.
        This is irreversible - used for storing passwords securely.
        """
        encrypted_string = hashlib.scrypt(
            string.encode('utf-8'),
            salt = self.encryption['oneway']['salt'],
            n    = self.encryption['oneway']['n'],
            r    = self.encryption['oneway']['r'],
            p    = self.encryption['oneway']['p']
        ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        """
        Reversible encryption using Fernet for session data.
        type: 'encrypt' or 'decrypt'
        message: string to encrypt/decrypt
        """
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message