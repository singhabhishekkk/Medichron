from datetime import datetime
from flask import Flask, flash, render_template, url_for, flash, redirect, request,render_template_string
import csv
import pandas as pd
import cv2
import pyzbar.pyzbar as pyzbar
import qrcode
from io import BytesIO
import os
# using those forms created here in our application
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

df = pd.read_csv('nameListDoc.csv')


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/contact')
def cont():
    return render_template("contact.html")


@app.route('/register', methods=['GET', 'POST'])
def reg():
    results = pd.read_csv('nameListUser.csv')
    x = len(results)
    sno = str(x+1)
    errors = {}
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["psw"]
        email = request.form['email']
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        location = request.form["location"]
        dateofbirth = request.form["dateofbirth"]
        aadhaar = request.form['aadhaar']
        phone = request.form['phone']
        uid = str(sno+firstname[0]+lastname[0]+phone[-4:]+aadhaar[-4:])
         
            
        fieldnamesU = ['sno','username', 'email', 'firstname', 'lastname',
                       'location', 'dateofbirth', 'password', 'aadhaar', 'phone','uid']
        
    
        with open('nameListUser.csv', 'a', newline='') as inFile:

            # DictWriter will help you write the file easily by treating the
            # csv as a python's class and will allow you to work with
            # dictionaries instead of having to add the csv manually.
            writer = csv.DictWriter(inFile, fieldnames=fieldnamesU)
            # writerow() will write a row in your csv file
            # while()

            writer.writerow({"sno":sno,'username': username, 'email': email, 'firstname': firstname, 'lastname': lastname,
                            'location': location, 'dateofbirth': dateofbirth, 'password': password,  'aadhaar': aadhaar,  'phone': phone,"uid":uid})

    return render_template('register.html', title='Register', errors=errors, data=df)


@app.route('/doctor', methods=['GET', 'POST'])
def doc():
    results = pd.read_csv('nameListUser.csv')
    x = len(results)
    sno = x
    errors = {}
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["psw"]
        email = request.form['email']
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        location = request.form["location"]
        dateofbirth = request.form["dateofbirth"]
        aadhaar = request.form['aadhaar']
        phone = request.form['phone']

        fieldnamesU = ['sno','username', 'email', 'firstname', 'lastname',
                       'location', 'dateofbirth', 'password', 'aadhaar', 'phone']

        with open('nameListDoc.csv', 'a', newline='') as inFile:
            # DictWriter will help you write the file easily by treating the
            # csv as a python's class and will allow you to work with
            # dictionaries instead of having to add the csv manually.
            writer = csv.DictWriter(inFile, fieldnames=fieldnamesU)
            # writerow() will write a row in your csv file
            # while()
            writer.writerow({'sno':sno,'username': username, 'email': email, 'firstname': firstname, 'lastname': lastname,
                            'location': location, 'dateofbirth': dateofbirth, 'password': password,  'aadhaar': aadhaar,  'phone': phone})

    return render_template('doctor.html', title='Register', errors=errors, data=df)


@app.route('/login', methods=['GET', 'POST'])
def log():
    errors = {}
    if request.method == "POST":
        print("username=", request.form["username"])
        print("password=", request.form["password"])

    if 'check' in request.form:
        check = request.form['check']

        error = ""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with open('nameListDoc.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == username and row[7] == password:
                        return redirect('/dashboardDoc/{}'.format(username))
                    else:
                        error = 'Invalid Credentials. Please try again.'
                        flash(error, "error")
        return render_template('login.html', error=error)

# Checking for UserCondition
    else:
        error = ""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with open('nameListUser.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == username and row[7] == password:
                        return redirect('/dashboardUser/{}'.format(username))
                    else:
                        error = 'Invalid Credentials. Please try again.'
                        flash(error, "error")
        return render_template('login.html', error=error)


@app.route('/dashboardUser/<username>', methods=['GET', 'POST'])
def dashboard(username):

    if request.method == 'POST':
        if 'click' in request.form:
             return redirect('/qrgenerate/{}'.format(username))
        
        if 'hist' in request.form:
             return redirect('/userhistory/{}'.format(username))
        

        

    with open('nameListUser.csv', 'r', newline='') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[1] == username:
                firstname = row[3]
                lastname = row[4]
                location = row[5]
                dateofbirth = row[6]
                email = row[2]
                phone = row[9]
                aadhaar = row[8]

               
        

    return render_template("dashboardUser.html",username=username, firstname=firstname, lastname=lastname, location=location, dateofbirth=dateofbirth, email=email, phone=phone, aadhaar=aadhaar)


@app.route('/dashboardDoc/<username>', methods=['GET', 'POST'])
def dashboarddoc(username):
    with open('nameListDoc.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == username:
                firstname = row[3]
                lastname = row[4]
                location = row[5]
                dateofbirth = row[6]
                email = row[2]
                phone = row[9]
                aadhaar = row[8]

                
            

    return render_template("dashboardDoc.html", username=username, firstname=firstname, lastname=lastname, location=location, dateofbirth=dateofbirth, email=email, phone=phone, aadhaar=aadhaar)


@app.route('/doctorhistory/<username>', methods=['GET', 'POST'])

def history(username):

    if request.method == 'POST':
        if 'back' in request.form:
             return redirect('/userhistory/{}'.format(username))
        
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime("%H:%M:%S")

    errors = {}
    if request.method == "POST":
        symptoms = request.form["symptoms"]
        diagnosis = request.form['diagnosis']
        treatment = request.form["treatment"]
        
         
            
        fieldnamesx = ['username','date','time', 'symptoms', 'diagnosis', 'treatment']
        
    
        with open('userhistory.csv', 'a', newline='') as inFile:
            # DictWriter will help you write the file easily by treating the
            # csv as a python's class and will allow you to work with
            # dictionaries instead of having to add the csv manually.
            writer = csv.DictWriter(inFile, fieldnames=fieldnamesx)
            # writerow() will write a row in your csv file
            # while()
            writer.writerow({"username":username,'date': date,'time':time, 'symptoms': symptoms, 'diagnosis': diagnosis, 'treatment': treatment})
            

    

    return render_template('historyDoctor.html',username=username,errors = errors)


@app.route('/userhistory/<username>', methods=['GET', 'POST'])
def userhistory(username):

    if request.method == 'POST':
        if 'pogo' in request.form:
             return redirect('/doctorhistory/{}'.format(username))
        
        
    with open('userhistory.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data=[]

        for row in reader:
            if row[0] == username:
                # date = row[1]
                # symptoms = row[2]
                # diagnosis = row[3]
                # treatment= row[4]
                data.append(row)
                
    return render_template("historyUser.html",data = data)#,date=date , symptoms = symptoms , diagnosis = diagnosis , treatment=treatment)


@app.route('/scan')
def scan():
    global camera
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            decoded_objects = pyzbar.decode(frame)  # decode QR codes in the frame
            if decoded_objects:
                # Do something with the QR code data here
                print(decoded_objects[0].data)
                camera.release() # release the camera when a QR code is detected
                data =decoded_objects[0].data.decode('utf-8')
                
            
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to quit
            break

    camera.release() # release the camera when done
    cv2.destroyAllWindows() # destroy all windows

    with open('nameListUser.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if data == row[10]:
                username = row[1]
                return redirect ('/userhistory/{}'.format(username))
                
            
@app.route('/qrgenerate/<username>', methods=['GET', 'POST'])
def gen(username):
    uid = ""
    with open('nameListUser.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == username:
               uid = row[10]

    save_directory = "static/qr_code"
    if not os.path.exists(save_directory):
       os.makedirs(save_directory)



    file_path = os.path.join(save_directory, "{}.png".format(uid))
    if not os.path.isfile(file_path):
        qr_code = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_code.add_data(uid)
        qr_code.make(fit=True)
        img = qr_code.make_image(fill_color="black", back_color="white")
        img.save(file_path)
    full_path = "qr_code/"+uid+".png"
        
       


    return render_template("qrgenerate.html",username = username ,uid = uid,full_path = full_path)
                                  
    
@app.route('/contact', methods=['GET', 'POST'])
def x():
    errors={}
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form['email']
        phone = request.form["phone"]
        messege= request.form["messege"]
       

        fieldnamesy = ['firstname','lastname', 'email', 'phone', 'messege']

        with open('contact.csv', 'a', newline='') as inFile:
            # DictWriter will help you write the file easily by treating the
            # csv as a python's class and will allow you to work with
            # dictionaries instead of having to add the csv manually.
            writer = csv.DictWriter(inFile, fieldnames=fieldnamesy)
            # writerow() will write a row in your csv file
            # while()
            writer.writerow({'firstname':firstname,'lastname':lastname, 'email':email, 'phone':phone, 'messege':messege})

    return render_template('contact.html',errors=errors)


    

if __name__ == '__main__':

    app.run(debug=True)
