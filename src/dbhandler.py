import sqlite3, datetime, os, subprocess

def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if not os.path.exists(db_file):
        folder_path = os.getcwd()  # Get the current working directory path
        try:
            subprocess.run(['icacls', folder_path, '/grant', 'Everyone:(OI)(CI)F', '/t', '/q'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")


    # Create Circulars table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Circulars (
                        CircularID INTEGER PRIMARY KEY,
                        CompanyFull TEXT,
                        CompanyShort TEXT,
                        Designation TEXT,
                        Fee INTEGER,
                        StartDate DATE,
                        LastDate DATE,
                        Status TEXT
                    )''')

    # Create Applications table with ON DELETE CASCADE constraint
    cursor.execute('''CREATE TABLE IF NOT EXISTS Applications (
                        ApplicationID INTEGER PRIMARY KEY,
                        CircularID INTEGER,
                        CompanyShort TEXT,
                        Category TEXT,
                        Designation TEXT,
                        AppliedOn DATE,
                        Registration TEXT,
                        Note TEXT,
                        Schedule TEXT,
                        FOREIGN KEY (CircularID) REFERENCES Circulars(CircularID) ON DELETE CASCADE
                    )''')

    # Create Exams table with ON DELETE CASCADE constraint
    cursor.execute('''CREATE TABLE IF NOT EXISTS Exams (
                        ExamID INTEGER PRIMARY KEY,
                        ApplicationID INTEGER,
                        CompanyShort TEXT,
                        Category TEXT,
                        Roll TEXT,
                        ExamType TEXT,
                        ExamDate DATE,
                        ExamVenue TEXT,
                        Result TEXT,
                        FOREIGN KEY (ApplicationID) REFERENCES Applications(ApplicationID) ON DELETE CASCADE
                    )''')

    # Create Archive table with ON DELETE CASCADE constraint
    cursor.execute('''CREATE TABLE IF NOT EXISTS Archive (
                        ArchiveID INTEGER PRIMARY KEY,
                        CircularID INTEGER,
                        CompanyFull TEXT,
                        CompanyShort TEXT,
                        Designation TEXT,
                        AppliedOn DATE,
                        Fee INTEGER,
                        ExamType TEXT,
                        ExamVenue TEXT,
                        Result TEXT,
                        Outcome TEXT,
                        Note TEXT,
                        FOREIGN KEY (CircularID) REFERENCES Circulars(CircularID) ON DELETE CASCADE
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS IDs (
                        ArchiveID INTEGER,
                        CircularID INTEGER,
                        ApplicationID INTEGER,
                        ExamID INTEGER
                    )''')

    cursor.execute('''INSERT INTO IDs (ArchiveID, CircularID, ApplicationID, ExamID)
                    VALUES (0, 0, 0, 0)''') 

    conn.commit()
    conn.close()
    print(f"Tables created/verified successfully in the database '{db_file}'.")

def newCircular(db_file, data):
    fullname = data['fullname']
    shortname = data['shortname']
    designation = data['designation']
    appfee = data['appfee']
    appdate = data['startdate']
    lastdate = data['lastdate']
    status = data['status']

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch the last CircularID from the IDs table
    cursor.execute('SELECT CircularID FROM IDs')
    last_circular_id = cursor.fetchone()

    # Fetch the last CircularID from the CircularID table
    cursor.execute('SELECT CircularID FROM IDs')
    last_circular_id = cursor.fetchone()[0]

    # Increment the last CircularID to get the new CircularID
    new_circular_id = last_circular_id + 1

    # Insert the data into the Circulars table
    cursor.execute('''
        INSERT INTO Circulars (CircularID, CompanyFull, CompanyShort, Designation, Fee, StartDate, LastDate, Status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (new_circular_id, fullname, shortname, designation, appfee, appdate, lastdate, status))

    # Update the IDs table with the new CircularID
    cursor.execute('''
        UPDATE IDs
        SET CircularID = ?
    ''', (new_circular_id,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return new_circular_id

def getData(db_file, table):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch all data from the Circulars table
    cursor.execute(f'SELECT * FROM {table}')
    data = cursor.fetchall()

    conn.close()

    return data    

def getDataRow(db_file, table, keyname, keyvalue):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Prepare the SELECT query with a WHERE clause to find the row
    query = f"SELECT * FROM {table} WHERE {keyname} = ?"

    # Execute the query to fetch the row based on the keyname and keyvalue
    cursor.execute(query, (keyvalue,))
    row = cursor.fetchone()  # Retrieve the first matching row

    conn.close()

    return row

def modCircular(db_file, circularid, data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Update data in the 'Circulars' table for the given circularID
    update_query = f'''
        UPDATE Circulars
        SET CompanyFull = ?,
            CompanyShort = ?,
            Designation = ?,
            Fee = ?,
            StartDate = ?,
            LastDate = ?,
            Status = ?
        WHERE circularID = ?
    '''

    # Extracting data from the 'data' dictionary
    circular_data = (
        data['fullname'],
        data['shortname'],
        data['designation'],
        data['appfee'],
        data['startdate'],
        data['lastdate'],
        data['status'],
        circularid  # circularID to update
    )

    # Execute the update query
    cursor.execute(update_query, circular_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def newApplication(db_file, circularid, data):
    company_short = data['shortname']
    category = data['category']
    designation = data['designation']
    applied_on = data['appdate']
    registration = data['regno']
    note = data['note']
    schedule = data['schedule']

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch the last ApplicationID from the Applications table
    cursor.execute('SELECT ApplicationID FROM IDs')
    last_application_id = cursor.fetchone()[0]

    # Increment the last ApplicationID to get the new ApplicationID
    new_application_id = last_application_id + 1

    # Insert the data into the Applications table
    cursor.execute('''
        INSERT INTO Applications (ApplicationID, CircularID, CompanyShort, Category, Designation, AppliedOn, Registration, Note, Schedule)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (new_application_id, circularid, company_short, category, designation, applied_on, registration, note, schedule))

    cursor.execute('''
        UPDATE IDs
        SET ApplicationID = ?
    ''', (new_application_id,))
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return new_application_id

def modApplication(db_file, applicationid, data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Update data in the 'Applications' table for the given ApplicationID
    update_query = '''
        UPDATE Applications
        SET CompanyShort = ?,
            Category = ?,
            Designation = ?,
            AppliedOn = ?,
            Registration = ?,
            Note = ?,
            Schedule = ?
        WHERE ApplicationID = ?
    '''

    # Extracting data from the 'data' dictionary
    application_data = (
        data['shortname'],
        data['category'],
        data['designation'],
        data['appdate'],
        data['regno'],
        data['note'],
        data['schedule'],
        applicationid
    )

    # Execute the update query
    cursor.execute(update_query, application_data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def newExam(db_file, applicationid, data):
    company_short = data['shortname']
    category = data['category']
    roll = data['rollno']
    exam_type = data['extype']
    exam_date = data['exdate']
    exam_venue = data['venue']
    result = data['result']

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch the last ExamID from the Exams table
    cursor.execute('SELECT ExamID FROM IDs')
    last_exam_id = cursor.fetchone()[0]

    # Increment the last ExamID to get the new ExamID
    new_exam_id = last_exam_id + 1

    # Insert the data into the Exams table
    cursor.execute('''
        INSERT INTO Exams (ExamID, ApplicationID, CompanyShort, Category, Roll, ExamType, ExamDate, ExamVenue, Result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (new_exam_id, applicationid, company_short, category, roll, exam_type, exam_date, exam_venue, result))

    cursor.execute('''
        UPDATE IDs
        SET ExamID = ?
    ''', (new_exam_id,))
    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return new_exam_id

def delCircular(db_file, circularid):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    
    cursor.execute('DELETE FROM Circulars WHERE CircularID = ?', (circularid,))
    conn.commit()
    conn.close()

    

def delExam(db_file, exam_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve the ApplicationID from the Exams table based on the provided ExamID
    cursor.execute('SELECT ApplicationID FROM Exams WHERE ExamID = ?', (exam_id,))
    row_data = cursor.fetchone()
    if row_data:
        application_id = row_data[0]

        # Delete the row from the Exams table using the given ExamID
        cursor.execute('DELETE FROM Exams WHERE ExamID = ?', (exam_id,))
        conn.commit()

        # Check the number of remaining rows with the same ApplicationID in the Exams table
        cursor.execute('SELECT COUNT(*) FROM Exams WHERE ApplicationID = ?', (application_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # If no other rows with the same ApplicationID, update Applications table Schedule to 'No'
            cursor.execute('UPDATE Applications SET Schedule = "No" WHERE ApplicationID = ?', (application_id,))
            conn.commit()

    conn.close()
def delApp(db_file, application_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve the CircularID from the Applications table based on ApplicationID
    cursor.execute('SELECT CircularID FROM Applications WHERE ApplicationID = ?', (application_id,))
    row_data = cursor.fetchone()
    if row_data:
        circular_id = row_data[0]

        # Delete rows from the Exams table associated with the given ApplicationID
        cursor.execute('DELETE FROM Exams WHERE ApplicationID = ?', (application_id,))
        conn.commit()

        # Delete the row from the Applications table based on the provided ApplicationID
        cursor.execute('DELETE FROM Applications WHERE ApplicationID = ?', (application_id,))
        conn.commit()

        # Update the Status in the Circulars table to 'Pending'
        cursor.execute('UPDATE Circulars SET Status = "Pending" WHERE CircularID = ?', (circular_id,))
        conn.commit()

    conn.close()

def modExam(db_file, exam_id, data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Update data in the 'Exams' table for the given ExamID
    update_query = '''
        UPDATE Exams
        SET CompanyShort = ?,
            Category = ?,
            Roll = ?,
            ExamType = ?,
            ExamDate = ?,
            ExamVenue = ?,
            Result = ?
        WHERE ExamID = ?
    '''

    # Extracting data from the 'data' dictionary
    exam_data = (
        data['shortname'],
        data['category'],
        data['rollno'],
        data['extype'],
        data['exdate'],
        data['venue'],
        data['result'],
        exam_id
    )

    # Execute the update query
    cursor.execute(update_query, exam_data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def evalDb(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

        # Fetch ExamIDs with 'Failed' status
    cursor.execute('''
        SELECT ExamID
        FROM Exams
        WHERE Result = 'Failed'
    ''')
    failed_exam_ids = cursor.fetchall()

    for exam_id in failed_exam_ids:
        # Fetch ApplicationID associated with the failed ExamID
        cursor.execute('''
            SELECT ApplicationID
            FROM Exams
            WHERE ExamID = ?
        ''', exam_id)
        application_id = cursor.fetchone()

        # Fetch all ExamIDs associated with the fetched ApplicationID
        cursor.execute('''
            SELECT ExamID
            FROM Exams
            WHERE ApplicationID = ?
        ''', application_id)
        associated_exam_ids = cursor.fetchall()

        # Move data associated with all associated ExamIDs to the Archive table
        for associated_exam_id in associated_exam_ids:
            cursor.execute('''
                INSERT INTO Archive (CircularID, CompanyFull, CompanyShort, Designation, AppliedOn, Fee, ExamType, ExamVenue, Result, Outcome, Note)
                SELECT c.CircularID, c.CompanyFull, c.CompanyShort, c.Designation, a.AppliedOn, c.Fee, e.ExamType, e.ExamVenue, e.Result, 'Failed', a.Note
                FROM Circulars c
                JOIN Applications a ON c.CircularID = a.CircularID
                JOIN Exams e ON a.ApplicationID = e.ApplicationID
                WHERE e.ExamID = ?
            ''', associated_exam_id)
            conn.commit()

    # Finally, delete data from the Circulars table where Applications data is deleted
    cursor.execute('''
        DELETE FROM Circulars
        WHERE CircularID IN (
            SELECT CircularID
            FROM Applications
            WHERE ApplicationID IN (
                SELECT ApplicationID
                FROM Exams
                WHERE Result = 'Failed'
            )
        )
    ''')

    # Commit changes to the database
    conn.commit()


    # Removing data from Applications table related to non-existing CircularID in Circulars table
    cursor.execute('DELETE FROM Applications WHERE CircularID NOT IN (SELECT CircularID FROM Circulars)')
    conn.commit()

    # Removing data from Exams table related to non-existing ApplicationID in Applications table
    cursor.execute('DELETE FROM Exams WHERE ApplicationID NOT IN (SELECT ApplicationID FROM Applications)')
    conn.commit()

    # Deleting rows from Exams table where ApplicationID has Schedule as 'No'
    cursor.execute('DELETE FROM Exams WHERE ApplicationID IN (SELECT ApplicationID FROM Applications WHERE Schedule = "No")')
    conn.commit()

    # Updating Applications table where Schedule is 'Yes' but not in Exams table
    cursor.execute('UPDATE Applications SET Schedule = "No" WHERE Schedule = "Yes" AND ApplicationID NOT IN (SELECT ApplicationID FROM Exams)')
    conn.commit()


    # Moving rows with 'Pending' status and LastDate before current date to Archives table
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO Archive (CircularID, CompanyFull, CompanyShort, Designation, Fee, Outcome)
        SELECT CircularID, CompanyFull, CompanyShort, Designation, Fee, 'Expired'
        FROM Circulars
        WHERE LastDate < ? AND Status = 'Pending'
    ''', (current_date,))
    conn.commit()

    cursor.execute('''
    DELETE FROM Applications
    WHERE CircularID IN (
        SELECT CircularID
        FROM Circulars
        WHERE Status = 'Pending'
    )
''')
    conn.commit()

    # Deleting rows from Circulars table where LastDate is before current date and Status is 'Pending'
    cursor.execute('DELETE FROM Circulars WHERE LastDate < ? AND Status = "Pending"', (current_date,))
    conn.commit()

    # Commit changes and close the connection
    conn.close()

def move2arc(db_file, exam_id):

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Exams
        SET Result = 'Passed!' WHERE ExamID = ?
    ''', (exam_id,))
    # Commit changes and close the connection
    conn.commit()


    # Fetch ApplicationID associated with the failed ExamID
    cursor.execute('''
        SELECT ApplicationID
        FROM Exams
        WHERE ExamID = ?
    ''', (exam_id,))
    application_id = cursor.fetchone()[0]

    # Fetch all ExamIDs associated with the fetched ApplicationID
    cursor.execute('''
    SELECT ExamID
    FROM Exams
    WHERE ApplicationID = ?
''', (application_id,))
    associated_exam_ids = cursor.fetchall()

    # Move data associated with all associated ExamIDs to the Archive table
    for associated_exam_id in associated_exam_ids:
        cursor.execute('''
            INSERT INTO Archive (CircularID, CompanyFull, CompanyShort, Designation, AppliedOn, Fee, ExamType, ExamVenue, Result, Outcome, Note)
            SELECT c.CircularID, c.CompanyFull, c.CompanyShort, c.Designation, a.AppliedOn, c.Fee, e.ExamType, e.ExamVenue, e.Result, 'Success!', a.Note
            FROM Circulars c
            JOIN Applications a ON c.CircularID = a.CircularID
            JOIN Exams e ON a.ApplicationID = e.ApplicationID
            WHERE e.ExamID = ?
        ''', associated_exam_id)
        conn.commit()

    # Finally, delete data from the Circulars table where Applications data is deleted
    cursor.execute('''
        DELETE FROM Circulars
        WHERE CircularID IN (
            SELECT CircularID
            FROM Applications
            WHERE ApplicationID IN (
                SELECT ApplicationID
                FROM Exams
                WHERE Result = 'Passed!'
            )
        )
    ''')

    # Commit changes to the database
    conn.commit()

