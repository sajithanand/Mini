
#from crypt import methods
from urllib import request
from flask import *
app.secret_key="abc"
from dbconnection import *
from datetime import datetime
app=Flask(__name__)
app.secret_key="444"
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/aboutus')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route('/login')
def log():
    return render_template("login2.html")

#login function
@app.route('/login', methods=['post'])
def login():
    username=request.form['username']
    password=request.form['password']
    qry=" SELECT * FROM login WHERE username=%s and password=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("invalid");window.location="login_index"</script>'''
    elif res['usertype'] == "admin":
        return '''<script>alert("valid");window.location="admin"</script>'''
    elif res['usertype'] == "patient":
        session['lid']=res['login_id'] #getting patient id from login function
                    
        return '''<script>alert("valid");window.location="Patienthome"</script>'''
    elif res['usertype'] == "Doctor":
        return '''<script>alert("valid");window.location="Doctor"</script>'''
    elif res['usertype'] == "Nurse":
        return '''<script>alert("valid");window.location="Nurse"</script>'''
    elif res['usertype'] == "Pharmacist":
        return '''<script>alert("valid");window.location="Pharmacist"</script>'''
    else:
        return '''<scrpit>alert("invalid");window.location="login"</script>'''

#Registration Function
@app.route('/registration', methods=['post'])
def registration():
    name=request.form['fname']
    home=request.form['home']
    place=request.form['place']
    city=request.form['city']
    pincode=request.form['pin']
    Bloodgroup=request.form['Blood_group']
    Gender=request.form['gender']
    age=request.form['age']
    Email=request.form['email']
    DOB=request.form['dob']
    Phone=request.form['phone']
    username=request.form['user']
    password=request.form['password']
    
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'patient')"
    val=(username,password)
    id=iud(qry,val)
   
    qry1="INSERT INTO `patient details` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1=(str(id),name,home,place,city,pincode,Gender,Bloodgroup,Email,DOB,Phone,age)
    iud(qry1,val1)
    return '''<script>alert("Registerd successfuly");window.location="/"</script>'''
    
@app.route("/register")
def register():
    return render_template("Patient/register (2).html")

#Admin Home page
@app.route('/admin')
def admin_home():
    return render_template("admin_home1.html")

#Add Doctor schedule
@app.route("/Add_schedule")
def schedule():
    q="SELECT * FROM `time_slot`"
    res=selectall(q)
    d=datetime.now().strftime("%Y-%m-%d")
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    re=selectall(qr)
    return render_template("add_schedule.html",val=res,val1=re,d=d)

@app.route("/Add_schedule1",methods=['post'])
def schedule1():
    doctor=request.form['select']
    Time=request.form['select2']
    Date=request.form['textfield']
    strength=request.form['textfield2']

    qry1="INSERT INTO `doctor_schedule` VALUES(NULL,%s,%s,%s,%s)"
    val=(Time,doctor,Date,strength)
    iud(qry1,val)

    return '''<script>alert("Registerd successfully");window.location="manage_schedule"</script>'''    
    
    


#Manage doctor schedule
@app.route("/manage_schedule")
def man_schedule():
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    re=selectall(qr)
    return render_template("manage_schedule.html",val1=re)

@app.route("/search_schedule",methods=['post'])
def search_schedule():
    did=request.form['select']
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    re=selectall(qr)
    qr="SELECT `time_slot`.*,`doctor_schedule`.* FROM `doctor_schedule` JOIN `time_slot` ON `time_slot`.`Tid`=`doctor_schedule`.`tid` WHERE `doctor_schedule`.`Emp_id`=%s"
    res=selectall2(qr,did)
    return render_template("manage_schedule.html",val1=re,val=res)

#Add Doctor schedule
@app.route("/Edit_schedule")
def Edit_schedule():
    id=request.args.get('id')
    session['ES_id']=id
    q="SELECT * FROM `time_slot`"
    res1=selectall(q)

    qry= "SELECT * FROM `doctor_schedule` WHERE sch_id=%s"
    res=selectone(qry,str(id))
    print(res)

    return render_template("editSchedule.html",val=res,val1=res1)



@app.route("/Edit_schedule1",methods=['post'])
def edit_1():
    Time=request.form['select2']
    Date=request.form['textfield']
    strength=request.form['textfield2']

    qry1="UPDATE `doctor_schedule` set `tid`=%s,`Date`=%s,`strength`=%s WHERE `sch_id`=%s"
    val=(Time,Date,strength,session['ES_id'])
    iud(qry1,val)

    return '''<script>alert("updated successfully");window.location="manage_schedule"</script>'''


@app.route("/delete_schedule")
def delete_schedule():
    id=request.args.get('id')
    
    

    qry= "delete FROM `doctor_schedule` WHERE sch_id=%s"
    iud(qry,str(id))

    return '''<script>alert("deleted successfully");window.location="manage_schedule"</script>'''


#Add Staff Data
@app.route("/AddstaffData",methods=['post'])
def AddstaffData():
    name=request.form['textfield']
    home=request.form['textfield2']
    place=request.form['textfield3']
    city=request.form['textfield4']
    pincode=request.form['textfield5']
    Age=request.form['textfield6']
    Gender=request.form['RadioGroup1']
    Experience=request.form['textfield8']
    Specialization=request.form['textfield9']
    Designation=request.form['select']
    Licensenumber=request.form['textfield11']
    username=request.form['textfield12']
    password=request.form['textfield13']
    image=request.files['file']
    filname=secure_filename(image.filename)
    image.save(os.path.join('static/doctorimages',filname))



    if Designation=="1":
    
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Doctor')"
        val=(username,password)
        id=iud(qry,val)

        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,Licensenumber,filname)
        iud(qry1,val1)
        return '''<script>alert("Registerd successfully");window.location="/"</script>'''
    elif Designation=="2":
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Pharmacist')"
        val=(username,password)
        id=iud(qry,val)

        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'null','available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,Licensenumber)
        iud(qry1,val1)
        return '''<script>alert("Registerd successfully");window.location="/"</script>'''
    else:
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Nurse')"
        val=(username,password)
        id=iud(qry,val)
        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'null','available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,Licensenumber)
        iud(qry1,val1)
        return '''<script>alert("Registerd successfully");window.location="/login"</script>'''

@app.route("/Addstaff1")
def Addstaff():
    return render_template("AddStaffData.html")
   
#View Staff Data
@app.route('/View Staff Data', methods=['get'])
def Staffview():
    qry = "SELECT * FROM `addstaffdata`"
    res=selectall(qry)
    return render_template('ViewStaffData.html',val=res)    

@app.route("/Activate")
def activate():
    id=request.args.get('id')
    q="UPDATE `addstaffdata` SET `Status`='Available' WHERE `E_id`=%s"
    iud(q,str(id))
    return '''<script>alert("updated successfully");window.location="View Staff Data"</script>'''

@app.route("/Inactivate")
def inactivate():
    id=request.args.get('id')
    q="UPDATE `addstaffdata` SET `Status`='Unavailable' WHERE `E_id`=%s"
    iud(q,str(id))
    return '''<script>alert("updated successfully");window.location="View Staff Data"</script>'''



#Manage vaccine schedule
@app.route("/vaccine_schedule")
def vaccine_schedule():
    q="SELECT *FROM `vaccine_table` "
    res=selectall(q)
    d=datetime.now().strftime("%Y-%m-%d")
    qr="SELECT * FROM `time_slot`"
    res1=selectall(qr)
    return render_template("Vaccine_schedule.html",val=res,val1=res1,d=d)

    
@app.route("/addvaccine_schedule",methods=['post'])
def addvaccine_schedule():
    Vaccine_name=request.form['select']
    Time=request.form['select2']
    Date=request.form['textfield']
    Strength=request.form['textfield2']
    

    q="INSERT INTO vaccine_schedule VALUES(NULL,%s,%s,%s,%s)"
    v=(Time,Vaccine_name,Date,Strength)
    res=iud(q,v)
    return '''<script>alert("Vaccine added successfully");window.location="vaccine_schedule"</script>'''




#View Doctor booking
@app.route("/View_booking")
def BOOK():
    qry = "SELECT `patient details`.`Name`,`addstaffdata`.`Name` AS drname,`doctor_schedule`.`Date`,`time_slot`.`Start time`,`End time` FROM `patient details` JOIN `booking_for_doctor` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` JOIN `doctor_schedule` ON `booking_for_doctor`.`sch_id`=`doctor_schedule`.`sch_id` JOIN `time_slot` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` JOIN `addstaffdata` ON `doctor_schedule`.`Emp_id`=`addstaffdata`.`login id` WHERE `addstaffdata`.`Designation`=1"
    res = selectall(qry)
    return render_template("ViewBooking.html",val=res)


#View vaccine booking
@app.route("/View_book")
def BOOKING():
   
    q="SELECT `booking_for_vaccination`.*,`patient details`.`Name` AS pname,`vaccine_table`.`Name`,`vaccine_schedule`.`Date`,`time_slot`.* FROM `time_slot` JOIN `vaccine_schedule` ON `vaccine_schedule`.`Tid`=`time_slot`.`Tid` JOIN `vaccine_table` ON `vaccine_table`.`vd_id`=`vaccine_schedule`.`Vac_id` JOIN `booking_for_vaccination` ON `booking_for_vaccination`.`Vsch_id`=`vaccine_schedule`.`Vsch_id` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_vaccination`.`Pat_id`"
    res=selectall(q)

    return render_template("ViewVaccineBooking.html",val=res)
    

    

#Add Vaccine Details
@app.route('/Vaccine Details', methods=['post'])
def add_vaccine():
    name=request.form['textfield2']
    description=request.form['textfield']

    qry1="INSERT INTO `vaccine_table` VALUES(NULL,%s,%s,'available')"
    val1=(name,description)
    iud(qry1,val1)
    return '''<script>alert("Registered successfuly");window.location="/admin"</script>'''

@app.route("/Viewvaccine")
def Vaccine():
    return render_template("VaccineDetails.html")

    

@app.route("/View Vaccine Booking")
def Vaccine_booking():
    return render_template("ViewVaccineBooking.html")

#View feedback function
@app.route("/View Feedback")
def View_feedback():
    qry="SELECT `feedback_table`.*,`patient details`.* FROM `feedback_table` JOIN `patient details` ON `feedback_table`.`pid`=`patient details`.`Login id`"
    res=selectall(qry)
    print(res)
    return render_template("ViewFeedback.html",data=res)

#sent notification
@app.route("/Sent_Notification")
def Sent_notification():
    return render_template("SentNotification.html")

@app.route('/snt_not', methods=['post'])
def snt_not():
    notification=request.form['textfield']
    q="INSERT INTO notification VALUES(NULL,CURDATE(),%s)"
    res=iud(q,notification)
    return '''<script>alert("Sent successfully");window.location="/Sent_Notification"</script>'''


#Patient Home
@app.route("/Patienthome")
def Patient_home():
    return render_template("Patient_home1.html")

#update Profile function
@app.route("/updprof")
def updprof():
    q1 = "SELECT * FROM `patient details` WHERE `patient details`.`Login id`=%s"
    res=selectone(q1,session['lid'])
    print(res,"hhhhhhhhhhhhhhhhhhhhhh")
    return render_template("Patient/UPDATE PROFILE.html",val=res)

   

    

@app.route("/updpro",methods=['post','get'])
def updpro():
    Name = request.form['nam']
    Home = request.form['hom']
    Place = request.form['pla']
    City = request.form['cit']
    pincode = request.form['pin']
    Gender = request.form['Radio']
    Blood_group= request.form['blood']
    Email= request.form['mail']
    Date_of_Birth= request.form['birth']
    Phone= request.form['phone']
    Age = request.form['ag']


    
    qry1 = "UPDATE `patient details` SET `Name`=%s,`Home`=%s,`place`=%s,`City`=%s,`Pincode`=%s,`Gender`=%s,`Blood_Group`=%s,`Email`=%s,`Phone_number`=%s,`Date_of_birth`=%s,`Age`=%s WHERE `Login id`=%s"
    val1 = (Name,Home,Place,City,pincode,Gender,Blood_group,Email,Date_of_Birth,Phone,Age,session['lid'])
    iud(qry1, val1)
    return '''<script>alert("profile updated successfuly");window.location="Patienthome"</script>'''



@app.route("/DoctorBooking")
def DoctorBooking():
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    res=selectall(qr)
    
    return render_template("Patient/Doctor Booking.html",val=res)

@app.route("/Doctor Booking1")
def DocotrBooking1():
    id=request.args.get('id')
    d=datetime.now().strftime("%Y-%m-%d")
    session['dlid']=id
    return render_template("Patient/Doctor Booking1.html",d=d)

@app.route("/search_schd",methods=['post'])
def search_schd():
    date=request.form['textfield']
    d=datetime.now().strftime("%Y-%m-%d")
    qr="SELECT `time_slot`.*,`doctor_schedule`.*  FROM `time_slot` JOIN `doctor_schedule` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` WHERE `doctor_schedule`.`Emp_id`=%s AND `doctor_schedule`.`Date`=%s"
    val=(session['dlid'],date)

    res=selectall2(qr,val)
    return render_template("Patient/Doctor Booking1.html",val=res,d=d)

@app.route("/doctorbook")
def doctorbook():
    id=request.args.get('id')
    q="SELECT `strength` FROM `doctor_schedule` WHERE `sch_id`=%s"
    res=selectone(q,str(id))
    print(res,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    if res['strength']==0:
        return '''<script>alert("booking closed");window.location="DoctorBooking"</script>'''

    else:
        q="INSERT INTO `booking_for_doctor` VALUES(NULL,%s,%s,'book')"   
        v=(session['lid'],str(id))
        iud(q,v)
        qr="UPDATE `doctor_schedule` SET `strength`=`strength`-1 WHERE `sch_id`=%s" 
        iud(qr,str(id))
        return '''<script>alert("booking success");window.location="DoctorBooking"</script>'''


#Vaccine Booking Function

@app.route("/VaccineBook")
def VaccineBook():
    qry="SELECT *FROM `vaccine_table` "
    res=selectall(qry)
    return render_template("Patient/Book_vaccine1.html",val=res)

@app.route("/VaccineBook1")
def VaccineBook1():
    id=request.args.get('id')
    d=datetime.now().strftime("%Y-%m-%d")
    session['vid']=id
    return render_template("Patient/Book_vaccine2html.html",d=d)

@app.route("/VaccineBook2")
def VaccineBook2():
    return render_template("Patient/Book_vaccine3.html")


@app.route("/search_schd1",methods=['post'])
def search_schd1():
    date=request.form['textfield']
    d=datetime.now().strftime("%Y-%m-%d")
    qr="SELECT `time_slot`.*,`vaccine_schedule`.* FROM `time_slot` JOIN `vaccine_schedule` ON `vaccine_schedule`.`Tid`=`time_slot`.`Tid` WHERE `vaccine_schedule`.`Date`=%s AND  `vaccine_schedule`.`Vac_id`=%s"
    val=(date,session['vid'])

    res=selectall2(qr,val)
    print(res)
    return render_template("Patient/Book_vaccine2html.html",val=res,d=d)

@app.route("/vaccinebook2")
def vaccineboo2():
    id=request.args.get('id')
    session['vschid']=id
    d=datetime.now().strftime("%Y-%m-%d")
    return render_template("Patient/Book_vaccine3.html",d=d)



@app.route("/vaccinebook3",methods=['post'])
def vaccinebook3():
    dose=request.form['textfield']
    q="SELECT `Strength` FROM `vaccine_schedule` WHERE `Vsch_id`=%s"
    res=selectone(q,session['vschid'])
    
    if res['Strength']==0:
        return '''<script>alert("booking closed");window.location="VaccineBook2"</script>'''

    else:
        q="INSERT INTO `booking_for_vaccination` VALUES(NULL,%s,%s,%s,'pending')"   
        v=(session['vschid'],session['lid'],dose)
        iud(q,v)
        qr="UPDATE vaccine_schedule SET `Strength`=`Strength`-1 WHERE `Vsch_id`=%s" 
        iud(qr,session['vschid'])
        return '''<script>alert("booking success");window.location="Patienthome"</script>'''




@app.route("/View prescription")
def view():
    return render_template("Patient/ViewPrescription.html")






#Add Feeedback Function
@app.route("/Add_feedbac",methods=['post'])
def Add_feed():
    feedback=request.form['textfield']

    qry1="INSERT INTO `feedback_table` VALUES(NULL,%s,CURDATE(),%s)"
    val=(session['lid'],feedback)
    iud(qry1,val)
    return '''<script>alert("feedback added succesfully");window.location="Patienthome"</script>'''

@app.route("/Add_feedback")
def Add_feedback():
    return render_template("Patient/SendFeedback.html")

#View notification function
@app.route('/Viewnotif', methods=['get'])
def Viewnotif():
    qry = "SELECT * FROM `notification`"
    res=selectall(qry)
    return render_template('Patient/ViewNotification.html',val=res)


@app.route("/adfeedback")
def adfeedbak():
    return render_template("Patient/ADD FEEDBACK.html")


#Doctor Home
@app.route("/Doctor")
def Docotor_home():
    return render_template("Doctor/Doctor home.html")

@app.route("/View Booking")
def Booking2():
    return render_template("Doctor/ViewBooking.html")

@app.route("/Create Prescription")
def Create():
    return render_template("Doctor/CreatePrescription.html")

@app.route("/Update prescription")
def Update():
    return render_template("Doctor/UpdatePrescription.html")


@app.route("/View notifi")
def Notifi():
    return render_template("Doctor/ViewNotification.html")



#Nurse
@app.route("/Nurse")
def Nurse_home():
    return render_template("Nurse/Nurse Homepage.html")

@app.route("/Manage vaccine booking")
def Nurse_view():
    q="SELECT `booking_for_vaccination`.*,`patient details`.`Name` AS pname,`vaccine_table`.`Name`,`vaccine_schedule`.`Date`,`time_slot`.* FROM `time_slot` JOIN `vaccine_schedule` ON `vaccine_schedule`.`Tid`=`time_slot`.`Tid` JOIN `vaccine_table` ON `vaccine_table`.`vd_id`=`vaccine_schedule`.`Vac_id` JOIN `booking_for_vaccination` ON `booking_for_vaccination`.`Vsch_id`=`vaccine_schedule`.`Vsch_id` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_vaccination`.`Pat_id`"
    res=selectall(q)

    return render_template("Nurse/Manage Booking.html",val=res)

@app.route("/View notif")
def Nurse_noti():
    return render_template("Nurse/ViewNotification.html")


@app.route("/vaccinated")
def vaccinated():  
    id=request.args.get('id')
    qry="UPDATE `booking_for_vaccination` SET `Status`='vaccinated' WHERE `Vcb_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("vaccinated succesfully");window.location="Nurse"</script>'''

#Pharmacist
@app.route("/Pharmacist")
def Pharmacist_home():
    return render_template("Pharmacist/Pharmacist Homepage.html")

@app.route("/Medicine details")
def Pharmacist_medicine():
    return render_template("Pharmacist/Viewmedicinedetails.html")

@app.route("/Manage Prescription")
def Pharmacist_prescription():
    return render_template("Pharmacist/viewPrescription and addMedicine.html")

@app.route("/View n")
def Pharmacist_notification():
    return render_template("Pharmacist/ViewNotification.html")

































app.run(debug=True)