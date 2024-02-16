import pymssql
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, session, jsonify, flash, g, send_file


SERVER_INFO = 'server info here'
USER_INFO = 'User info here'
PASSWORD = 'Password here'
DATABASE = 'Database here'


conn = pymssql.connect(
   server=SERVER_INFO,
   user=USER_INFO,
   password=PASSWORD,
   database=DATABASE,
   as_dict=True
)

cur = conn.cursor()
app = Flask(__name__)
app.secret_key = "hello"

"""
This route serves images based on the provided image name.
"""
@app.route('/image/<image_name>')
def get_image(image_name):
    try:
        return send_file(f'images/{image_name}', mimetype='image/jpeg')
    except FileNotFoundError:
        return "Image not found", 404

"""
Routes to provided html pages.
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/employee')
def employee_page():
    return render_template('employee.html')

@app.route('/adopter')
def adopter_page():
    return render_template('adopter.html')

@app.route('/adopterDelete')
def adopter_delete_page():
    return render_template('adopterDelete.html')

@app.route('/adopterUpdate')
def adopter_update_page():
    return render_template('adopterUpdate.html')

@app.route('/insertAR')
def ar_insert_page():
    return render_template('animalRecordInsert.html')

@app.route('/deleteAR')
def ar_delete_page():
    return render_template('animalRecordDelete.html')

@app.route('/insertMR')
def mr_insert_page():
    return render_template('medicalRecordInsert.html')

@app.route('/deleteMR')
def mr_delete_page():
    return render_template('medicalRecordDelete.html')

@app.route('/updateMR')
def mr_update_page():
    return render_template('medicalRecordUpdate.html')

@app.route('/adoptAR')
def ar_adopt_page():
    return render_template('animalRecordAdopt.html')

"""
Helper Functions and Getters
"""
#selectEmployeeID
def selectEmployeeID(shelterID, employeeName):
    SQL_QUERY = """
    SELECT E_ID FROM EMPLOYEE WHERE S_ID = %s AND E_Name = %s;
    """
    cur.execute(SQL_QUERY, (shelterID, employeeName))
    rows = cur.fetchone()

    # Return the first element of the result if it exists, else return None
    return rows if rows else None

#getAnimalID
def getAnimalID(adopterID):
    SQL_QUERY = """
    SELECT A_ID FROM ADOPTED WHERE AD_ID = %s;
    """
    cur.execute(SQL_QUERY, (adopterID))
    rows = cur.fetchone()

    # Return the first element of the result if it exists, else return None
    return rows if rows else None

#selectAnimalID
def selectAnimalID(animalName, animalAge, animalType, animalBreed, shelterID):
    SQL_QUERY = """
    SELECT A_ID FROM ANIMAL WHERE A_Name = %s AND A_Age = %s AND A_Animal_type = %s AND A_Breed = %s AND S_ID = %s;
    """
    cur.execute(SQL_QUERY, (animalName, animalAge, animalType, animalBreed, shelterID))
    rows = cur.fetchone()

    # Return the first element of the result if it exists, else return None
    return rows if rows else None

#selectAdopterID
def selectAdopterID(adopterName, animalID):
    SQL_QUERY = """
    SELECT AD_ID FROM ADOPTER WHERE AD_NAME = %s AND A_ID = %s;
    """
    cur.execute(SQL_QUERY, (adopterName, animalID))
    rows = cur.fetchone()

    # Return the first element of the result if it exists, else return None
    return rows if rows else None

#selectMedicalID
def selectMedicalID(employeeID, diagnosis, animalID):
    SQL_QUERY = """
    SELECT M_ID FROM MEDICAL_RECORD WHERE E_ID = %s AND M_Diagnosis = %s AND A_ID = %s;
    """
    cur.execute(SQL_QUERY, (employeeID, diagnosis, animalID))
    row = cur.fetchone()

    # Return the first element of the result if it exists, else return None
    return row if row else None


"""
Query calls
"""
#View Shelter
@app.route('/view-shelter')
def viewShelter():
    SQL_QUERY = """
    SELECT
        SHELTER.S_ID,
        SHELTER.S_Name,
        SHELTER.S_Location,
        COUNT(DISTINCT ANIMAL.A_ID) AS AnimalCount,
        COUNT(DISTINCT EMPLOYEE.E_ID) AS EmployeeCount
    FROM
        SHELTER
    LEFT JOIN
        ANIMAL ON SHELTER.S_ID = ANIMAL.S_ID
    LEFT JOIN
        EMPLOYEE ON SHELTER.S_ID = EMPLOYEE.S_ID
    GROUP BY
        SHELTER.S_ID, SHELTER.S_Name, SHELTER.S_Location;
    """
    cur.execute(SQL_QUERY)
    rows = cur.fetchall()
    return render_template("shelterDisplay.html", things=rows)

#Add shelter
@app.route('/add-shelter', methods=['GET', 'POST'])
def addShelter():
    try:
        shelterName = request.form['shelterName']
        shelterLocation = request.form['shelterLocation']
    except:
        flash("Invalid Number Entry", "info")
        return render_template("shelterInsert.html")
   
    SQL_QUERY = """
    INSERT INTO SHELTER VALUES(%s, %s);
    """
    
    cur.execute(SQL_QUERY, (shelterName, shelterLocation))
    conn.commit()
    return render_template("shelterInsert.html")

#Delete Shelter
@app.route('/delete-shelter', methods=['GET', 'POST'])
def deleteShelter():
    try:
        shelterID = int(request.form['shelterID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("shelterDelete.html")
    
    SQL_QUERY1 = """
    DELETE FROM SHELTER WHERE S_ID = %s;
    """
    SQL_QUERY2 ="""
    DELETE from WORKS WHERE S_ID = %s;
    """
    SQL_QUERY3 ="""
    DELETE from EMPLOYEE WHERE S_ID = %s;
    """
    cur.execute(SQL_QUERY2, (shelterID))
    cur.execute(SQL_QUERY3, (shelterID))
    cur.execute(SQL_QUERY1, (shelterID))
    conn.commit()
    return render_template("shelterDelete.html")

#Update Shelter
@app.route('/update-shelter', methods=['GET', 'POST'])
def updateShelter():
    try:
        shelterLocation = request.form['shelterLocation']
        shelterID = int(request.form['shelterID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("shelterUpdate.html")
   
    SQL_QUERY = """
    UPDATE SHELTER SET S_Location = %s WHERE S_ID = %s;
    """
    
    try:
        cur.execute(SQL_QUERY, (shelterLocation, shelterID))
        conn.commit()
        flash("Shelter Updated Successfully", "success")
    except Exception as e:
        flash(f"Error updating shelter: {str(e)}", "error")

    
    # cur.execute(SQL_QUERY, (shelterLocation, shelterID))
    # conn.commit()
    return render_template("shelterUpdate.html")

#Display All Employee
@app.route('/display-all-employee', methods=['GET', 'POST'])
def displayEmployee():
    if request.method == 'POST':
        try:
            SID = int(request.form['SID'])
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("employeeDisplayResult.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get SID from query parameters
        SID = request.args.get('SID')
        if SID is None:
            return render_template("employeeDisplay.html")
        try:
            SID = int(SID)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("employeeDisplay.html")

    SQL_QUERY = """
    SELECT EMPLOYEE.E_ID, EMPLOYEE.E_Name, SHELTER.S_Name
    FROM EMPLOYEE, SHELTER
    WHERE EMPLOYEE.S_ID = SHELTER.S_ID AND SHELTER.S_ID = %s;
    """
    cur.execute(SQL_QUERY, (SID,))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("employeeDisplay.html", things=rows)

#Search a Single Employee
@app.route('/search-employee', methods=['GET', 'POST'])
def searchEmployee():
    if request.method == 'POST':
        try:
            EID = int(request.form['EID'])
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("employeeSearch.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get EID from query parameters
        EID = request.args.get('EID')
        if EID is None:
            return render_template("employeeSearch.html")
        try:
            EID = int(EID)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("employeeSearch.html")

    SQL_QUERY = """
    SELECT EMPLOYEE.E_ID, EMPLOYEE.E_Name, EMPLOYEE.E_SSN, EMPLOYEE.E_Position, EMPLOYEE.S_ID, WORKS.startDate
    FROM EMPLOYEE
    JOIN WORKS ON EMPLOYEE.E_ID = WORKS.E_ID
    WHERE EMPLOYEE.E_ID = %s;
    """
    cur.execute(SQL_QUERY, (EID,))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("employeeSearch.html", things=rows)

#Add Employee
@app.route('/add-employee', methods=['POST', 'GET'])
def addEmployee():
    try:
        employee_name = request.form['employeeName']
        employee_ssn = request.form['employeeSSN']
        employee_wage = request.form['employeeWage']
        employee_position = request.form['employeePosition']
        shelter_id = request.form['employeeSID']
    except KeyError:
        flash("Invalid Number Entry", "info")
        return render_template("employeeInsert.html")

    # Use placeholders to prevent SQL injection
    sql_insert_employee = "INSERT INTO EMPLOYEE VALUES (%s, %s, %s, %s, %s);"
    sql_insert_works = "INSERT INTO WORKS VALUES (%s, %s, %s);"

    # Assuming date is the current date
    current_date = datetime.now().date()

    try:
        # Insert employee
        cur.execute(sql_insert_employee, (employee_name, employee_ssn, employee_wage, employee_position, shelter_id))
        # Insert into WORKS
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        flash("Error adding employee", "error")

    # Get the employee ID
    employee_id = selectEmployeeID(shelter_id, employee_name)
    if employee_id is None:
        flash("Employee not found", "error")
        return render_template("employeeInsert.html")

    try: 
        cur.execute(sql_insert_works, (shelter_id, int(employee_id.get('E_ID', 0)), current_date))
        conn.commit()
        flash("Employee and works record added successfully", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash("Error adding employee", "error")
    return render_template("employeeInsert.html")

#Delete Employee
@app.route('/delete-employee', methods=['GET', 'POST'])
def deleteEmployee():
    try:
        employeeID = int(request.form['employeeID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("employeeDelete.html")
   
    SQL_DELETE_WORKS = "DELETE FROM WORKS WHERE E_ID = %s;"
    SQL_DELETE_EMPLOYEE = "DELETE FROM EMPLOYEE WHERE E_ID = %s;"

    cur.execute(SQL_DELETE_WORKS, (employeeID))
    cur.execute(SQL_DELETE_EMPLOYEE, (employeeID))
    conn.commit()
    return render_template("employeeDelete.html")

#Update Employee
@app.route('/update-employee', methods=['GET', 'POST'])
def updateEmployee():
    try:
        employeeID = request.form['employeeID']
        employeeWage = request.form['employeeWage']
        employeePosition = request.form['employeePosition']
        shelterID = int(request.form['employeeSID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("employeeUpdate.html")
   
    SQL_UPDATE_EMPLOYEE = """
    UPDATE EMPLOYEE SET E_Wage = %s, E_Position = %s, S_ID = %s WHERE E_ID = %s;
    """
    SQL_UPDATE_WORKS = """
    UPDATE WORKS SET S_ID = %s WHERE E_ID = %s;
    """
    
    try:
        cur.execute(SQL_UPDATE_EMPLOYEE, (employeeWage, employeePosition, shelterID, employeeID))
        cur.execute(SQL_UPDATE_WORKS, (shelterID, employeeID))
        conn.commit()
        flash("Employee Updated Successfully", "success")
    except Exception as e:
        flash(f"Error updating shelter: {str(e)}", "error")
        
    return render_template("employeeUpdate.html")

#Search Adopter
@app.route('/adopterSearch', methods=['GET', 'POST'])
def searchAnimal():
    if request.method == 'POST':
        try:
            Animaltype = request.form['animalType']
            AnimalAge = int(request.form['age'])
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("adopter.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get EID from query parameters
        EID = request.args.get('EID')
        if None in (Animaltype, AnimalAge):
            return render_template("adopter.html")
        try:
            Animaltype = Animaltype
            AnimalAge = int(AnimalAge)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("adopter.html")

    SQL_QUERY = """
    SELECT
    ANIMAL.A_ID,
    ANIMAL.A_name,
    ANIMAL.A_Age,
    ANIMAL.A_Animal_type,
    ANIMAL.A_Breed,
    (SELECT SHELTER.S_Name FROM SHELTER WHERE SHELTER.S_ID = ANIMAL.S_ID) AS 'Shelter Name',
    (SELECT SHELTER.S_Location FROM SHELTER WHERE SHELTER.S_ID = ANIMAL.S_ID) AS 'Shelter Location'
FROM
    ANIMAL
WHERE
    ANIMAL.A_Adoption_status = 'Not Adopted'
    AND ANIMAL.A_ID IN (
        SELECT A_ID
        FROM ANIMAL
        WHERE ANIMAL.A_Animal_type = %s
        AND ANIMAL.A_Age <= %s
    )
    AND ANIMAL.S_ID IN (
        SELECT S_ID
        FROM SHELTER
        WHERE SHELTER.S_ID = ANIMAL.S_ID
    );

    """
    cur.execute(SQL_QUERY, (Animaltype, AnimalAge))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("adopter.html", things=rows)

#Display All Animals With Medical Record
@app.route('/display-all-animal-medicalrecord', methods=['GET', 'POST'])
def displayAllAnimal():
    if request.method == 'POST':
        try:
            EID = int(request.form['employeeID'])
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("employeeSearch.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get EID from query parameters
        EID = request.args.get('EID')
        if EID is None:
            return render_template("displayAnimalMedicalRecord.html")
        try:
            EID = int(EID)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("displayAnimalMedicalRecord.html")

    SQL_QUERY = """
    SELECT ANIMAL.A_ID, ANIMAL.A_name, ANIMAL.A_Age, ANIMAL.A_Animal_type, ANIMAL.A_Breed, SHELTER.S_Name, MEDICAL_RECORD.M_Health_status
    FROM EMPLOYEE
    LEFT JOIN SHELTER ON EMPLOYEE.S_ID = SHELTER.S_ID
    LEFT JOIN ANIMAL ON ANIMAL.S_ID = SHELTER.S_ID
    LEFT JOIN MEDICAL_RECORD ON ANIMAL.A_ID = MEDICAL_RECORD.A_ID
    WHERE EMPLOYEE.E_ID = %s;
    """
    cur.execute(SQL_QUERY, (EID,))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("displayAnimalMedicalRecord.html", things=rows)

#Search Animal Record and Medical Recorrd
@app.route('/search-animal-medicalrecord', methods=['GET', 'POST'])
def searchAnimalMedicalRecord():
    if request.method == 'POST':
        try:
            AnimalID = request.form['animalID']
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("animalSearch.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get EID from query parameters
        AnimalID = request.args.get('animalID')
        if AnimalID is None:
            return render_template("animalSearch.html")
        try:
            AnimalID = int(AnimalID)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("animalSearch.html")

    SQL_QUERY = """
    SELECT DISTINCT ANIMAL.A_ID, ANIMAL.A_name, ANIMAL.A_Age, ANIMAL.A_Animal_type, ANIMAL.A_Breed, 
                    SHELTER.S_Name, MEDICAL_RECORD.M_ID, MEDICAL_RECORD.M_Diagnosis, MEDICAL_RECORD.M_Health_status
    FROM EMPLOYEE
    LEFT JOIN SHELTER ON EMPLOYEE.S_ID = SHELTER.S_ID
    LEFT JOIN ANIMAL ON ANIMAL.S_ID = SHELTER.S_ID
    LEFT JOIN MEDICAL_RECORD ON ANIMAL.A_ID = MEDICAL_RECORD.A_ID
    WHERE ANIMAL.A_ID = %s;
    """

    cur.execute(SQL_QUERY, (AnimalID))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("animalSearch.html", things=rows)

#Search Adopter
@app.route('/searchAdopter', methods=['GET', 'POST'])
def searchAdopter():
    if request.method == 'POST':
        try:
            AdopterID = int(request.form['adopterID'])
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("adopterSearch.html", things=None)
    elif request.method == 'GET':
        # If it's a GET request, try to get EID from query parameters
        EID = request.args.get('EID')
        if None in (AdopterID):
            return render_template("adopterSearch.html")
        try:
            AdopterID = int(AdopterID)
        except ValueError:
            flash("Invalid Number Entry", "info")
            return render_template("adopterSearch.html")

    SQL_QUERY = """SELECT ADOPTER.AD_ID, ADOPTER.AD_Name, ADOPTER.AD_Age, ADOPTER.AD_Address, ADOPTER.AD_Phone_number, ANIMAL.A_ID, ANIMAL.A_Name, ADOPTED.Date_of_adoption
    FROM ADOPTER 
    JOIN ADOPTED ON (ADOPTED.AD_ID = ADOPTER.AD_ID) 
    JOIN ANIMAL ON (ADOPTED.A_ID = ANIMAL.A_ID)
    WHERE ADOPTED.AD_ID = %s;
    """
    cur.execute(SQL_QUERY, (AdopterID))
    rows = cur.fetchall()

    if request.method == 'GET':
        # If it's a GET request and AJAX, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(things=rows)

    # Render the template with the results
    return render_template("adopterSearch.html", things=rows)

#Delete Adopter
@app.route('/delete-adopter', methods=['GET', 'POST'])
def deleteAdopter():
    try:
        adopterID = int(request.form['adopterID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("adopterDelete.html")
   
    SQL_DELETE_ADOPTED = """DELETE from ADOPTED WHERE AD_ID = %s;"""
    SQL_DELETE_ADOPTER = """DELETE from ADOPTER WHERE AD_ID = %s;"""
    SQL_UPDATE_ANIMAL = "UPDATE ANIMAL SET A_Adoption_status = 'Not Adopted' WHERE A_ID = %s;"

    animalID = getAnimalID(adopterID)
    if animalID is None:
        flash("Animal not found", "error")
        return render_template("animalRecordInsert.html")
    cur.execute(SQL_UPDATE_ANIMAL, (int(animalID.get('A_ID', 0))))
    cur.execute(SQL_DELETE_ADOPTED, (adopterID))
    cur.execute(SQL_DELETE_ADOPTER, (adopterID))
    
    conn.commit()
    return render_template("adopterDelete.html")

#Update Adopter
@app.route('/update-adopter', methods=['GET', 'POST'])
def updateAdopter():
    try:
        adopterID = int(request.form['adopterID'])
        adopterName = request.form['adopterName']
        adopterAge = request.form['adopterAge']
        adopterAddress = request.form['adopterAddress']
        adopterPhone = request.form['adopterPhone']
    except ValueError:
        flash("Invalid Number Entry", "info")
        return render_template("adopterUpdate.html")

    SQL_QUERY = """
    UPDATE ADOPTER SET AD_Name = %s, AD_Age = %s, AD_Address = %s, AD_Phone_number = %s WHERE AD_ID = %s;
    """

    try:
        cur.execute(SQL_QUERY, (adopterName, adopterAge, adopterAddress, adopterPhone, adopterID))
        conn.commit()
        flash("Adopter Updated Successfully", "success")
    except Exception as e:
        flash(f"Error updating adopter: {str(e)}", "error")

    return render_template("adopterUpdate.html")

#Add Animal
@app.route('/add-animal', methods=['POST', 'GET'])
def addAnimal():
    try:
        animalName = request.form['animalName']
        animalAge = int(request.form['animalAge'])  # Convert to integer
        animalType = request.form['animalType']
        animalBreed = request.form['animalBreed']
        shelterID = int(request.form['shelterID'])  # Convert to integer
    except ValueError:
        flash("Invalid Number Entry", "info")
        return render_template("animalRecordInsert.html")

    if None in (animalName, animalAge, animalType, animalBreed, shelterID):
        flash("All fields are required", "info")
        return render_template("animalRecordInsert.html")

    # Use placeholders to prevent SQL injection
    sql_insert_animal = "INSERT INTO ANIMAL VALUES (%s, %s, %s, %s, 'Not Adopted', %s);"
    sql_insert_shelters = "INSERT INTO SHELTERS VALUES (%s, %s, %s);"

    # Assuming date is the current date
    current_date = datetime.now().date()

    try:
        # Insert animal
        cur.execute(sql_insert_animal, (animalName, animalAge, animalType, animalBreed, shelterID))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        flash("Error adding employee", "error")
    
    # Get animal ID
    animal_id = selectAnimalID(animalName, animalAge, animalType, animalBreed, shelterID)
    if animal_id is None:
        flash("Animal not found", "error")
        return render_template("animalRecordInsert.html")
    
    # Insert into SHELTERS
    try:
        cur.execute(sql_insert_shelters, (shelterID, int(animal_id.get('A_ID', 0)), current_date))
        conn.commit()
        flash("Animal Record Inserted Successfully", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")

    return render_template("animalRecordInsert.html")

#Delete Animal
@app.route('/delete-animal', methods=['GET', 'POST'])
def deleteAnimal():
    try:
        animalID = int(request.form['animalID'])
    except:
        flash("Invalid Number Entry", "info")
        return render_template("shelterDelete.html")
   
    SQL_QUERY = """DELETE FROM ANIMAL WHERE A_ID = %s;"""
    SQL_QUERY2 = """DELETE from SHELTERS WHERE A_ID = %s;"""
    SQL_QUERY3 = """DELETE from ADOPTED WHERE A_ID = %s;"""
    SQL_QUERY5 = """DELETE from MEDICAL_RECORD WHERE A_ID = %s;"""
    SQL_QUERY6 = """DELETE from ADOPTER WHERE A_ID = %s;"""
    SQL_DELETE_CREATES = """DELETE FROM CREATES WHERE M_ID IN (SELECT M_ID FROM MEDICAL_RECORD WHERE A_ID = %s);"""
    
    cur.execute(SQL_DELETE_CREATES, (animalID))
    cur.execute(SQL_QUERY3, (animalID))
    cur.execute(SQL_QUERY2, (animalID))
    cur.execute(SQL_QUERY6, (animalID))
    cur.execute(SQL_QUERY5, (animalID))
    cur.execute(SQL_QUERY, (animalID))
    conn.commit()
    return render_template("animalRecordDelete.html")

#Add Adopter
@app.route('/add-adopter', methods=['POST', 'GET'])
def addAdopter():
    try:
        adopterName = request.form['adopterName']
        adopterAge = int(request.form['adopterAge'])
        adopterAddress = request.form['adopterAddress']
        adopterPhone = request.form['adopterPhone']
        animalID = int(request.form['animalID'])
    except ValueError:
        flash("Invalid Number Entry", "info")
        return render_template("animalRecordAdopt.html")

    
    # Use placeholders to prevent SQL injection
    sql_insert_adopter = "INSERT INTO ADOPTER VALUES (%s, %s, %s, %s, %s)"
    sql_insert_adopted = "INSERT INTO ADOPTED VALUES (%s, %s, %s)"
    sql_update_animal = "UPDATE ANIMAL SET A_Adoption_status = 'Adopted' WHERE A_ID = %s;"
    
    # date is the current date
    current_date = datetime.now().date()
    
    try:
        # Insert adopter
        cur.execute(sql_insert_adopter, (adopterName, adopterAge, adopterAddress, adopterPhone, animalID))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        flash("Error adding adopter", "error")
    
    # Get adopter ID
    adopter_id = selectAdopterID(adopterName, animalID)
    if adopter_id is None:
        flash("Adopter not found", "error")
        return render_template("animalRecordAdopt.html")
    try:
        cur.execute(sql_insert_adopted, (animalID, int(adopter_id.get('AD_ID', 0)), current_date))
        cur.execute(sql_update_animal, (animalID))
        conn.commit()
        flash("Adoption Successful", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")

    return render_template("animalRecordAdopt.html")

#Delete Medical Record
@app.route('/delete-medicalRecord', methods=['GET', 'POST'])
def deleteMedicalRecord():
    try:
        medicalID = int(request.form['medicalIDToDelete'])
    except ValueError:
        flash("Invalid Number Entry", "info")
        return render_template("medicalRecordDelete.html")

    SQL_DELETE_MEDICAL_RECORD = """DELETE FROM MEDICAL_RECORD WHERE M_ID = %s;"""
    SQL_DELETE_CREATES = """DELETE from CREATES WHERE M_ID = %s;"""
    
    cur.execute(SQL_DELETE_MEDICAL_RECORD, (medicalID))
    cur.execute(SQL_DELETE_CREATES, (medicalID))
    conn.commit()

    return render_template("medicalRecordDelete.html")

#Update Medical Record
@app.route('/update-medical-record', methods=['GET', 'POST'])
def updateMedicalRecord():
    if request.method == 'POST':
        try:
            diagnosis = request.form['updatedDiagnosis']
            medicalRecordID = int(request.form['medicalIDToUpdate'])

            SQL_QUERY = """
            UPDATE MEDICAL_RECORD SET M_Diagnosis = %s WHERE M_ID = %s;
            """

            cur.execute(SQL_QUERY, (diagnosis, medicalRecordID))
            conn.commit()
            flash("Medical Record Updated Successfully", "success")
        except Exception as e:
            flash(f"Error updating medical record: {str(e)}", "error")

    return render_template("medicalRecordUpdate.html")

#Add Medical Record
@app.route('/add-medical-record', methods=['POST', 'GET'])
def addMedicalRecord():
    try:
        employeeID = int(request.form['employeeID'])
        animalID = int(request.form['animalID'])
        diagnosis = request.form['diagnosis']
        healthStatus = request.form['status']
        
    except ValueError:
        flash("Invalid Number Entry", "info")
        return render_template("medicalRecordInsert.html")

    # Use placeholders to prevent SQL injection
    sql_insert_medical = "INSERT INTO MEDICAL_RECORD VALUES (%s, %s, %s, %s);"
    sql_insert_creates = "INSERT INTO CREATES VALUES (%s, %s, %s, 'Medical record CREATED')"

    # date is the current date
    current_date = datetime.now().date()

    try:
        cur.execute(sql_insert_medical, (healthStatus, diagnosis, employeeID, animalID))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        flash("Error adding medical record", "error")

    medicalRecord_id = selectMedicalID(employeeID, diagnosis, animalID)
    if medicalRecord_id is None:
        flash("Medical record not found", "error")
        return render_template("medicalRecordInsert.html")
    
    try:
        cur.execute(sql_insert_creates, (employeeID, int(medicalRecord_id.get("M_ID", 0)), current_date))
        conn.commit()
        flash("Creates Successful", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")

    return render_template("medicalRecordInsert.html")

if __name__ == "__main__":
    app.run(debug=True)
    cur.close()
    conn.close()


    