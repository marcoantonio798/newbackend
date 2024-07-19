from flask import Flask, render_template, request, redirect, url_for, session  
import os  
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)  
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta aleatória  

# Configuração do PostgreSQL  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)  

# Modelo de Imagem  
class Image(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    filename = db.Column(db.String(120), nullable=False)  

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
    if request.method == 'POST':  
        if 'file' not in request.files:  
            return redirect(request.url)  
        file = request.files['file']  
        if file.filename == '':  
            return redirect(request.url)  
        if file and allowed_file(file.filename):  
            filename = file.filename  
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            
            # Salva a imagem no banco de dados  
            new_image = Image(filename=filename)  
            db.session.add(new_image)  
            db.session.commit()  
            return redirect(url_for('galeria', new_image=filename))  
    return render_template('upload.html')  

@app.route('/')  
def galeria():  
    # Recupera as imagens do banco de dados  
    images = Image.query.all()  
    new_image = request.args.get('new_image')  
    return render_template('galeria.html', images=images, new_image=new_image)  

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
 
if __name__ == '__main__':  
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)  