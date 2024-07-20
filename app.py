from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory  
import os  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.utils import secure_filename  

app = Flask(__name__)  
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta aleatória  

# Dicionário simulando um banco de dados de usuários  
users = {  
    'fulano': 'senha123'  
}  

# Configuração para upload de arquivos  
UPLOAD_FOLDER = 'static/images'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tatudados_user:sA3ZzTzCJcl0CpTrcEcGLSjdGVWenpv4@dpg-cqaqbt56l47c73clajjg-a.oregon-postgres.render.com/tatudados'  
db = SQLAlchemy(app)  

class Image(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    filename = db.Column(db.String(120), nullable=False)  

def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  

@app.route('/upload', methods=['GET', 'POST'])  
def upload():  
    if 'username' in session and session['username'] == 'fulano':  
        if request.method == 'POST':  
            file = request.files['file']  
            if file and allowed_file(file.filename):  
                filename = secure_filename(file.filename)  
                # Salvar o arquivo no diretório  
                file.save(os.path.join(UPLOAD_FOLDER, filename))  
                new_image = Image(filename=filename)  
                db.session.add(new_image)  
                db.session.commit()  
                return redirect(url_for('galeria'))  
            else:  
                # Adicione uma mensagem de erro ou redirecionamento caso o upload falhe  
                return "Tipo de arquivo não permitido", 400  
    return render_template('upload.html')  

@app.route('/galeria')  
def galeria():  
    images = Image.query.all()  
    return render_template('galeria.html', images=images) 

@app.route('/ideias', methods=['GET', 'POST'])  
def ideias():  
    ideias = os.listdir(app.config['UPLOAD_IDEIAS'])    
     
    return render_template('ideias.html', ideias=ideias)  


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

def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  

@app.route('/base')
def base():
    return render_template('base.html')
@app.route('/logout')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))  

@app.route('/about')  
def about():  
    
    return render_template('about.html')

@app.route('/favicon.ico')  
def favicon():  
    return send_from_directory(app.static_folder, 'favicon.ico')
 
if __name__ == '__main__':  
    app.run(debug=True)