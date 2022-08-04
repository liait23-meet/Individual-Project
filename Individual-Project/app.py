from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyAQH97hQMbnc4U1RCtGDqJnJMI4ZGsOJoE",
  "authDomain": "individual-cs-project-3-8-2022.firebaseapp.com",
  "databaseURL": "https://individual-cs-project-3-8-2022-default-rtdb.firebaseio.com/",
  "projectId": "individual-cs-project-3-8-2022",
  "storageBucket": "individual-cs-project-3-8-2022.appspot.com",
  "messagingSenderId": "204266152879",
  "appId": "1:204266152879:web:f449303d3943bff984455a",
  "measurementId": "G-BLKGLBVM6V"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods = ['GET','POST'])
def home():
  return render_template('home.html')

@app.route('/about', methods = ['GET','POST'])
def about():
    return render_template('about.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('addrecipes'))
        #except:
        error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"email": request.form ['email'], "password": request.form['password']}
        return redirect(url_for('signin'))
        #except:
        error = "Authentication failed"
    return render_template("signup.html")

@app.route('/addrecipes', methods = ['GET','POST'])
def addrecipes():
    if request.method == 'POST':
        title = request.form["title"]
        text = request.form["text"]
        recipe = {"title":title, "text":text}
        db.child("Recipes").push(recipe)
        return render_template("addrecipes.html")
    return render_template('addrecipes.html')

# @app.route('/add_tweet', methods=['GET', 'POST'])
# def add_tweet():

#     if request.method == 'POST':
#         try:
#             artical = {"tittle": request.form ['tittle'], "text": request.form ['text']}
#             db.child("addrecipes").push(artical)
#             return redirect(url_for('recipes'))
#         except:
#            print("Couldn't add articles")
#     return render_template("addrecipes.html")


@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    recipes_dict = db.child("Recipes").get().val()
    return render_template("recipes.html", rdict = recipes_dict)


if __name__ == '__main__':
    app.run(debug=True)