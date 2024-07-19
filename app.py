from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory  
import os  

app = Flask(__name__)  
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta aleatória  

# Dicionário simulando um banco de dados de usuários  
users = {  
    'fulano': 'senha123'  
}  

# Configuração para upload de arquivos  
UPLOAD_FOLDER = 'static/images'  
UPLOAD_IDEIAS = 'static/ideias'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  
app.config['UPLOAD_IDEIAS'] = UPLOAD_IDEIAS  

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
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
                 
        return render_template('upload.html')  
    else:  
        return redirect(url_for('login'))

@app.route('/')  
def galeria():  
    images = os.listdir(app.config['UPLOAD_FOLDER'])  # Pega as 3 primeiras imagens  
    new_image = request.args.get('new_image')  
    return render_template('galeria.html', images=images, new_image=new_image)  

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