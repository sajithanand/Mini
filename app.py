
#from crypt import methods
from email.headerregistry import Address
from select import select
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
    return render_template("login.html")

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
        session['lid']=res['login_id']
        return '''<script>alert("valid");window.location="admin"</script>'''
    elif res['usertype'] == "patient":
        session['lid']=res['login_id'] #getting patient id from login function
                    
        return '''<script>alert("valid");window.location="Patienthome"</script>'''
    elif res['usertype'] == "Doctor":
        session['lid']=res['login_id']
        return '''<script>alert("valid");window.location="Doctor"</script>'''
    elif res['usertype'] == "Nurse":
        session['lid']=res['login_id']
        return '''<script>alert("valid");window.location="Nurse"</script>'''
    elif res['usertype'] == "Pharmacist":
        session['lid']=res['login_id']
        return '''<script>alert("valid");window.location="Pharmacist"</script>'''
    else:
        return '''<scrpit>alert("invalid");window.location="login"</script>'''

#Registration Function
@app.route('/registration', methods=['post'])
def registration():
    name=request.form['fname']
    address=request.form['home']
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
   
    qry1="INSERT INTO `patient details` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1=(str(id),name,Gender,Bloodgroup,Email,DOB,Phone,age,address)
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
    val=(Time,Date,doctor,strength)
    iud(qry1,val)

    return '''<script>alert("Registerd successfully");window.location="manage_schedule"</script>'''    
    
    


#Manage doctor schedule
@app.route("/manage_schedule")
def man_schedule():
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    re=selectall(qr)
    return render_template("manage_schedul1.html",val1=re)

@app.route("/search_schedule",methods=['post'])
def search_schedule():
    did=request.form['select']
    qr="SELECT * FROM `addstaffdata` WHERE `Designation`=1"
    re=selectall(qr)
    qr="SELECT `time_slot`.*,`doctor_schedule`.* FROM `doctor_schedule` JOIN `time_slot` ON `time_slot`.`Tid`=`doctor_schedule`.`tid` WHERE `doctor_schedule`.`Emp_id`=%s"
    res=selectall2(qr,did)
    dsid = []
    for i in res:
        dsid.append(str(i['sch_id']))
    a=",".join(dsid)   
    print(a,"44444444444444444444")
    return render_template("manage_schedul1.html",val1=re,val=res,dscid=str(a))

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



@app.route("/refresh_schedule")
def refresh_schedule():
    sid=request.args.get('id')
    a = sid.split(',')
    print(a,type(a),"88888888888888888888")
    for i in range(0, len(a)):
        qry= "update `doctor_schedule` set strength=20 WHERE sch_id=%s"
        iud(qry,str(a[i]))
        # print(a[i])
        return '''<script>alert("Slot refreshed successfully");window.location="manage_schedule"</script>'''
        
     
#Add Staff Data
@app.route("/AddstaffData",methods=['post'])
def AddstaffData():
    name=request.form['name']
    home=request.form['Home']
    place=request.form['place']
    city=request.form['City']
    pincode=request.form['pin']
    Age=request.form['age']
    Gender=request.form['RadioGroup1']
    Experience=request.form['experience']
    Specialization=request.form['Specialization']
    Designation=request.form['Designation']
    Licensenumber=request.form['Licensenumber']
    Registration=request.form['Registration_number']
    username=request.form['Username']
    password=request.form['Password']
    # image=request.files['file']
    # filname=secure_filename(image.filename)
    # image.save(os.path.join('static/doctorimages',filname))



    if Designation=="1":
    
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Doctor')"
        val=(username,password)
        id=iud(qry,val)
        image=request.files['file']
        filname=secure_filename(image.filename)
        image.save(os.path.join('static/doctorimages',filname))


        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,%s,%s,'available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,filname,Registration)
        iud(qry1,val1)
        return '''<script>alert("Registered successfully");window.location="/"</script>'''
    elif Designation=="2":
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Pharmacist')"
        val=(username,password)
        id=iud(qry,val)

        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL,'available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,Licensenumber)
        iud(qry1,val1)
        return '''<script>alert("Registered successfully");window.location="/"</script>'''
    else:
        qry="INSERT INTO `login` VALUES(NULL,%s,%s,'Nurse')"
        val=(username,password)
        id=iud(qry,val)
        qry1="INSERT INTO `addstaffdata` VALUES(%s,NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL,%s,'available')"
        val1=(str(id),name,home,place,city,pincode,Age,Gender,Experience,Specialization,Designation,Registration)
        iud(qry1,val1)
        return '''<script>alert("Registered successfully");window.location="/login"</script>'''

@app.route("/Addstaff1")
def Addstaff():
    return render_template("staff.html")
   
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
    qry = "SELECT `patient details`.`Name`,`addstaffdata`.`Name` AS drname,`doctor_schedule`.`Date`,`time_slot`.`Start time`,`End time`,`booking_for_doctor`.`Status`,`booking_for_doctor`.`date` FROM `patient details` JOIN `booking_for_doctor` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` JOIN `doctor_schedule` ON `booking_for_doctor`.`sch_id`=`doctor_schedule`.`sch_id` JOIN `time_slot` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` JOIN `addstaffdata` ON `doctor_schedule`.`Emp_id`=`addstaffdata`.`login id` WHERE `addstaffdata`.`Designation`=1"
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
    name=request.form['vaccine']
    description=request.form['description']

    qry1="INSERT INTO `vaccine_table` VALUES(NULL,%s,%s,'available')"
    val1=(name,description)
    iud(qry1,val1)
    return '''<script>alert("vaccine details added successfully");window.location="/admin"</script>'''

@app.route("/Viewvaccine")
def Vaccine():
    return render_template("vaccine.html")

    

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
    return render_template("Notification.html")

@app.route('/snt_not', methods=['post'])
def snt_not():
    notification=request.form['Notification']
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
    return render_template("Patient/update.html",val=res)

   

    

@app.route("/updpro",methods=['post','get'])
def updpro():
    name = request.form['fname']
    address = request.form['home']
    Gender = request.form['gender']
    Bloodgroup= request.form['Blood_group']
    Email= request.form['email']
    Date_of_birth= request.form['dob']
    Phone= request.form['phone']
    Age = request.form['age']


    
    qry1 = "UPDATE `patient details` SET `Name`=%s,`Gender`=%s,`Blood_Group`=%s,`Email`=%s,`Phone_number`=%s,`Date_of_birth`=%s,`Age`=%s,`Address`=%s WHERE `Login id`=%s"
    val1 = (name,Gender,Bloodgroup,Email,Date_of_birth,Phone,Age,address,session['lid'])
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
    qr="SELECT `time_slot`.*,`doctor_schedule`.*  FROM `time_slot` JOIN `doctor_schedule` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` WHERE `doctor_schedule`.`Emp_id`=%s"
    val=(session['dlid'])

    res=selectall2(qr,val)
    print(res)
    return render_template("Patient/Doctor Booking1.html",d=d,val=res)

@app.route("/search_schd",methods=['post'])
def search_schd():
    # date=request.form['textfield']
    # d=datetime.now().strftime("%Y-%m-%d")
    qr="SELECT `time_slot`.*,`doctor_schedule`.*  FROM `time_slot` JOIN `doctor_schedule` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` WHERE `doctor_schedule`.`Emp_id`=%s AND `doctor_schedule`.`Date`=CURDATE()"
    val=(session['dlid'])

    res=selectall2(qr,val)
    print(res)
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
        q="INSERT INTO `booking_for_doctor` VALUES(NULL,%s,%s,'book',curdate())"   
        v=(session['lid'],str(id))
        iud(q,v)
        qr="UPDATE `doctor_schedule` SET `strength`=`strength`-1 WHERE `sch_id`=%s" 
        iud(qr,str(id))
        return '''<script>alert("booking success");window.location="DoctorBooking"</script>'''

#View booking function   
@app.route("/View_book1")
def View_book1():
    qry = "SELECT `booking_for_doctor`.*,`addstaffdata`.`Name`,`doctor_schedule`.`Date`,`time_slot`.* FROM `booking_for_doctor` JOIN `doctor_schedule` ON `doctor_schedule`.`sch_id`=`booking_for_doctor`.`sch_id` JOIN `addstaffdata` ON `addstaffdata`.`login id`=`doctor_schedule`.`Emp_id` JOIN `time_slot` ON `time_slot`.`Tid`=`doctor_schedule`.`tid` WHERE `booking_for_doctor`.`Pat_id`=%s and booking_for_doctor.Status='book' "
    res = selectall2(qry,session['lid'])
    return render_template("Patient/View_booking.html",val=res)

#cancel booking function
@app.route("/cancel_booking")
def cancel_booking():
    id = request.args.get('id')
    qry = "UPDATE `booking_for_doctor` SET `Status`='canceled' WHERE `Bid`=%s"
    iud(qry,id)
    return '''<script>alert("Booking cancelled");window.location="Patienthome"</script>'''



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



#VIEW PRESCRIPTION
@app.route("/View_prescription")
def view():
    q="SELECT `prescription_table`.`Prescription`,`prescription_table`.`Status`,`addstaffdata`.`Name` FROM `prescription_table` JOIN `booking_for_doctor` ON `booking_for_doctor`.`Bid`=`prescription_table`.`Bid`  JOIN `doctor_schedule` ON `doctor_schedule`.`sch_id`=`booking_for_doctor`.`sch_id` JOIN `addstaffdata` ON `addstaffdata`.`login id`=`doctor_schedule`.`Emp_id` WHERE `booking_for_doctor`.`Pat_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template("Patient/ViewPrescription.html",val=res)






#Add Feeedback Function
@app.route("/Add_feedbac",methods=['post'])
def Add_feed():
    feedback=request.form['Feedback']

    qry1="INSERT INTO `feedback_table` VALUES(NULL,%s,CURDATE(),%s)"
    val=(session['lid'],feedback)
    iud(qry1,val)
    return '''<script>alert("feedback added succesfully");window.location="Patienthome"</script>'''

@app.route("/Add_feedback")
def Add_feedback():
    return render_template("Patient/addFeed.html")

#View notification function
@app.route('/Viewnotif', methods=['get'])
def Viewnotif():
    qry = "SELECT * FROM `notification`"
    res=selectall(qry)
    print(len(res),"*********************")
    import datetime
    # x=datetime.strptime('5/5/2019','%d/%m/%Y')
    # x = datetime.datetime(res[0]["Date"],'%Y/%m/%d')

    # print(x.strftime("%d %b %Y"))
    x = datetime.datetime.strptime(str(res[0]["Date"]), '%Y-%m-%d').strftime('%d/%B/%Y')
    print(x)
    for i in range(len(res)):
        res[i]["Date"] = datetime.datetime.strptime(str(res[i]["Date"]), '%Y-%m-%d').strftime('%d-%b-%Y')

    # print(res[0]["Date"])
    return render_template('Patient/ViewNotification.html',val=res)





#Doctor Home
@app.route("/Doctor")
def Docotor_home():
    return render_template("Doctor_home.html")

#View Doctor booking
@app.route("/View_booked")
def BOOKED():
    # qry = "SELECT `patient details`.`Name`,`addstaffdata`.`Name` AS drname,`doctor_schedule`.`Date`,`time_slot`.`Start time`,`End time`,`booking_for_doctor`.`Status` FROM `patient details` JOIN `booking_for_doctor` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` JOIN `doctor_schedule` ON `booking_for_doctor`.`sch_id`=`doctor_schedule`.`sch_id` JOIN `time_slot` ON `doctor_schedule`.`tid`=`time_slot`.`Tid` JOIN `addstaffdata` ON `doctor_schedule`.`Emp_id`=`addstaffdata`.`login id` WHERE `addstaffdata`.`Designation`=1 and `doctor_schedule`.`Emp_id`=%s" 
    qry="SELECT `patient details`.`Name`,`Login id`,`doctor_schedule`.`Date`,`time_slot`.*,`booking_for_doctor`.* ,`booking_for_doctor`.date as d FROM `doctor_schedule` JOIN `time_slot` ON `time_slot`.`Tid`=`doctor_schedule`.`tid` JOIN `booking_for_doctor` ON `booking_for_doctor`.`sch_id`=`doctor_schedule`.`sch_id` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` WHERE `doctor_schedule`.`Emp_id`=%s AND `booking_for_doctor`.`Status`='book'"
    res = selectall2(qry,session['lid'])
    return render_template("Doctor/ViewBooking.html",val=res)

#Create prescription function
@app.route("/CreatePrescription")
def Create():
    id=request.args.get('id')
    session['bbid']=id
    q="SELECT * FROM `prescription_table` WHERE `Bid`=%s"
    res=selectall2(q,str(id))
    return render_template("Doctor/CreatePrescription.html",val=res)

#Upload prescription
@app.route("/Upload_Prescription")
def upload():
   return render_template("Doctor/upload.html")

#Upload prescription
@app.route("/upload_prescr",methods=['post'])
def upload_prescr():
    pres=request.files['file']
    pp=secure_filename(pres.filename)
    pres.save(os.path.join('static/prescription',pp))

    qry="INSERT INTO `prescription_table` VALUES(NULL,%s,%s,curdate(),'pending')"
    val=(session['bbid'],pp)
    iud(qry,val)
   
    return '''<script>alert("prescription added successfully");window.location="CreatePrescription"</script>'''
    







# @app.route("/make_presc",methods=['POST'])
# def make_presc():
#     mid=request.form['select']
#     remark=request.form['textfield']
#     q="INSERT INTO `prescription_table` VALUES(NULL,%s,%s,%s,'pending')"
#     v=(session['bid'],mid,remark)
#     iud(q,v)
#     return '''<script>alert("Prescription added successfully");window.location="View_booked"</script>'''




#Create report function
@app.route("/Create_report")
def Create_report():
    
    return render_template("Doctor/Create_report.html")

@app.route("/addCreate_report",methods=['post'])
def addCreate_report():
    report=request.form['textarea']
    q="INSERT INTO `report` VALUES(NULL,%s,%s,CURDATE())"
    v=(session['brid'],report)
    iud(q,v)
    return '''<script>alert("report added succesfully");window.location="View_booked"</script>'''


#View previous report function
@app.route("/View_report")
def View_report():
    id=request.args.get('id')
    bid=request.args.get('id')
    session['brid']=id
    pid=request.args.get('pid')
    q="SELECT  * FROM `report` WHERE `Bid` IN(SELECT `Bid` FROM `booking_for_doctor` WHERE `Pat_id`=%s)"
    res=selectall2(q,pid)
    return render_template("Doctor/viewReport.html",val=res)




#View notification function by doctor
@app.route('/Viewnoti', methods=['get'])
def noti():
    qry = "SELECT * FROM `notification`"
    res=selectall(qry)
    print(len(res),"*********************")
    import datetime
    # x=datetime.strptime('5/5/2019','%d/%m/%Y')
    # x = datetime.datetime(res[0]["Date"],'%Y/%m/%d')

    # print(x.strftime("%d %b %Y"))
    x = datetime.datetime.strptime(str(res[0]["Date"]), '%Y-%m-%d').strftime('%d/%B/%Y')
    print(x)
    for i in range(len(res)):
        res[i]["Date"] = datetime.datetime.strptime(str(res[i]["Date"]), '%Y-%m-%d').strftime('%d-%b-%Y')

    # print(res[0]["Date"])
    return render_template('Pharmacist/ViewNotification.html',val=res)



#Nurse
@app.route("/Nurse")
def Nurse_home():
    return render_template("Nurse_1.html")

@app.route("/Manage vaccine booking")
def Nurse_view():
    q="SELECT `booking_for_vaccination`.*,`patient details`.`Name` AS pname,`vaccine_table`.`Name`,`vaccine_schedule`.`Date`,`time_slot`.* FROM `time_slot` JOIN `vaccine_schedule` ON `vaccine_schedule`.`Tid`=`time_slot`.`Tid` JOIN `vaccine_table` ON `vaccine_table`.`vd_id`=`vaccine_schedule`.`Vac_id` JOIN `booking_for_vaccination` ON `booking_for_vaccination`.`Vsch_id`=`vaccine_schedule`.`Vsch_id` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_vaccination`.`Pat_id`"
    res=selectall(q)

    return render_template("Nurse/Manage Booking.html",val=res)

#View notification function
@app.route("/notify")
def notify():
    qry = "SELECT * FROM `notification`"
    res=selectall(qry)
    print(len(res),"*********************")
    import datetime
    # x=datetime.strptime('5/5/2019','%d/%m/%Y')
    # x = datetime.datetime(res[0]["Date"],'%Y/%m/%d')

    # print(x.strftime("%d %b %Y"))
    x = datetime.datetime.strptime(str(res[0]["Date"]), '%Y-%m-%d').strftime('%d/%B/%Y')
    print(x)
    for i in range(len(res)):
        res[i]["Date"] = datetime.datetime.strptime(str(res[i]["Date"]), '%Y-%m-%d').strftime('%d-%b-%Y')

    # print(res[0]["Date"])
    return render_template('Pharmacist/ViewNotification.html',val=res)


#View vaccine booking function
@app.route("/vaccinated")
def vaccinated():  
    id=request.args.get('id')
    qry="UPDATE `booking_for_vaccination` SET `Status`='vaccinated' WHERE `Vcb_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("vaccinated successfully");window.location="Nurse"</script>'''

#Pharmacist
@app.route("/Pharmacist")
def Pharmacist_home():
    return render_template("Pharmacist_home.html")


#Add medicine details
@app.route("/addmedicine",methods=['post'])
def addmedicine():
    Medicine_name=request.form['Medicine_Name']
    Quantity=request.form['Quantity']
    Batch=request.form['Batch_Number']
    Manu=request.form['Manufacture']
    Expiriy=request.form['Expiry']
    Type=request.form['Type']
    Description=request.form['Description']
    Dosage=request.form['Dosage']

    q3="INSERT INTO `medicine_table` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    v3=(Medicine_name,Quantity,Batch,Manu,Expiriy,Type,Description,Dosage)
    res=iud(q3,v3)
    return '''<script>alert("Medicine added successfully");window.location="Pharmacist"</script>'''

@app.route("/Medicine details")
def Pharmacist_medicine():
    return render_template("Pharmacist/add-medicine.html")

#Manage medicine details
@app.route("/View_details")
def View_details():
    q="SELECT * FROM `medicine_table` ORDER BY `Medicine_name` "
    res=selectall(q)
    q1="SELECT * FROM `medicine_table`"
    res1=selectall(q1)
    print(res,"qqqqqqqqqqqqqqqqqqqqqqqqqq")
    return render_template("Pharmacist/MANAGE_MEDICINE.html",data=res,val=res1)


@app.route("/View_details1",methods=['post'])
def View_details1():
    mid=request.form['mid']  
    print(mid,'aaaaaaaaaaaaaaaaaaaaaaaa')
    q="SELECT * FROM `medicine_table`"
    res=selectall(q)
    q1="SELECT * FROM `mesdicine_table` WHERE `Med_id`=%s"
    res1=selectall2(q1,mid)
    return render_template("Pharmacist/MANAGE_MEDICINE.html",data=res1,val=res)

#Edit Details
@app.route("/edit_details")
def editMedicine_details():
    id=request.args.get('id')
    session['mid']=id
    qry="SELECT * FROM `medicine_table` WHERE `Med_id`=%s"
    res=selectone(qry,str(id))
    return render_template("Pharmacist/update.html",val=res)

#Update Details
@app.route("/update_details",methods=['post'])
def update_details():
    medicine=request.form['textfield2']
    quantity=request.form['textfield4']
    batch_number=request.form['textfield']
    manufacture_date=request.form['textfield3']
    expiry_date=request.form['textfield5']

    qry1="UPDATE `medicine_table` set `Medicine_name`=%s,`Quantity`=%s,`Batch_number`=%s,`Manufacture_date`=%s,`Expiry_date`=%s WHERE `Med_id`=%s"
    val=(medicine,quantity,batch_number,manufacture_date,expiry_date,session['mid'])
    iud(qry1,val)

    return '''<script>alert("updated successfully");window.location="edit_details"</script>'''


    



#Delete Details
@app.route("/delete_details")
def delete_details():
    id=request.args.get('id')
    qry="delete FROM `medicine_table` WHERE `Med_id`=%s"
    iud(qry,str(id))


    return '''<script>alert("Deleted successfully");window.location="Pharmacist"</script>'''



#View patient details function
@app.route("/View_Patient_Details")
def View_Patient_Details():
    qry = "SELECT * FROM `patient details` JOIN `booking_for_doctor` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id`"
    res = selectall(qry)
    return render_template("Pharmacist/view_presc.html",val=res)


#Search patient  details function
@app.route("/search_patient",methods=['post'])
def search_patient():
    print(request.form)
    name=request.form['mid']
    print(name)
    qry="SELECT  `patient details`.*,`booking_for_doctor`.`Bid`,`doctor_schedule`.`Date` FROM `booking_for_doctor` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` JOIN `doctor_schedule` ON `doctor_schedule`.`sch_id`=`booking_for_doctor`.`sch_id` WHERE `patient details`.`Login id`=%s"
    res=selectall2(qry,name)
    print(res,"aaaaaaaaaaaaaaaaaaaaa")
    return render_template("Pharmacist/view_presc.html",val1=res)





#Manage prescription function
@app.route("/managePrescription")
def managePrescription():
    id=request.args.get('id')
    q="SELECT `prescription_table`.*,`addstaffdata`.`Name` FROM `addstaffdata` JOIN `doctor_schedule` ON `doctor_schedule`.`Emp_id`=`addstaffdata`.`login id` JOIN `booking_for_doctor` ON `booking_for_doctor`.`sch_id`=`doctor_schedule`.`sch_id` JOIN `prescription_table` ON `prescription_table`.`Bid`=`booking_for_doctor`.`Bid` WHERE `booking_for_doctor`.`Bid`=%s"
    res=selectall2(q,str(id))
    return render_template("Pharmacist/manage-presc.html",val=res)




@app.route("/edit_status")
def edit_status():
    id=request.args.get('id')
    session['presid']=id
    return render_template("Pharmacist/status1.html")


@app.route("/update_status", methods=['post'])
def update_status():
    status=request.form['textfield']
    qry="UPDATE `prescription_table` SET STATUS=%s WHERE `Presc_id`=%s"
    iud(qry,(status,session['presid']))

    return ''''<script>alert("updated");window.location="View_Patient_Details"</script>'''



#UPDATE MEDICINE details
@app.route("/medicineDetails",methods=['post','get'])
def medicineDetails():
    q="SELECT*FROM `medicine_table`"
    res=selectall(q)
    return render_template("Pharmacist/update-med.html",val=res)


@app.route("/medicineDetails1",methods=['post'])
def medicineDetails1():
    mdcn=request.form['select']
    qty=request.form['textfield']
    q="UPDATE `medicine_table` SET `Quantity`=`Quantity`-%s WHERE `Med_id`=%s"
    v=(qty,mdcn)
    iud(q,v)
    return '''<script>alert("updated");window.location='/medicineDetails'</script>'''




#View patient details
# @app.route("/View_Patient_Details")
# def View_Patient_Details():
#     q1="SELECT `booking_for_doctor`.*,`patient details`.`Name`,`doctor_schedule`.`Date` FROM `booking_for_doctor` JOIN `patient details` ON `patient details`.`Login id`=`booking_for_doctor`.`Pat_id` JOIN `doctor_schedule` ON `doctor_schedule`.`sch_id`=`booking_for_doctor`.`sch_id`"
    
#     res=selectall(q1)
#     return render_template("Pharmacist/ViewPatientNames.html",val=res)




# @app.route("/Manage Prescription")
# def Pharmacist_prescription():
#     id=request.args.get('id')
#     q="SELECT `prescription_table`.*,`medicine_table`.* FROM `medicine_table`JOIN `prescription_table` ON `prescription_table`.`Med_id`=`medicine_table`.`Med_id` WHERE `prescription_table`.`Bid`=%s"
#     res=selectall2(q,str(id))
#     return render_template("Pharmacist/viewPrescription and addMedicine.html",val=res) 

#View and update status
# @app.route("/medicine_given")
# def medicine_given():  
#     id=request.args.get('id')
#     qry="UPDATE `prescription_table` SET `Status`='medicine given' WHERE `Bid`=%s"
#     iud(qry,str(id))
#     return '''<script>alert("medicine added successfully");window.location="Pharmacist"</script>'''


@app.route("/View_n")
def Pharmacist_notification():
    qry = "SELECT * FROM `notification`"
    res=selectall(qry)
    print(len(res),"*********************")
    import datetime
    # x=datetime.strptime('5/5/2019','%d/%m/%Y')
    # x = datetime.datetime(res[0]["Date"],'%Y/%m/%d')

    # print(x.strftime("%d %b %Y"))
    x = datetime.datetime.strptime(str(res[0]["Date"]), '%Y-%m-%d').strftime('%d/%B/%Y')
    print(x)
    for i in range(len(res)):
        res[i]["Date"] = datetime.datetime.strptime(str(res[i]["Date"]), '%Y-%m-%d').strftime('%d-%b-%Y')

    # print(res[0]["Date"])
    return render_template('Pharmacist/ViewNotification.html',val=res)
    

@app.route("/viewreport")
def viewreport():
    return render_template("ViewBookingReport.html")


@app.route("/viewreport1",methods=['post'])
def viewreport1():  
    fdate=request.form['textfield']
    tdate=request.form['textfield3']
    q="SELECT COUNT(*) AS c,`Name` FROM `vaccine_table` JOIN `vaccine_schedule` ON `vaccine_schedule`.`Vac_id`=`vaccine_table`.`vd_id` JOIN `booking_for_vaccination` ON `booking_for_vaccination`.`Vsch_id`=`vaccine_schedule`.`Vsch_id` WHERE `Date` BETWEEN %s AND %s GROUP BY `vaccine_table`.`vd_id`"
    v=(fdate,tdate)
    res=selectall2(q,v)

    q1="SELECT COUNT(*) AS co FROM `booking_for_doctor` WHERE  `date` BETWEEN %s AND %s "
    re=selectall2(q1,v)
    q2="SELECT * FROM `medicine_table` WHERE `Quantity`<300"
    res1=selectall(q2)
    print(res)
    print(re)
    print(res1)
    result=[]
    for i in res:
        row={"title":"Vaccine "+i['Name'],"des":str(i['c'])+" patients Booked"}
        result.append(row)
    for i in re:
        row={"title":"Doctor Bookings:","des":str(i['co'])+" patients Booked"}
        result.append(row)
    for i in res1:
        row={"title":"Medicine "+i['Medicine_name'],"des":str(i['Quantity'])+" units Remaining"}
        result.append(row)





    return render_template("ViewBookingReport.html",val=result)


































app.run(debug=True)