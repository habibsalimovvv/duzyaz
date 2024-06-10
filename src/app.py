import os
from models import model
from flask import Flask, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'



# app.config['MYSQL_HOST'] = os.getenv('database')
# app.config['MYSQL_USER'] = os.getenv('host')
# app.config['MYSQL_PASSWORD'] = os.getenv('password')
# app.config['MYSQL_DB'] = os.getenv('user')

# mysql = MySQL(app)

is_logged_in = False

@app.route('/')
def index():
    if is_logged_in == False:
        return render_template('ana_sayfa.html')
    else:
        return render_template('kullanici_ana_sayfa.html')



@app.route('/duzelt_sayfasi')
def correct_page():
    return render_template('duzelt_sayfasi.html')

@app.route('/giris_ekrani', methods=['GET', 'POST'] )
def login_page():
    global is_logged_in
    if request.method == 'POST':
        is_true = model.login_page(request, User)
        if is_true == False:
           return redirect(url_for('login_page'))
        if is_true == True:
           is_logged_in = True
           print(is_logged_in)
           return redirect(url_for('index')) 
    else:
        return render_template('giris_ekrani.html')

@app.route('/sign_in', methods=['GET', 'POST'] )
def sign_in_page():
    if request.method == 'POST':
        model.sign_in(request, db, User)
        return redirect(url_for('login_page'))
    else:
        return render_template('kayit_ekrani.html')  

@app.route('/correct', methods=['POST'])
def correct_text():
    input_text = request.form.get('input')

    if not input_text:
      return redirect(url_for('correct_page'))

    corrected_text = model.correct_text(input_text)

    return render_template('duzelt_sayfasi.html',corrected=corrected_text, text=input_text )
    

@app.route('/urunler')
def products_page():
    if is_logged_in == False:
        return render_template('urunler.html')
    if is_logged_in == True:
        return render_template('kullanici_urunler.html')

@app.route('/hakkimizda')
def about_page():
    if is_logged_in == False:
        return render_template('hakkimizda.html')
    if is_logged_in == True:
        return render_template('kullanici_hakkimizda.html')

@app.route('/iletisim')
def contact_page():
    if is_logged_in == False:
        return render_template('iletisim.html')
    if is_logged_in == True:
        return render_template('kullanici_iletisim.html')
    
@app.route('/logout')
def logout():
    global is_logged_in
    is_logged_in = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)