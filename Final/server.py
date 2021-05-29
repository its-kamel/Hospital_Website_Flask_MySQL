from flask import Flask,render_template,request,url_for,redirect,send_from_directory

import datetime  
from datetime import date 
import calendar 
import re
import os

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="CardiologyDep"
)
mycursor = mydb.cursor()



def convert_to_RFC_datetime(year, month, day, hour, minute):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
   
def findDay(date): 
    year , month, day = (int(i) for i in date.split('-'))     
    born = datetime.date(year, month, day) 
    return born.strftime("%A")
 
def get_doctors():
   Doctor_FNames=[]
   Doctor_LNames=[]
   Doctor_SSN = []
   Dnames=[]
   mycursor.execute('SELECT * FROM doctors')
   doctors = mycursor.fetchall()

   for doctor in doctors:
      Doctor_FNames.append(doctor[0])
      Doctor_LNames.append(doctor[1])
      Doctor_SSN.append(doctor[3])

   for fname,lname,dssn in zip(Doctor_FNames,Doctor_LNames,Doctor_SSN):
      Dnames.append('Dr. ' + fname+' '+lname+' '+ ' - ' + str(dssn))
   return Dnames





app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
global fnm
global R1 
global R2
global R3
global R4
global R5 
global ct
global cn
global finalfn
global finalln
R1=0 
R2=0 
R3=0 
R4=0 
R5=0
ct=[]
cn=[]
finalfn=[]
finalln=[]





@app.route('/',methods=['GET','POST'])
def home():
   
   ispatient=False
   isadmin=False
   isdr=False
   isnurse=False
   if request.method=="POST":
      ssn= request.form['SSN']
      passward=request.form['pass']
      global ssn2             #global variable carrying the current signed in ssn
      ssn2=int(ssn)
    
      #patient check sign in
      mycursor.execute("SELECT Pssn FROM patients WHERE Pssn=%s AND P_password=%s" ,(ssn2,passward,))
     
      patresult=mycursor.fetchall()
      if  patresult:
         ispatient=True
         
         

      
          
#admin check in sign in
      mycursor.execute("SELECT Ad_ssn FROM Admin WHERE Ad_ssn=%s AND  Ad_password=%s ",(ssn2,passward,))
      adminresult=mycursor.fetchall()
      if adminresult:
          isadmin=True

     
          
#doctor check in sign in
      mycursor.execute("SELECT Dssn FROM doctors WHERE Dssn=%s AND D_password=%s", (ssn2,passward,))
      docresult=mycursor.fetchall()
      if docresult:
          isdr=True

      
         
     # nurse check in sign in     
      mycursor.execute("SELECT Nssn FROM nurses WHERE Nssn=%s AND N_password=%s",(ssn2,passward,))
      nuresult=mycursor.fetchall()
      if nuresult:
         isnurse=True

      
          
      
       

      if(ispatient==True):
         return redirect("/Patient_Homepage")
      elif(isadmin==True):
         return redirect("/admin")
      elif(isdr==True):
         return redirect("/Doctor_Homepage")
      elif(isnurse==True):
         return redirect("/nurse")

      else:
             return redirect("/signup")
   
         
         
   else:
      return render_template("signin.html")



@app.route('/signup',methods=['Get','POST'])
def addpatient():
   if request.method=="POST":
      patFname=request.form['P_first_name']
      patLname=request.form['P_last_name']
      patssn=request.form['PSSNn']
      patadds=request.form['address']
      patgender=request.form['gender']
      patpasswd=request.form['user_password']
      patbdate=request.form['Bdate']
      patenrtydate=request.form['Edate']
      sql="INSERT INTO patients (Fname,Lname,Pssn,address,gender,P_password,P_bdate ,EnterDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
      val=(patFname,patLname,patssn,patadds,patgender,patpasswd,patbdate,patenrtydate)
      mycursor.execute(sql,val) 
      mydb.commit()
      return redirect("/")
   else:
      return render_template("signup.html")



@app.route('/Patient_Homepage/contact',methods=["GET",'POST'])
def contactus():
   if request.method =="POST":
      global complain
      global ssn_compl
      
      
   
      complain=request.form['contact']
      ssn_compl=request.form['complpainSSN']
      paswrd=request.form['pas']
      
      sql=("SELECT Pssn FROM patients Where Pssn= %s AND P_password=%s")
      val=(ssn_compl,paswrd,)
      mycursor.execute(sql,val)
      myresult=mycursor.fetchone()
      if myresult:
         ct.append(complain)
         cn.append(ssn_compl)
         return redirect("/Patient_Homepage")
      else:
       return redirect("/Patient_Homepage/contact")

   else:
       return render_template("contact.html")

   
@app.route('/Patient_Homepage',methods=['Get','POST'])
def Patient_homepage():
   if  request.method == "POST":
      rate=request.form['rate']
      if rate == '1':
         global R1
         R1+=1
      elif rate == '2':
         global R2
         R2+=1
      elif rate == '3':
         global R3
         R3+=1
      elif rate == '4':
         global R4
         R4+=1
      elif rate == '5':
         global R5
         R5+=1
      return redirect('/Patient_Homepage')

   else:

      sql1 = (""" SELECT Fname FROM patients WHERE Pssn = %s""")
      val1 = (ssn2,)
      mycursor.execute(sql1,val1)
      myresult1 = mycursor.fetchone()
      sql2 = (""" SELECT Lname FROM patients WHERE Pssn = %s """)
      val2 = (ssn2,)
      mycursor.execute(sql2,val2)
      myresult2 = mycursor.fetchone()
      return render_template("Patient_Homepage.html", fname = myresult1[0], lname = myresult2[0])
     

@app.route('/admin/complain',methods=['Get','POST'])
def complain_cont():
   checking=[]
 
   for x in cn:
       strings = [str(y) for y in x]
       a_string = "".join(strings)
       an_integer = int(a_string)
       sql1=("SELECT Fname FROM patients WHERE Pssn = %s")
       val1 = (an_integer,)
       mycursor.execute(sql1,val1)
       myresult1 = mycursor.fetchall()
       finalfn.append(myresult1)
       sql2=("SELECT Lname FROM patients WHERE Pssn = %s")
       val2 = (an_integer,)
       mycursor.execute(sql2,val2)
       myresult2 = mycursor.fetchall()
       finalln.append(myresult2)      
       
   for x in zip(cn,ct):
          checking.append("Patient with SSN: "+ str(x[0])+":  "+"  "+x[1]+"  ")

   if len(checking)>0:
      x=True
      return render_template("complain.html",cssn=cn,comp=checking)
      
      
   else:
      return redirect("/admin")

   
@app.route('/admin')
def ad():
   mycursor.execute("SELECT COUNT(Dssn) FROM doctors")
   myresult1 = mycursor.fetchone()
   mycursor.execute("SELECT COUNT(Pssn) FROM patients")
   myresult2 = mycursor.fetchone()
   mycursor.execute("SELECT COUNT(Nssn) FROM nurses")
   myresult3 = mycursor.fetchone()
   mycursor.execute("SELECT SUM(D_salary) FROM doctors")
   myresult4 = mycursor.fetchone()
   mycursor.execute("SELECT SUM(N_salary) FROM nurses")
   myresult5 = mycursor.fetchone()
   mycursor.execute("SELECT AVG(D_salary) FROM doctors")
   myresult6 = mycursor.fetchone()
   mycursor.execute("SELECT AVG(N_salary) FROM nurses")
   myresult7 = mycursor.fetchone()
   sql8 =(""" SElECT Ad_Fname FROM admin WHERE Ad_ssn = %s""")
   val8 =(ssn2,)
   mycursor.execute(sql8,val8)
   myresult8 = mycursor.fetchone()
   sql9 =(""" SElECT Ad_Lname FROM admin WHERE Ad_ssn = %s""")
   val9 =(ssn2,)
   mycursor.execute(sql9,val9)
   myresult9 = mycursor.fetchone()
   #male/female drs
   mycursor.execute(""" SELECT COUNT(Dssn) FROM doctors WHERE Dgender='female'""")
   FemD=mycursor.fetchone()
   mycursor.execute(""" SELECT COUNT(Dssn) FROM doctors WHERE Dgender='male'""")
   mD=mycursor.fetchone()
   #male/female nurse
   mycursor.execute(""" SELECT COUNT(Nssn) FROM nurses WHERE Ngender='female'""")
   FemN=mycursor.fetchone()
   mycursor.execute(""" SELECT COUNT(Nssn) FROM nurses WHERE Ngender='male'""")
   mN=mycursor.fetchone()
   #current year
   now = datetime.datetime.now()
   ysql="SELECT COUNT(Pssn) FROM patients WHERE year(EnterDate)=%s"
   yval=(now.year,)
   mycursor.execute(ysql,yval)
   EnterD = mycursor.fetchone()
   nsql="SELECT COUNT(P_ssn) FROM examine WHERE year(EXdate)=%s"
   nval=(now.year,)
   mycursor.execute(nsql,nval)
   ExD=mycursor.fetchone()
   dsql="SELECT COUNT(Dssn) FROM doctors WHERE year(Jdate)=%s"
   dval=(now.year,)
   mycursor.execute(dsql,dval)
   JD = mycursor.fetchone()
   return render_template("admin.html", Dcount=myresult1[0], Pcount=myresult2[0], Ncount=myresult3[0], Total_dsal=myresult4[0], 
                        Total_nsal=myresult5[0], AVG_dsal=myresult6[0], AVG_nsal=myresult7[0], fname=myresult8[0], lname=myresult9[0],
                        FD=FemD[0],MD=mD[0],FN=FemN[0],MN=mN[0],r1=R1,r2=R2,r3=R3,r4=R4,r5=R5, newP=EnterD[0], newE=ExD[0], newD=JD[0])


@app.route('/admin/Dadmin', methods=['POST'])
def addDoctor():
   fname = request.form['docFname']
   lname = request.form['docLname']
   dssn = request.form['docSSN']
   password = request.form['pass']
   Gender = request.form['gender']
   bdate = request.form['Bdate']
   depID = request.form['depID']
   jndate = request.form['jdate']
   day = request.form['day']
   stime = request.form['start']
   etime = request.form['end']
   sal = request.form['salary']
   Dsql = """INSERT INTO doctors (D_Fname, D_Lname, Dssn, D_password, Dgender, D_bdate, Dep_id, Jdate, day,St_time,End_time, D_salary) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   Dval = (fname,lname,dssn,password,Gender,bdate,depID,jndate,day,stime,etime,sal)
   mycursor.execute(Dsql,Dval)
   mydb.commit()
   return redirect("/admin")


@app.route('/admin/Dadmin', methods=['GET'])
def viewDoctor():
   mycursor.execute("SELECT * FROM doctors")
   myresult = mycursor.fetchall()
   return render_template("Dadmin.html", doctorsData= myresult)


@app.route('/admin/Nadmin', methods=['POST'])
def addNurse():
   N_fname = request.form['NFname']
   N_lname = request.form['NLname']
   nssn = request.form['NSSN']
   npass = request.form['Npass']
   ngender = request.form['Ngender']
   dID = request.form['depid']
   Nsal = request.form['Nsalary']
   day = request.form['day']
   st = request.form['st']
   et = request.form['et']
   Nsql = """ INSERT INTO nurses (N_Fname, N_Lname, Ngender, Nssn, N_salary, N_password, Dep_id, day,St_time,End_time)  
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   Nval = (N_fname, N_lname, ngender, nssn, Nsal, npass, dID, day, st, et)
   mycursor.execute(Nsql,Nval)
   mydb.commit()
   return redirect("/admin")

@app.route('/admin/Nadmin', methods=['GET'])
def viewNurse():
   mycursor.execute("SELECT * FROM nurses")
   myresult = mycursor.fetchall()
   return render_template("Nadmin.html", nursesData= myresult)


@app.route('/admin/Aadmin', methods=['POST'])
def addAdmin():
   fname = request.form['Fname']
   lname = request.form['Lname']
   ssn = request.form['ASSN']
   apass = request.form['Apass']
   Asql = """ INSERT INTO admin (Ad_ssn, Ad_password, Ad_Fname, Ad_Lname) VALUES (%s,%s,%s,%s)"""
   Aval = (ssn,apass,fname,lname)
   mycursor.execute(Asql,Aval)
   mydb.commit()
   return redirect("/admin")


@app.route('/admin/Aadmin', methods=['GET'])
def viewAdmin():
   mycursor.execute("SELECT * FROM admin")
   myresult= mycursor.fetchall()
   return render_template("Aadmin.html", adminsData = myresult)


@app.route('/admin/Rdoctor', methods=['GET',"POST"])
def Remove_doctor():
   if request.method=="POST":
      sn= request.form['drsn']
      sql2="DELETE FROM examine WHERE D_ssn=%s"
      val2=(sn,)
      mycursor.execute(sql2,val2)
      mydb.commit()
      sql1="DELETE FROM doctors WHERE Dssn= %s "
      val1=(sn,)
      mycursor.execute(sql1,val1)
      mydb.commit()

      return redirect("/admin")
   else:
      return render_template("Rdoctor.html")


   

@app.route('/admin/Rnurse', methods=['GET',"POST"])
def Remove_nurse():
    if request.method=="POST":
      sn= request.form['nsn']
      sql="DELETE FROM nurses WHERE Nssn= %s "
      val=(sn,)
      mycursor.execute(sql,val)
      mydb.commit()
      return redirect("/admin")
    else:
      return render_template("Rnurse.html")


@app.route('/admin/Radmin', methods=['GET',"POST"])
def Remove_Admin():
    if request.method=="POST":
      sn= request.form['adsn']
      sql="DELETE FROM Admin WHERE Ad_ssn= %s "
      val=(sn,)
      mycursor.execute(sql,val)
      mydb.commit()
      return redirect("/admin")
    else:
      return render_template("Radmin.html")
  

@app.route("/nurse")
def nur():
   sql1 =("""SELECT day,St_time,End_time FROM  nurses WHERE Nssn = %s """)
   val1 =(ssn2,)
   mycursor.execute(sql1,val1)
   myresult1 = mycursor.fetchall()
   sql2 =(""" SElECT N_Fname FROM nurses WHERE Nssn = %s""")
   val2 =(ssn2,)
   mycursor.execute(sql2,val2)
   myresult2 = mycursor.fetchone()
   sql4 =(""" SElECT N_Lname FROM nurses WHERE Nssn = %s """)
   val4 =(ssn2,)
   mycursor.execute(sql4,val4)
   myresult4 = mycursor.fetchone()
   return render_template("nurse.html",shiftsData=myresult1,name=myresult2[0],lname=myresult4[0])




@app.route('/Patient_appointment',methods=['GET','POST'])
def Patient_appointment():
   if request.method == "POST":
      Patient_SSN=ssn2
      Name= request.form['D_Name']
      Enter_date= request.form['Entry_date']
      Hour= request.form['Entry_time']
      Reason= request.form['P_reason']
      day = findDay(Enter_date)
      Doctor_SSN=re.findall('[A-zA-Z].- ([0-9].*)',Name)
      mycursor.execute('SELECT D_Fname FROM doctors WHERE %s BETWEEN St_time AND End_time AND day = %s AND Dssn = %s',(Hour,day,Doctor_SSN[0]))
      myresult = mycursor.fetchall()
      available_doctors=len(myresult)
      mycursor.execute('SELECT Fname, Lname, address FROM patients WHERE Pssn = %s',(ssn2,))
      myresult = mycursor.fetchall()
      full_name= str(myresult[0][0])+' '+str(myresult[0][1])
      if available_doctors != 0:
         mycursor.execute(""" INSERT INTO examine (P_ssn,D_ssn,EXdate,EXtime,reason) VALUES (%s,%s,%s,%s,%s)""",(Patient_SSN,Doctor_SSN[0],Enter_date,Hour,Reason))
         mydb.commit()
        
         from datetime import datetime, timedelta
         from cmain import get_calendar_service
         import datetime  
         from datetime import date 

         service = get_calendar_service()

         #convert from string to date
         date_string = "".join(Enter_date)
         format_strd = '%Y-%m-%d' # Date Format
         date = datetime.datetime.strptime(date_string, format_strd) 

         #convert from string to time
         time_string = "".join(Hour)
         format_strt = '%H:%M' # Time Format
         time = datetime.datetime.strptime(time_string, format_strt)
         

         hour_adjustment = -2
   
         duration = 60
         ftime = time + timedelta(minutes=duration)

         ftime = ftime + timedelta(hours=hour_adjustment)
         

         if time.hour == 1 :
            time = datetime.datetime(time.year, time.month, time.day , 23, time.minute, 0)
            ftime = datetime.datetime(ftime.year, ftime.month, ftime.day, 0, ftime.minute, 0)
            
         else:
            time = datetime.datetime(time.year, time.month, time.day, time.hour+hour_adjustment, time.minute, 0)


         service.events().insert(calendarId='primary',
          body={
           "summary": 'Appointment',
           "description": 'Appointment for {}'.format(full_name),
           "start": {
              "dateTime": convert_to_RFC_datetime (date.year, date.month, date.day, time.hour , time.minute), 
              "timeZone": 'GMT'
            },
           "end": { 
              "dateTime": convert_to_RFC_datetime (date.year, date.month, date.day, ftime.hour, ftime.minute), 
              "timeZone": 'GMT'
            },
         }
         ).execute()
         return render_template("Patient_appointment.html",sc_msg = "Appointement Set !",Dlist= get_doctors(),PSSN =ssn2)
      else:
         return render_template("Patient_appointment.html", er_msg = "Doctor not Available" , Dlist= get_doctors(),PSSN =ssn2)
   else:
      
      return render_template("Patient_appointment.html", df_msg = "Look for your Doctor Now !!", Dlist= get_doctors(),PSSN =ssn2)
   
   
@app.route('/Patient_viewDoctors')
def patient_view():
   mycursor.execute("SELECT D_Fname,D_Lname,day,St_time,End_time FROM doctors")
   myresult = mycursor.fetchall()
   return render_template("Patient_viewDoctors.html",doctorsData=myresult)

@app.route("/Patient_Homepage/upload", methods=['GET','POST'])
def upload():
   if request.method == "POST":
      target = os.path.join(APP_ROOT, 'Scans/')

      if not os.path.isdir(target):
         os.mkdir(target)

      for file in request.files.getlist("file"):
         filename = file.filename
         global fnm
         fnm=filename
         destination = "/".join([target, filename])
         file.save(destination)
         with open(destination, 'rb') as file:
            binaryData = file.read()
         mycursor.execute("UPDATE patients SET Scans= %s WHERE Pssn = %s",(binaryData,ssn2))
         mydb.commit()
      return render_template("viewscan.html",oppa=fnm)
   else:
      return render_template("upload.html")

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("Scans", filename)


@app.route("/Patient_Homepage/viewscan", methods=['GET','POST'])
def view():
   global fnm
   try:
      return render_template("viewscan.html",oppa=fnm)
   except:
      return render_template("signin.html")

@app.route("/Doctor_viewscan", methods=['GET','POST'])
def Doctor_viewscan():
   global fnm
   try:
      return render_template("Doctor_viewscan.html",oppa=fnm)
   except:
      return render_template("signin.html")
  
@app.route("/Doctor_download", methods=['GET','POST'])
def Doctor_download():
   patID=pid
   mycursor.execute("Select Scans FROM patients WHERE Pssn =%s",(patID,))
   image = mycursor.fetchall()
   if image[0][0] != None:
      desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
      target = os.path.join(desktop,'Your_Scans/')
      if not os.path.isdir(target):
         os.mkdir(target)
      destination = "/".join([target, 'Scan.JPG'])
      with open(destination, 'wb') as file:
         try:
            file.write(image[0][0])
         except:
            return render_template("signin.html")
      return redirect("/Doctor_Homepage")
   return render_template("signin.html")


@app.route("/download", methods=['GET','POST'])
def download():
      mycursor.execute("Select Scans FROM patients WHERE Pssn =%s",(ssn2,))
      image = mycursor.fetchall()
      if image[0][0] != None:
         desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
         target = os.path.join(desktop,'Your_Scans/')

         if not os.path.isdir(target):
               os.mkdir(target)
         destination = "/".join([target, 'Scan.JPG'])
         with open(destination, 'wb') as file:
            try:
               file.write(image[0][0])
            except:
               return render_template("signin.html")
         return redirect("/Patient_Homepage")
      return render_template("signin.html")

@app.route('/Doctor_Homepage', methods=['GET'])
def Doctor_homepage():
   id=ssn2
   global key
   key=0
   sql = ("SELECT D_Fname FROM doctors WHERE Dssn = %s")
   val = (id,)
   mycursor.execute(sql,val)
   myresult = mycursor.fetchone()
   sql1 = ("SELECT D_Lname FROM doctors WHERE Dssn = %s")
   val1 = (id,)
   mycursor.execute(sql1,val1)
   myresult1 = mycursor.fetchone()
   return render_template("Doctor_Homepage.html", D_Fname = myresult[0], D_Lname = myresult1[0])

@app.route('/Doctor_Prescription' ,methods = ['POST', 'GET'])
def Doctor_Prescription():
   if request.method == 'POST':
      D_ID=ssn2
      P_ID = request.form['Patient ID']
      #p_date = request.form['Prescription Date']
      today=date.today()
      p_date= today.strftime('%Y/%m/%d')
      #p_date = today().date()
      Diagnose = request.form['Diagnose']
      mycursor.execute("SELECT COUNT(presID) FROM prescriptions") 
      PresID = mycursor.fetchone() [0]+1
      pid=int(P_ID)
      mycursor.execute("SELECT Pssn FROM patients ")
      myresult=mycursor.fetchall()
      cm=0
      cond1=0
      for x in myresult:
         strings = [str(y) for y in x]
         a_string = "".join(strings)
         an_integer = int(a_string)
         if(an_integer==pid):
            cm=cm+1
      if (cm!=0):
         sql = "INSERT INTO prescriptions (P_date,diagnose,presID,P_ssn,D_ssn) VALUES (%s, %s,%s,%s,%s)"
         val = (p_date,Diagnose,PresID,P_ID,D_ID)
         mycursor.execute(sql, val) 
         mydb.commit() 
         global presid
         presid = PresID
         return redirect('/Doctor_sh')
      else:
         cond1 = 1   
         return render_template('Doctor_Prescription.html', msg="The ID you have entered does not exist", condition1=cond1 )
   else:
      return render_template('Doctor_Prescription.html')

@app.route('/Doctor_sh',methods = ['POST', 'GET'])
def Doctor_sh():
   if request.method == 'GET':
      id=presid
      sql=("SELECT P_date,diagnose FROM prescriptions WHERE presID = %s")
      val=(id,)
      mycursor.execute(sql,val) 
      myresult = mycursor.fetchall()
      sql1=("SELECT Mname,t_per_day,start_date,end_date FROM medications WHERE pres_id = %s")
      val1=(id,)
      mycursor.execute(sql1,val1) 
      myresult1 = mycursor.fetchall()
      sql2=("SELECT MP_Name,Type FROM medical_procedures WHERE pres_id = %s")
      val2=(id,)
      mycursor.execute(sql2,val2) 
      myresult2 = mycursor.fetchall()
      return render_template('Doctor_sh.html', Prescriptions=myresult, Medications=myresult1, Medicalprocedures=myresult2)
   else:
      return render_template('Doctor_sh.html')
          

@app.route('/Doctor_Medications',methods = ['POST', 'GET'])
def Doctor_Medications():
   if request.method == 'POST':
      presID=presid
      MN = request.form['Medication Name']
      TPD = request.form['Dosage Per Day']
      SD = request.form['Start Date']
      ED = request.form['End Date']
      mycursor.execute("SELECT COUNT(M_No) FROM medications") 
      Mno = mycursor.fetchone() [0] + 1
      sql = "INSERT INTO medications (Mname,t_per_day,pres_id,start_date,end_date,M_No) VALUES (%s, %s,%s,%s, %s,%s)"
      val = (MN,TPD,presID,SD,ED,Mno)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('Doctor_Medications.html')
   else:
      return render_template('Doctor_Medications.html')

@app.route('/Doctor_Medicalprocedures',methods = ['POST', 'GET'])
def Doctor_Medicalprocedures():
   if request.method == 'POST':
      presID=presid
      MPN = request.form['Medical Procedures Name']
      MPT = request.form['Medical Procedures Type']
      mycursor.execute("SELECT COUNT(MP_No) FROM medical_procedures") 
      MP = mycursor.fetchone() [0] + 1
      sql = "INSERT INTO medical_procedures (MP_No,pres_id,MP_Name,Type) VALUES (%s, %s,%s,%s)"
      val = (MP,presID,MPN,MPT)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('Doctor_Medicalprocedures.html')
   else:
      return render_template('Doctor_Medicalprocedures.html')

@app.route('/Doctor_Appointments',methods = ['GET'])
def Doctor_Appointments():
   D_ID=ssn2
   sql=("SELECT Fname, Lname, EXdate, EXtime FROM examine JOIN patients ON examine.p_ssn = patients.Pssn WHERE D_ssn = %s")
   val=(D_ID,)
   mycursor.execute(sql,val) 
   myresult = mycursor.fetchall()
   return render_template('Doctor_Appointments.html', Appointments=myresult)
   

@app.route('/DoctorsPatient_Examination',methods=['GET','POST'])
def DoctorsPatient_Examination():
   if request.method=="POST":
      idi= request.form['Patients_pssn']
      id=int(idi)
      mycursor.execute("SELECT Pssn FROM patients ")
      myresult0=mycursor.fetchall()
      c=0
      cond=0
      for x in myresult0:
         strings = [str(y) for y in x]
         a_string = "".join(strings)
         an_integer = int(a_string)
         if(an_integer==id):
            c=c+1
      if (c!=0):
         global pid
         pid=id
         sql0=" SELECT Fname,Lname,EnterDate,gender,P_bdate FROM patients WHERE patients.Pssn=%s"
         val0=(id,)
         mycursor.execute(sql0,val0)
         patientinfo = mycursor.fetchall()
         val=(id,)
         sql ="SELECT Mname,t_per_day,start_date,end_date  FROM patients JOIN prescriptions ON patients.Pssn=prescriptions.P_ssn JOIN medications ON prescriptions.presID=medications.pres_id WHERE patients.Pssn=%s"
         mycursor.execute(sql, val)
         myresult = mycursor.fetchall()
         sql1 ="SELECT P_Date, MP_Name, Type  FROM patients JOIN prescriptions ON patients.Pssn=prescriptions.P_ssn JOIN medical_procedures ON prescriptions.presID=medical_procedures.pres_id WHERE patients.Pssn=%s"
         mycursor.execute(sql1, val)
         myresult1 = mycursor.fetchall()
         sql2="SELECT diagnose,P_date FROM patients JOIN prescriptions ON patients.Pssn=prescriptions.P_ssn WHERE patients.Pssn=%s"
         mycursor.execute(sql2,val)
         diagnoss=mycursor.fetchall()
         return  render_template("Doctor_ph.html",medication=myresult,patient=patientinfo,diagnosesinfo=diagnoss, medicalpro=myresult1, msg="") 
      else:  
         cond=1
         return render_template('DoctorsPatient_Examination.html', msg="The ID you have entered does not exist", condition=cond)
   else:
      return render_template("DoctorsPatient_Examination.html")


if __name__ == '__main__':
   app.run(host='127.0.0.1', port=80)