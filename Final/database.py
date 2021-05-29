import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql"
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS CardiologyDep")
mycursor.execute("CREATE DATABASE CardiologyDep")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="CardiologyDep"
)
mycursor = mydb.cursor()


mycursor.execute("DROP TABLE IF EXISTS patients")
mycursor.execute("""CREATE TABLE patients (Fname VARCHAR(255), Lname VARCHAR(255), Pssn INT, address VARCHAR(255),
                    gender VARCHAR(255), P_password VARCHAR(255), P_bdate DATE,EnterDate DATE,Scans BLOB DEFAULT NULL ,PRIMARY KEY(Pssn))""")

mycursor.execute("DROP TABLE IF EXISTS department")
mycursor.execute("""CREATE TABLE department (Dep_name VARCHAR(255), DepID INT, PRIMARY KEY(DepID))""")

mycursor.execute("DROP TABLE IF EXISTS Admin")
mycursor.execute("""CREATE TABLE Admin (Ad_ssn INT, Ad_password VARCHAR(255), Ad_Fname VARCHAR(255),
                    Ad_Lname VARCHAR(255), PRIMARY KEY(Ad_ssn))""")

mycursor.execute("DROP TABLE IF EXISTS doctors")
mycursor.execute("""CREATE TABLE doctors (D_Fname VARCHAR(255), D_Lname VARCHAR(255), Dgender VARCHAR(255), Dssn INT,
                    D_password VARCHAR(255),day VARCHAR(255),St_time TIME, End_time TIME, Dep_id INT, D_bdate DATE, Jdate DATE,
                    D_salary INT, PRIMARY KEY(Dssn),FOREIGN KEY (Dep_id) REFERENCES department(DepID))""")

mycursor.execute("DROP TABLE IF EXISTS nurses")
mycursor.execute(""" CREATE TABLE nurses (N_Fname VARCHAR(255), N_Lname VARCHAR(255), Ngender VARCHAR(255), Nssn INT,Dep_id INT,
                    N_salary INT, N_password VARCHAR(255),day VARCHAR(255),St_time TIME, End_time TIME,
                     PRIMARY KEY(Nssn), FOREIGN KEY (Dep_id) REFERENCES department(DepID))""")

mycursor.execute("DROP TABLE IF EXISTS examine")
mycursor.execute(""" CREATE TABLE examine( P_ssn INT, D_ssn INT, EXdate DATE, EXtime TIME, reason VARCHAR(255),
                     FOREIGN KEY (P_ssn) REFERENCES patients(Pssn), FOREIGN KEY (D_ssn) REFERENCES doctors(Dssn) )""")

mycursor.execute("DROP TABLE IF EXISTS prescriptions")
mycursor.execute(""" CREATE TABLE prescriptions ( presID INT, P_ssn INT,D_ssn INT,P_Date DATE, diagnose VARCHAR(255),
                    PRIMARY KEY(presID), FOREIGN KEY (P_ssn) REFERENCES patients(Pssn),
                    FOREIGN KEY (D_ssn) REFERENCES doctors(Dssn))""")


mycursor.execute("DROP TABLE IF EXISTS medications")
mycursor.execute(""" CREATE TABLE medications( Mname VARCHAR(255), t_per_day INT, pres_id INT, start_date DATE, end_date DATE,
                    M_No INT,PRIMARY KEY(M_No), FOREIGN KEY (pres_id) REFERENCES prescriptions(presID))""")

mycursor.execute("DROP TABLE IF EXISTS Medical_Procedures")
mycursor.execute(""" CREATE TABLE  Medical_Procedures (MP_No INT, pres_id INT,MP_Name VARCHAR(255),Type VARCHAR(255), PRIMARY KEY(MP_No),
                    FOREIGN KEY (pres_id) REFERENCES prescriptions(presID))""")

mycursor.execute("INSERT INTO department (Dep_name, DepID) VALUES ('cardiology','1')")
mycursor.execute("""INSERT INTO admin (Ad_ssn, Ad_password, Ad_Fname ,Ad_Lname) VALUES ('1','123','Ayman','Anwar')""")
mydb.commit()
