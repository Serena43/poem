from flask import Flask, render_template, request,redirect,url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "condingisfun"


@app.route('/', methods=['GET']) # Decorator
def index():
	return render_template('index.html')


def is_username_exists(username):
	conn = sqlite3.connect("static/database.db")
	cursor = conn.cursor()
	cursor.execute("Select * from USERS where username=?",(username,))
	result = cursor.fetchone()
	conn.close()
	return result is not None # return False is result is None, True otherwise.

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		first_name = request.form.get("firstname")
		last_name = request.form.get("lastname")
		email = request.form.get("email")
		if is_username_exists(username):
			flash("Username already exists")
		else:  # if there is not username that user trying to register
			# Connecting to our database
			conn = sqlite3.connect("static/database.db")
			cursor = conn.cursor()
			#              Insert data into table Users
			cursor.execute("Insert INTO USERS (username,password,first_name,last_name,email) VALUES (?,?,?,?,?)",(username,password,first_name,last_name,email))
			conn.commit() # Saving
			conn.close() # disconnect with the databse
			return render_template('signup.html')
		return render_template('signup.html')

	else: # GET
		return render_template('signup.html')

def check_password(username,password):
	conn = sqlite3.connect("static/database.db")
	cursor = conn.cursor()
	cursor.execute("Select password from USERS where username=?",(username,))
	real_password = cursor.fetchone()
	conn.close()
	if cursor.fetchone() is None:
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
		if check_password(username,password):
			return redirect(url_for('index'))
		else:
			flash("Invalid username or password")
		return render_template('login.html')
	else:
		return render_template('login.html')
# Main function
if __name__ == '__main__':
    app.run(debug=True,port=7000)