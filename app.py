#To Execute the code read "ReadME.Txt" file 
#Prerequisites :: text editor, python3 , flask module 

from flask import Flask, redirect, sessions, url_for, request,render_template,make_response
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mysqldb import MySQL

with open('templates/config.json' , 'r') as c:
    params = json.load(c)['params']

    
app = Flask(__name__, template_folder='templates')      

'''
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///info.db"   #database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Donername = db.Column(db.String(200), nullable=False)
    bloodT = db.Column(db.String(500), nullable=False)
    contactME = db.Column(db.String(500), nullable=False)
 
    def __repr__(self) -> str:
        return f"{self.sno} - {self.Donername}"
'''

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'info'
 
mysql = MySQL(app)



#Main page
@app.route('/' ,methods=['GET', 'POST'],)
def hello_world():
    if request.method == 'POST':
        if request.form.get('action1') == 'Doner':
            return render_template('doner.html')
        elif  request.form.get('action2') == 'Patient':
            pass 
            return render_template('patient.html')
        else:
            pass 
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html")


# DONER
@app.route('/successDoner/<Donername>/<bloodT>/<contactME>')
def success( Donername, bloodT, contactME):

    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO table_info(Donername,bloodT,contactME) VALUES(%s,%s,%s)''',(Donername,bloodT,contactME))
    cursor.execute(''' SELECT * FROM table_info ''')
    user = cursor.fetchall()
    mysql.connection.commit()

    return render_template('infotable.html',allinfo=user,Donername = Donername,contactME=contactME)


@app.route('/doner', methods = ['POST' , 'GET'])
def Donation():
    if request.method == 'POST':
        user = request.form['nm']
        user2 = request.form['blood']
        user3 = request.form['contact']
        return redirect(url_for('success', Donername = user , bloodT = user2 ,contactME = user3))
    else:
        return render_template('doner.html')


#Patient 
@app.route('/successpatient/<Patientname>')
def successD(Patientname):
   return 'welcome %s' % Patientname

@app.route('/patient', methods = ['POST' , 'GET'])
def patient():
    if request.method == 'POST':
        user = request.form['nm']
        user2 = request.form['contact']
        return redirect(url_for('show', NAME = user , CONTACT = user2))
    else:
        return render_template('patient.html')


#This route is just to check the information site 
@app.route('/show/<NAME>/<CONTACT>')
def show(NAME,CONTACT):
    
 
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM table_info ''')
    user = cursor.fetchall()

    return render_template('infotable2.html', allinfo =user,NAME = NAME , CONTACT = CONTACT )

#Contact us form
@app.route('/information')
def information():
    return render_template('information.html')
   
#information for doner
@app.route('/donerINFO')
def donerINFO():
    return render_template('donerINFO.html')

#Information about the blood banks
@app.route('/bloodBank')
def bloodBank():
    return render_template('bloodBank.html')

#Redirected form to send request to doner
@app.route('/sendRequest/<int:sno>/<NAME>/<CONTACT>/<dCONTACT>')
def sendRequest(sno,NAME,CONTACT,dCONTACT):


    #info = Info.query.filter_by(sno=sno).first()
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM table_info ''')
    user = cursor.fetchall()


    return render_template('sendRequest.html', info = user , NAME = NAME , CONTACT = CONTACT, dCONTACT= dCONTACT)


#Redirected form to send request to admin
@app.route('/requestDelete/<int:sno>/<NAME>/<CONTACT>')
def requestDelete(sno,NAME,CONTACT):
    #info = Info.query.filter_by(sno=sno).first()

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT Donername,bloodT,contactME FROM table_info ''')
    user = cursor.fetchall()
    return render_template('requestdelete.html', info = user , NAME = NAME , CONTACT = CONTACT,params=params)


#List of Doners available 

@app.route('/list3')
def pp3():
 
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT Donername,bloodT,contactME FROM table_info ''')
    user = cursor.fetchall()

    return render_template('infotable3.html', allinfo =user,)



#To remove the Query
@app.route('/remove')
def remove():
    #info = Info(  Donername = "Name", bloodT = "Blood type" ,contactME = "123456789")   
    #allinfo = Info.query.all()

        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM table_info ''')
        user = cursor.fetchall()

        return render_template('admin.html', allinfo =user,)


@app.route('/delete/<sno>')
def delete(sno):
    #info = Info.query.filter_by(sno=sno).first()
    #db.session.delete(info)
    #db.session.commit()


    cursor = mysql.connection.cursor()
    # Dsno = " DELETE FROM table_info WHERE sno = ?"
    # cursor.execute(Dsno % (sno,))

    cursor.execute(" DELETE FROM table_info WHERE sno = %s" % (sno,))
    mysql.connection.commit()                          ## replacement for conn.commit()


   
    return redirect('/remove')


#Admin / dashbord
@app.route('/admin', methods = ['GET','POST'])
def Admin():
    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):


                #info = Info(  Donername = "Name", bloodT = "Blood type" ,contactME = "123456789")   
                #allinfo = Info.query.all()

                    cursor = mysql.connection.cursor()
                    cursor.execute(''' SELECT * FROM table_info ''')
                    user = cursor.fetchall()

                    return render_template('admin.html', allinfo =user,)
        else:
             return render_template('login.html', params=params)
    else:
        return render_template('login.html', params=params)

#login
@app.route('/login')
def login():
    return render_template('login.html', params=params)
    

if __name__ == '__main__':
   app.run(debug = True)