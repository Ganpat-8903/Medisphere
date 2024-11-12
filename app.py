from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hospital'
mysql = MySQL(app)

logged_in = False
@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'ganpat8903' and password == '1234':
            logged_in = True  
            return redirect(url_for('index'))  
        else:
            return render_template('login.html', message='Invalid Username or password! Please try again.')

    return render_template('login.html')

@app.route('/')
def index():
    global logged_in
    if logged_in:
        return render_template('index.html')
    else:
        return redirect(url_for('login')) 

@app.route('/display_doctors')
def display_doctors():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM doctors')
    doctors = cursor.fetchall()
    cursor.close()
    return render_template('display_doctors.html', doctors=doctors)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        pname = request.form['pname']
        address = request.form['address']
        contact_no = request.form['contact_no']
        age = int(request.form['age'])
        illness = request.form['illness']
        
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO patients(p_name, address, contact_no, age, illness) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (pname, address, contact_no, age, illness))
        mysql.connection.commit()
        cursor.close()
        return render_template('message.html')
    
    return render_template('add_patient.html')

@app.route('/display_patients')
def display_patients():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()

    cursor.execute('SELECT * FROM illnesses')
    illnesses = cursor.fetchall()

    cursor.close()

    return render_template('display_patients.html', patients=patients, illnesses=illnesses)



@app.route('/remove_patient', methods=['GET', 'POST'])
def remove_patient():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM patients WHERE p_id = %s', (patient_id,))
        patient = cursor.fetchone() 
        if patient:
            cursor.execute('DELETE FROM patients WHERE p_id = %s', (patient_id,))
            mysql.connection.commit()
            cursor.close()
            return render_template('message_remove.html') 
        else:
            cursor.close()
            return render_template('remove_patient.html', message='No patient found with that ID.')
    
    return render_template('remove_patient.html')



@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date_str = request.form['appointment_date']
        
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE d_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        
        if doctor:
            cursor.execute("SELECT * FROM patients WHERE p_id = %s", (patient_id,))
            patient = cursor.fetchone()  
            
            if patient:
                sql = "INSERT INTO appointments(p_id, d_id, date) VALUES (%s, %s, %s)"
                cursor.execute(sql, (patient_id, doctor_id, appointment_date_str))  
                mysql.connection.commit()
                return render_template('message_appointment.html')  
            else:
                cursor.close()
                return render_template('add_appointment.html', message='No patient found with that ID.')
        else:
            cursor.close()
            return render_template('add_appointment.html', message='Doctor with ID {} not found.'.format(doctor_id))
        
    return render_template('add_appointment.html')


@app.route('/display_appointments')
def display_appointments():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT appointments.*, patients.p_name, doctors.d_name FROM appointments JOIN patients ON appointments.p_id = patients.p_id JOIN doctors ON appointments.d_id = doctors.d_id')
    appointments = cursor.fetchall()
    cursor.close()
    return render_template('display_appointments.html', appointments=appointments)

@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM patients WHERE p_id = %s', (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        if patient:
            return render_template('patient_details.html', patient=patient)
        else:
            return render_template('search_patient.html', message='No patient found with that ID.')
    
    return render_template('search_patient.html')

if __name__ == '__main__':
    app.run(debug=True)
