from user import *
from water import *
from exercise import *
import pandas as pd
import mysql.connector
import hashlib
import datetime
import os
import json
from cerberus import Validator

def loadjson():
    var = os.path.dirname(os.path.abspath('databasepassword.json')) + '\\databasepassword.json'
    with open(var) as f:
     data = json.load(f)
    return data

def validatewater(water):
    waterschema = {'amount' :  {'type':'integer','min':16, 'max':900,'required':True},
          'goal': {'type':'integer','min':16, 'max':900, 'required':True},
          'date': {'type':'date', 'required':True},
          'metrics':{'type':'integer','min':0, 'max':1}}
    v = Validator(waterschema)
    if (v.validate(water)):
        return True
    else:
        print(v.errors)
        return False

def validateexercise(exercise):
    exerciseschema = {'calories': {'type':'integer','min':0, 'max':1000,'required':True},
          'start': {'type':'date'},
          'end': {'type':'date'},
          'date': {'type':'date', 'required':True},
          'name':{'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required':True}}
    v = Validator(exerciseschema)
    if (v.validate(exercise)):
        return True
    else:
        print(v.errors)
        return False

def validateuser(user):
    userschema = {'fname': {'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required':True},
            'lname': {'type':'string', 'maxlength': 45, 'regex':'^[A-z]+$', 'required': True},
            'username':{'type':'string', 'maxlength': 45, 'regex':'^[A-z0-9]+$', 'required': True},
            'password':{'type':'string', 'maxlength': 45, 'minlength':8, 'regex':'\\w+', 'required': True},
            'currentweight':{'type':'integer','min':70, 'max':600, 'required': True},
            'goalweight':{'type':'integer','min':70, 'max':600, 'required': True},
            'age':{'type':'integer','min':18, 'max':100, 'required': True},
            'height' :{'type':'integer', 'required': True},
            'startweight':{'type':'integer','min':70, 'max':600, 'required': True},
            'metrics': {'type':'integer','min':0, 'max':1, 'required': True},
            'gender': {'type':'integer','min':0, 'max':1, 'required': True},
            'watergoal': {'type':'integer','min':0, 'max':900, 'required': True}}
    v = Validator(userschema)
    if (v.validate(user)):
        return True
    else:
        print(v.errors)
        return False

def addwater(water, user):
    admin = loadjson()
    waterdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = waterdb.cursor()
    cursor.execute("INSERT INTO water (username, currentwater, date, metrics, goalwater) VALUES (%s, %s, %s, %s, %s)", (user.username, water.amount, water.date, user.metrics, water.goal))
    id = cursor.lastrowid
    waterdb.commit()
    cursor.close()
    waterdb.close()
    return id

def findwater(date, user):
    admin = loadjson()
    waterdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = waterdb.cursor()
    cursor.execute("SELECT * FROM water WHERE date = %s AND username = %s", (date,user.username))
    row = cursor.fetchone()
    if(row == None ):
        return None
    else:
        id = row[0]
        print ("users water goal {}".format(user.watergoal))
        water = Water(row[1], user.watergoal, row[3],row[5])
        return water, id

def updatewater(water, user, id):
    admin = loadjson()
    waterdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = waterdb.cursor()
    cursor.execute("REPLACE INTO water (idwaterintake, currentwater, goalwater, date, username, metrics) VALUES (%s, %s, %s, %s, %s, %s)", (id, water.amount, water.goal, water.date, user.username, user.metrics))
    waterdb.commit()
    cursor.close()
    waterdb.close()
    return True

def addexercise(exercise, user):
    admin = loadjson()
    exercisedb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = exercisedb.cursor()
    cursor.execute("INSERT INTO exercise (exercisename, username, caloriesburned, starttime, endtime, date) VALUES (%s, %s, %s, %s, %s, %s)", (exercise.name, user.username, exercise.calories, exercise.start, exercise.end,exercise.date))
    id = cursor.lastrowid
    exercisedb.commit()
    cursor.close()
    exercisedb.close()
    return id

def findexercise(name, date, user):
    admin = loadjson()
    exercisedb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = exercisedb.cursor()
    size = cursor.execute("SELECT * FROM exercise WHERE exercisename = %s AND date = %s AND username = %s", (name,date,user.username))
    row = cursor.fetchall()
    if(size == 0):
        print("error exercise does not exist")
        return None
    elif( size == 1):
        id = row[0]
        exercise = Exercise(row["caloriesburned"],row["starttime"], row["endtime"], row["date"],row["exercisename"])
        cursor.close()
        exercisedb.close()
        return exercise, id
    else:
        print("several exercise were found with that name please enter the id of the one you wish to update")
        for x in row:
            print("Id: %d Name: %s Date: %x", row["idexercise"], row["exercisename"], row["date"])
        id = int(input("Enter the specific id"))
        cursor.execute("SELECT * FROM exercise WHERE exercisename = %s AND date = %s AND username = %s AND idexercise = %s", (name,date,username, id))
        if row == None:
            print("WRONG")
            return None
        else:
            exercise = Exercise(row["caloriesburned"],row["starttime"], row["endtime"], row["date"],row["exercisename"])
            cursor.close()
            exercisedb.close()
            return exercise, id

def updateexercise(exercise, user, id):
    admin = loadjson()
    exercisedb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = exercisedb.cursor()
    cursor.execute("REPLACE INTO exercise (idexercise, exercisename, username, caloriesburned, starttime, endtime, date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, exercise.name, user.username, exercise.calories,exercise.starttime,exercise.endtime,exercise.date, exercise.name))
    exercisedb.commit()
    cursor.close()
    exercisedb.close()
    return True

def hashpassword(password):
    hashpassword = hashlib.sha1(password.encode('UTF-8')).hexdigest()
    return hashpassword

def finduser(username, password):
    admin = loadjson()
    userdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = userdb.cursor()
    passw = hashpassword(password)
    cursor.execute("SELECT * FROM  users WHERE username = %s AND password = %s", (username,passw))
    row = cursor.fetchone()
    if(row == None ):
        print("error user does not exist")
        return None, None
    else:
        user1 = User(row[2],row[3],row[1],row[4],row[5],row[6],row[7],row[8],row[9], row[10], row[11], row[12])
        id = row[0]
        cursor.close()
        userdb.close()
        return user1, id

def adduser(user):
    admin = loadjson()
    userdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = userdb.cursor()
    cursor.execute("INSERT INTO users (fname, lname, username, password, startweight, currentweight, goalweight, age, height, metrics, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user.fname, user.lname,user.username,user.password, user.startweight,user.currentweight,user.goalweight, user.age,user.height,user.metrics,user.gender))
    id = cursor.lastrowid
    userdb.commit()
    cursor.close()
    userdb.close()
    return id

def updateuser(user, id):
    admin = loadjson()
    userdb = mysql.connector.connect(user=admin["user"], password = admin["password"], host = admin["host"], database=admin["database"])
    cursor = userdb.cursor()
    cursor.execute("REPLACE INTO users (idusers, fname, lname, username, password, startweight, currentweight, goalweight, age, height, metrics, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, user.fname, user.lname,user.username,user.password, user.startweight,user.currentweight,user.goalweight, user.age,user.height,user.metrics,user.gender))
    userdb.commit()
    cursor.close()
    userdb.close()
    return True

#TODO
def exercisemenu(user):
    choice = int(input("Enter 1 to log a new exercise for today or 0 to update an existing exercise"))
    if(choice==1):
        name = input("Enter exercise name: ")
        calories = int(input("Enter calories burned: "))

        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        date1 = datetime.date(year, month, day)

        time_entry1 = input('Enter the start time in HH:MM 24Hourformat: ')
        shour, sminute= map(int, time_entry1.split(':'))
        starttime = datetime.datetime(year, month, day, shour, sminute)

        time_entry2 = input('Enter the end time in HH:MM 24Hourformat: ')
        ehour, eminute= map(int, time_entry2.split(':'))
        endtime = datetime.datetime(year, month, day, ehour, eminute)

        exercise = Exercise(calories,starttime,endtime,date1,name)
        addexercise(exercise, user)

    elif(choice == 0):
        name = input("Enter exercise name: ")
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        date1 = datetime.date(year, month, day)
        exercise, id = findexercise(name, date1, user)
        while(True):
            print("What would you like to do")
            print("-------------------------")
            choice2 = int(input("1:Update Time\n2:Update date\n3:Update Calories\n4:Change Name\n5:Check Exercise Duration\n6:Exit"))
            if(choice2 == 1):
                num = int(input("Enter 0 for the start time or 1 for the end time "))
                time_entry = input('Enter the end time in HH-MM 24Hourformat: ')
                hour, minute= map(int, time_entry.split('-'))
                time = datetime.datetime(year, month, day, hour, minute)
                exercise.updatetime(num, time)

            elif(choice2 == 2):
                newdate_entry = input('Enter a date in YYYY-MM-DD format: ')
                newyear, newmonth, newday = map(int, newdate_entry.split('-'))
                newdate = datetime.date(newyear, newmonth, newday)
                exercise.updatedate(newdate)

            elif(choice2 == 3):
                newcal = int(input("Enter the updated calorie count: "))
                exercise.updatecalories(newcal)

            elif(choice2 == 4):
                newname = input("Enter the update exercise name: ")
                exercise.changename(newname)

            elif(choice2 == 5):
                #fix this later
                print("6 minutes of exercise recorded")

            elif(choice2 == 6):
                updateexercise(exercise, user, id)
                break

            else:
                print("Incorrect entry please try again")
    else:
        print("Invalid selection")

def watermenu(user):
    choice = int(input("Enter 1 to create a new water entry 0 update an existing water entry: "))
    if(choice == 1):
        amount = int(input("Enter how much water you have consumed: "))
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        date = datetime.date(year, month, day)
        water = Water(amount,user.watergoal, date, user.metrics)
        addwater(water, user)
    elif(choice == 0):
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year, month, day = map(int, date_entry.split('-'))
        date = datetime.date(year, month, day)
        water, id = findwater(date, user)
        while(True):
            print("What would you like to do")
            print("-------------------------")
            choice = int(input("1:Add water\n2:Check Water Goal\n3:Update water amount\n4:Exit"))
            if(choice == 1):
                addamount = int(input("Enter the amount of water to be added to the current date"))
                water.addwater(addamount)
            elif(choice == 2):
                water.checkgoal()
            elif(choice == 3):
                wateramount = int(input("Enter the new amount of water for the current date"))
                water.updatewateramount(wateramount)
            elif(choice == 4):
                updatewater(water, user, id)
                break
            else:
                print("Incorrect entry please try again")
    else:
        print("Invalid selection")

def usermenu(user,id):
    while(True):
        print("What would you like to do")
        print("-------------------------")
        choice = int(input("1:Update Weight\n2:Check Weight Loss\n3:Update Age\n4:Change Height\n5:Change name\n6:Change password\n7:Update Metrics\n8:update Weight Goal\n9:Exit"))
        if(choice == 1):
            delta = int(input("Enter weight change: (-)pounds for loss (+)pounds for gain"))
            user.updateweight(delta)
            print(user)

        elif(choice == 2):
            print(user.checkweight())

        elif(choice == 3):
             age = int(input("Enter age change: "))
             user.updateage(age)
             print(user)

        elif(choice == 4):
            height = input("Enter height change: ")
            user.updateheight(height)

        elif(choice == 5):
            first = input("Enter first name change")
            last = input("Enter last name change")
            user.updatename(first, last)
            print(user)

        elif(choice == 6):
            newpassword = input("Enter new password")
            newhash = hashpassword(newpassword)
            user.updatepassword(newhash)

        elif(choice == 7):
            metrics = input("Enter new metrics")
            user.updatemetrics(metrics)

        elif(choice == 8):
            goal = int(input("Enter new goal"))
            user.updategoalweight(goal)
            print(user)

        elif(choice == 9):
            updateuser(user, id)
            break

        else:
            print("Incorrect entry please try again")

def mainmenu(user, id):
    while(True):
        enter = int(input("1. Edit User Information: \n2. Add or Update water log: \n3. Add or Update exercise log: \n4.Logout: "))
        if(enter == 1):
            usermenu(user, id)
        elif(enter == 2):
            watermenu(user)
        elif(enter == 3):
            exercisemenu(user)
        elif(enter == 4):
            break
        else:
            print("Invalid selection")

if __name__ == '__main__':
    print("helloworld")
    enter = int(input("Existing user: 1\nNew User: 2 \n"))
    if(enter==1):
        print("Welcome user please enter in you information when prompted")
        username = input("Enter username: ")
        password = input("Enter password: ")
        user1, id = finduser(username, password)
        if(user1 != None):
            mainmenu(user1, id)
        else:
            print("User was not found")

    elif(enter==2):
        print("Welcome new user please enter in you information when prompted")
        fname = input("Enter first name: ")
        lname = input("Enter last name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        currentweight = int(input("Enter your weight in pounds or kg: "))
        goalweight = int(input("Enter your goal weight in pounds or kg: "))
        age = int(input("Enter your age: "))
        height = input("Enter height in inches or centimeters: ")
        metrics = int(input("Enter desired metrics: 1=pounds 0 = kilograms"))
        gender = int(input("Enter your gender: 1=Female 0=Male"))
        watergoal = int(input("Enter a daily water goal (minimum of 64 oz or 1.9L): "))
        password = hashpassword(password)
        userdict = {'fname': fname,
                'lname': lname,
                'username':usename,
                'password':password,
                'currentweight':currentweight,
                'goalweight':goalweight,
                'age':age,
                'height':metrics,
                'startweight':currentweight,
                'metrics': metrics,
                'gender': gender,
                'watergoal': watergoal}

        if(validateuser(userdict)
            user1 = User(fname, lname, username, password,  currentweight, currentweight, goalweight, age,height,metrics,gender, watergoal)
            id = adduser(user1)
            mainmenu(user1, id)
        else:
            print("There was an error in validating your information please try again")
    else:
        print("Incorrect entry please try again")
