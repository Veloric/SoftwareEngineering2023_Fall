# Team 3's Python driver
# This is the main driver for the project; hosts all methods, calls to database, as well as functionally runs the website.

from flask import Flask as fl
from flask import url_for, request, render_template, redirect, session
from markupsafe import escape
# import mysql.connector
import re

# Initialize FLASK
app = fl(__name__, static_url_path='/static')
app.secret_key = "Team3Project"

# Database connection functions
def connectdb():
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "mysql",
            database = "bakery"
        )
        print("Connected!")
        return mydb
    except:
        print("Connection failed, uh oh!")


def disconnectdb(mydb):
    mydb.close()


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/order", methods=["GET", "POST"])
def order():
    msg = ""
    # TODO: Rewrite order functionality to support new page functions and layout.
    if request.method == "POST" and "flavor" in request.form and "size" in request.form and "quantity" in request.form and "decor" in request.form:
        flavor = request.form["flavor"]
        size = request.form["size"]
        quantity = request.form["quantity"]
        decor = request.form["decor"]
        mydb = connectdb()
        cursor = mydb.cursor()
        command = "INSERT INTO Orders (CupcakeFlavor, CupcakeSize, CupcakeQuantity, DecorRequests) VALUES (%s, %s, %s, %s)"
        values = (flavor, size, quantity, decor)
        cursor.execute(command, values)
        mydb.commit()
        # for testing purposes only
        print(cursor.rowcount, " record inserted")
        disconnectdb(mydb)
        msg = "Order placed! You may now exit this page. (Create an account to view order history)"
    elif request.method == "POST":
        msg = "There was an error handling your request, please try again!"
        # Testing purposes only
        print(request.form, " List of all data sent")
        
    return render_template("order.html", msg=msg)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    msg = ""
    if request.method == "POST" and "date" in request.form and "time" in request.form and "phone" in request.form and "email" in request.form and "question" in request.form:
        date = request.form["date"]
        time = request.form["time"]
        phone = request.form["phone"]
        email = request.form["email"]
        question = request.form["question"]
        mydb = connectdb()
        cursor = mydb.cursor()
        command = "INSERT INTO Contact (ContactDate, ContactTime, ContactPhone, ContactEmail, ContactQuestion) VALUES (%s, %s, %s, %s, %s)"
        values = (date, time, phone, email, question)
        cursor.execute(command, values)
        mydb.commit()
        # Testing below
        print(cursor.rowcount, " record inserted")
        disconnectdb(mydb)
        msg = "Form received! You may now exit this page."
    elif request.method == "POST":
        msg = "There was an error handling your request, please try again!"
        # Testing below
        print(request.form, " List of all the data sent")

    return render_template("contact.html", msg=msg)

@app.route("/menu")
def menu():
    mydb = connectdb()
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM minidesserts')
    miniMenu = cursor.fetchall()

    cursor.execute('SELECT * FROM desserttray')
    trays = cursor.fetchall()
  
    cursor.execute('SELECT * FROM pieandcheesecake')
    piecheese = cursor.fetchall()

    cursor.execute('SELECT * FROM cupcake')
    cupcake = cursor.fetchall()

    cursor.execute('SELECT * FROM dietary')
    dietary = cursor.fetchall()

    cursor.execute('SELECT * FROM signatureflavorcake')
    sf = cursor.fetchall()

    cursor.execute('SELECT * FROM cake')
    cake = cursor.fetchall()

    disconnectdb(mydb)
    return render_template("menu.html", miniMenu=miniMenu, trays=trays, piecheese=piecheese, cupcake=cupcake, dietary=dietary, sf=sf, cake=cake)

# Admin Menu Functions below
# ADDING TO MENU
@app.route("/addMenu", methods=["GET", "POST"])
def addMenu():
    msg = ""
    if request.method == "POST" and "menuID" in request.form and "categoryName" in request.form and "dessertName" in request.form and "dessertPrice" in request.form:
        menuID = request.form["menuID"]
        categoryName = request.form["categoryName"]
        dessertName = request.form["dessertName"]
        dessertPrice = request.form["dessertPrice"]
        mydb = connectdb()
        cursor = mydb.cursor()
        command = "INSERT INTO MiniDesserts (MenuID, CategoryName, DessertName, DessertPrice) VALUES (%s, %s, %s, %s)"
        values = (menuID, categoryName, dessertName, dessertPrice)
        cursor.execute(command, values)
        mydb.commit()
        print(cursor.rowcount, " record inserted")
        disconnectdb(mydb)
        msg = "Form received! You may now exit this page."
    elif request.method == "POST":
        msg = "There was an error handling your request, please try again!"
        # Testing below
        print(request.form, " List of all the data sent")

    return render_template("addMenu.html", msg=msg)

# EDITING FROM MENU
@app.route("/editMenu", methods=["GET", "POST"])
def editMenu():
    msg = ""

    mydb = connectdb()
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM MiniDesserts")
    rowCount = cursor.fetchall()[0][0]

    if request.method == "POST" and "miniDessertsID" in request.form and "menuID" in request.form and "categoryName" in request.form and "dessertName" in request.form and "dessertPrice" in request.form:
        miniDessertsID = request.form["miniDessertsID"]
        menuID = request.form["menuID"]
        categoryName = request.form["categoryName"]
        dessertName = request.form["dessertName"]
        dessertPrice = request.form["dessertPrice"]

        command = "UPDATE MiniDesserts SET MenuID = %s, CategoryName = %s, DessertName = %s, DessertPrice = %s WHERE MiniDessertsID = %s"
        values = (menuID, categoryName, dessertName, dessertPrice, miniDessertsID)
        cursor.execute(command, values)
        mydb.commit()
        print(cursor.rowcount, " record updated!")
        
        msg = "Form received! You may now exit this page."
    elif request.method == "POST":
        msg = "There was an error handling your request, please try again!"
        # Testing below
        print(request.form, " List of all the data sent")

    disconnectdb(mydb)

    return render_template("editMenu.html", rowCount=rowCount, msg=msg)

# DELETING FROM MENU
@app.route("/deleteMenu", methods=["GET", "POST"])
def deleteMenu():
    msg = ""

    mydb = connectdb()
    cursor = mydb.cursor()

    if request.method == "POST" and "miniDessertsID" in request.form: 
        print(request.form)
        miniDessertsID = request.form["miniDessertsID"]

        check = cursor.execute("SELECT * from MiniDesserts WHERE MiniDessertsID = %s", [(miniDessertsID)])
        print(check, " check")
        if check != "None":
            command = "DELETE from MiniDesserts WHERE MiniDessertsID = %s"
            values = [(miniDessertsID)]
            cursor.execute(command, values)
            mydb.commit()
            print(cursor.rowcount, " record deleted!")
            msg = "Form received! You may now exit this page."
        else:
            msg = "Error, the ID is invalid!"
    elif request.method == "POST":
        msg = "There was an error handling your request, please try again!"
        # Testing below
        print(request.form, " List of all the data sent")

    disconnectdb(mydb)

    return render_template("deleteMenu.html", msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    mydb = connectdb()
    if request.method == "POST" and "username" in request.form and "password" and "email" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        mydb.cursor().execute("SELECT * FROM ACCOUNT WHERE Email = %s", (email))
        account = mydb.cursor().fetchone()
        if account:
            msg = "Account already exists, login to your account!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid email! Try again!"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username can only contain letters and numbers!"
        elif not username or not password or not email:
            msg = "Incomplete forum, please try again."
        else:
            mydb.cursor().execute("INSERT INTO ACCOUNT (Username, Password, Email)")
            mydb.commit()
            msg = "Sucessfully registered! You may now login!"
            disconnectdb(mydb)
            redirect(url_for("login.html"))
    elif request.method == "POST":
        msg = "Please fill out the information before submitting!"
    return render_template("register.html", msg = msg)

@app.route("/login", methods = ["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        mydb = connectdb()
        mydb.cursor().execute("SELECT * FROM ACCOUNT WHERE Username = %s AND Password = %s", (username, password))
        account = mydb.cursor().fetchone()
        if account:
            session["loggedin"] = True
            session["id"] = account["AccountID"]
            session["username"] = username
            disconnectdb()
            redirect(url_for("profile.html"))
        else:
            msg = "Incorrect login!"

    return render_template("login.html", msg = msg)

@app.route("/logout")
def logout():
    #TODO: Allow logging out and removal of session data
    pass

@app.route("/profile")
def profile():
    #TODO: Write profile page, and check admin status
    return render_template("profile.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

if __name__ == '__main__':
    app.run()