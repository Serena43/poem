from flask import Flask, render_template # flask: like library, python programme, connects frontend & backend

app = Flask(__name__)

@app.route('/', methods=['GET']) # / => main homepage; decorator
def index(): #index func calls render_template, showing login.html on website
	return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup():
	return render_template('signup.html') #render_template imported, finds signup.html file (app.py를 기준으로 template folder안에있는걸 찾는거)

# Main function (Python syntax)
if __name__ == '__main__':
	app.run(debug=True)