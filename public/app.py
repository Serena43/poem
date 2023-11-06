from flask import Flask, render_template, request, url_for, flash, redirect # flask: like library, python programme, connects frontend & backend
import sqlite3 #library that connects python & database
import bcrypt

app = Flask(__name__)
app.secret_key = "randommessage"

@app.route('/', methods=['GET']) # / => main homepage; decorator
def index(): #index func calls render_template, showing login.html on website
	return render_template('index.html')

def username_exists(username):
	conn = sqlite3.connect('static/database.db')
	cursor = conn.cursor()
	cursor.execute("Select * from Users where username=?",(username,))
	# * => select (bringing all columns)
	result = cursor.fetchone() #result=none if x exist
	conn.close()
	return result is not None #return False if result is None, True otherwise.

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == "POST":
		username = request.form.get("username") #username: python, "username": html
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		first_name = request.form.get("firstname")
		last_name = request.form.get("lastname")
		email = request.form.get("email")

		password = "password".encode('utf-8')
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(password, salt)

		if username_exists(username):
			flash("Username already exists.") #sending to frontend
		else: #if there is no username which user is trying to register w/
			#connecting to database
			conn = sqlite3.connect("static/database.db")
			cursor = conn.cursor() #명령 to database, needed to execute; conn: db, cursor: 명령
			#				Insert data into table Users (column names); (?) -> python variables
			cursor.execute("Insert INTO USERS (username, password, first_name, last_name, email) VALUES (?,?,?,?,?)",(username,hashed_password,first_name,last_name,email)) #USERS: table name
			conn.commit() #write changes; saving
			conn.close() #disconnecting with the database bc x need db anymore
			return render_template('signup.html') # returning to homepage (login page)
		return render_template('signup.html')

	else: #GET
		return render_template('signup.html') #render_template imported, finds signup.html file (app.py를 기준으로 template folder안에있는걸 찾는거)

def check_password(username, password):
	conn = sqlite3.connect('static/database.db')
	cursor = conn.cursor()
	cursor.execute("Select password from Users where username=?",(username,))
	real_password = cursor.fetchone() #[0] bc returns list
	conn.close()

	if real_password is None:
		return False
	else:
		real_password = real_password[0]

	if password == real_password:
		return True
	else:
		return False

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")

		input_password = "password_attempt".encode('utf-8')

		conn = sqlite3.connect('static/database.db')
		cursor = conn.cursor()
		cursor.execute("Select password from Users where username=?", (username,))
		hashed_password = cursor.fetchone()
		conn.close()

		if bcrypt.checkpw(input_password, hashed_password):
			print("Password is correct!")
		else:
			print("Password is incorrect!")

		if check_password(username, password):
			return redirect(url_for('index')) #index = homepage
		else:
			flash("Invalid username or password!")
		return render_template('login.html')
	else: #if method == GET
		return render_template('login.html')

# Main function (Python syntax)
if __name__ == '__main__':
	app.run(debug=True)