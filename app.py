from flask import Flask, render_template, request, redirect, url_for, session  
import os  

app = Flask(__name__)  
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta aleatória  

# Dicionário simulando um banco de dados de usuários  
users = {  
    'fulano': 'senha123'  
}  

# Configuração para upload de arquivos  
UPLOAD_FOLDER = 'static/images'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/upload', methods=['GET', 'POST'])  
def upload():  
    if 'username' in session and session['username'] == 'fulano':  
        if request.method == 'POST':  
            if 'file' not in request.files:  
                return redirect(request.url)  
            file = request.files['file']  
            if file.filename == '':  
                return redirect(request.url)  
            if file and allowed_file(file.filename):  
                filename = file.filename  
                conn = get_db_connection()  
                cur = conn.cursor()  
                cur.execute("INSERT INTO images (filename, user_id) VALUES (%s, %s)", (filename, session['user_id']))  
                conn.commit()  
                cur.close()  
                conn.close()  
                return redirect(url_for('galeria', new_image=filename))  
        return render_template('upload.html')  
    else:  
        return redirect(url_for('login'))  
                 

@app.route('/')  
def galeria():  
    conn = get_db_connection()  
    cur = conn.cursor()  
    cur.execute("SELECT filename FROM images")  
    images = [row[0] for row in cur.fetchall()]  
    new_image = request.args.get('new_image')  
    cur.close()  
    conn.close()  
    return render_template('galeria.html', images=images, new_image=new_image) 



@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
        if username in users and users[username] == password:  
            session['username'] = username  
            return redirect(url_for('user', username=username))  
        else:  
            return render_template('login.html', error='Usuário ou senha inválidos')  
    return render_template('login.html')  

@app.route('/user/<username>')  
def user(username):  
    if 'username' in session and session['username'] == username:  
        return render_template('user.html', username=username)  
    else:  
        return redirect(url_for('login'))  

@app.route('/logout')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))  

@app.route('/about')  
def about():  
    
    return render_template('about.html')

import os  
import psycopg2  

def get_db_connection():  
    conn = psycopg2.connect(  
        host=os.environ.get('dpg-cqaqbt56l47c73clajjg-a'),  
        database=os.environ.get('tatudados'),  
        user=os.environ.get('tatudados_user'),  
        password=os.environ.get('sA3ZzTzCJcl0CpTrcEcGLSjdGVWenpv4'), 
        port=5432,  
    )  
    return conn

if __name__ == '__main__':  
    app.run(debug=True)